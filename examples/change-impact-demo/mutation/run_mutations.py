#!/usr/bin/env python3
"""Isolated, explicitly scoped mutation experiment. Never edits the source tree."""
import argparse
import json
import os
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

DEMO = Path(__file__).resolve().parents[1]
REPO = DEMO.parents[1]
DEMO_REL = DEMO.relative_to(REPO)
CATALOG = Path(__file__).resolve().parent / "mutants"
TIMEOUT = 90

ASSERT_PREFIXES = ("AssertionError", "assert ", "Failed:")

def classify(code, xml_file, expected_tests=None):
    info = {"assertion_failures": [], "crashes": [], "errors": [], "tests": 0, "skipped": 0, "failure_heads": []}
    if code not in (0, 1) or not xml_file.exists():
        return "ERROR", info
    try:
        root = ET.parse(xml_file).getroot()
    except ET.ParseError:
        return "ERROR", info
    cases = list(root.iter("testcase"))
    info["tests"] = len(cases)
    info["skipped"] = sum(tc.find("skipped") is not None for tc in cases)
    if (expected_tests is not None and info["tests"] != expected_tests) or info["skipped"]:
        return "ERROR", info
    for tc in cases:
        name = f'{tc.get("classname", "")}::{tc.get("name", "")}'
        if tc.find("error") is not None:
            info["errors"].append(name)
        failure = tc.find("failure")
        if failure is not None:
            lines = (failure.get("message") or "").strip().splitlines()
            head = lines[0] if lines else ""
            info["failure_heads"].append({"test": name, "head": head})
            key = "assertion_failures" if head.startswith(ASSERT_PREFIXES) else "crashes"
            info[key].append(name)
    if info["errors"]:
        return "ERROR", info
    if info["crashes"]:
        return "CRASHED", info
    if info["assertion_failures"] and code == 1:
        return "KILLED", info
    if code == 0 and not info["assertion_failures"]:
        return "SURVIVED", info
    return "ERROR", info

def test(work, expected_tests=None):
    xml_file = work / "mutation-junit.xml"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(work / "src") + os.pathsep + str(work / "data")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
           "--junitxml=" + str(xml_file), "tests"]
    try:
        p = subprocess.run(cmd, cwd=work, env=env, capture_output=True,
                           text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", {}, "Timed out"
    status, info = classify(p.returncode, xml_file, expected_tests)
    return status, info, (p.stdout + "\n" + p.stderr)[-2500:]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("mutation-results.json"))
    args = parser.parse_args()
    mutants = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CATALOG.glob("*.json"))]
    if not mutants:
        sys.exit("No mutant JSON files found")
    results = []
    with tempfile.TemporaryDirectory(prefix="suhavx-mutation-") as tmp:
        base = Path(tmp) / "base"
        shutil.copytree(REPO, base, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "mutation-junit.xml"))
        status, baseline_info, log = test(base / DEMO_REL)
        if status != "SURVIVED":
            sys.exit("Baseline must pass before mutation: " + status + "\n" + log)
        expected_tests = baseline_info["tests"]
        for mutant in mutants:
            work = Path(tmp) / mutant["id"]
            shutil.copytree(base, work)
            target = (work / DEMO_REL / mutant["file"]).resolve()
            if not target.is_relative_to(work.resolve()) or not target.is_file():
                status, info, detail = "INVALID", {}, "Invalid target path"
            else:
                source = target.read_text(encoding="utf-8")
                if source.count(mutant["old"]) != 1:
                    status, info, detail = "INVALID", {}, "Original text not uniquely found"
                else:
                    target.write_text(source.replace(mutant["old"], mutant["new"]), encoding="utf-8")
                    try:
                        py_compile.compile(str(target), cfile=str(work / "mutant.pyc"), doraise=True)
                    except py_compile.PyCompileError as exc:
                        status, info, detail = "INVALID", {}, str(exc)
                    else:
                        status, info, detail = test(work / DEMO_REL, expected_tests)
            results.append({"id": mutant["id"], "rule": mutant["rule"],
                            "expected": mutant["expected"], "status": status,
                            "killers": info.get("assertion_failures", []), "assertion_failures": info.get("assertion_failures", []),
                            "crashes": info.get("crashes", []), "errors": info.get("errors", []),
                            "tests": info.get("tests"), "skipped": info.get("skipped"),
                            "failure_heads": info.get("failure_heads", []),
                            "rationale": mutant["rationale"],
                            "detail": detail if status != "KILLED" else ""})
            print(f'{mutant["id"]}: {status} ({len(info.get("assertion_failures", []))} assertions)')
    args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    canary = next((m for m in results if m["id"] == "CANARY"), None)
    if canary is None or canary["status"] != "KILLED" or not any(
        "CANARY: isolated mutant was executed" in item["head"] for item in canary["failure_heads"]
    ):
        sys.exit("CANARY did not execute as expected")
    # Canary must produce the exact assertion message in the isolated copy.
    if any(m["status"] != m["expected"] for m in results if m["id"] != "CANARY"):
        sys.exit(1)
    print("Core mutation expectations satisfied (canary is execution-only).")

if __name__ == "__main__":
    main()
