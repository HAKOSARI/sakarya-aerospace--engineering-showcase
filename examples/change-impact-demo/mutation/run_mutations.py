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
CATALOG = Path(__file__).resolve().parent / "mutants"
TIMEOUT = 90

def classify(code, xml_file):
    if code not in (0, 1) or not xml_file.exists():
        return "ERROR", []
    try:
        root = ET.parse(xml_file).getroot()
    except ET.ParseError:
        return "ERROR", []
    cases = list(root.iter("testcase"))
    if not cases:
        return "ERROR", []
    assertions, crashes, errors = [], [], []
    for tc in cases:
        name = f'{tc.get("classname", "")}::{tc.get("name", "")}'
        if tc.find("error") is not None:
            errors.append(name)
        failure = tc.find("failure")
        if failure is not None:
            msg = (failure.get("message") or "") + "\n" + (failure.text or "")
            if "AssertionError" in msg or "Failed:" in msg or "pytest.fail" in msg:
                assertions.append(name)
            else:
                crashes.append(name)
    if errors:
        return "ERROR", errors
    if crashes:
        return "CRASHED", crashes
    if assertions and code == 1:
        return "KILLED", assertions
    if code == 0 and not assertions:
        return "SURVIVED", []
    return "ERROR", []

def test(work):
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
        return "TIMEOUT", [], "Timed out"
    status, killers = classify(p.returncode, xml_file)
    return status, killers, (p.stdout + "\n" + p.stderr)[-2500:]

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
        shutil.copytree(DEMO, base, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "mutation-junit.xml"))
        status, _, log = test(base)
        if status != "SURVIVED":
            sys.exit("Baseline must pass before mutation: " + status + "\n" + log)
        for mutant in mutants:
            work = Path(tmp) / mutant["id"]
            shutil.copytree(base, work)
            target = (work / mutant["file"]).resolve()
            if not target.is_relative_to(work.resolve()) or not target.is_file():
                status, killers, detail = "INVALID", [], "Invalid target path"
            else:
                source = target.read_text(encoding="utf-8")
                if source.count(mutant["old"]) != 1:
                    status, killers, detail = "INVALID", [], "Original text not uniquely found"
                else:
                    target.write_text(source.replace(mutant["old"], mutant["new"]), encoding="utf-8")
                    try:
                        py_compile.compile(str(target), cfile=str(work / "mutant.pyc"), doraise=True)
                    except py_compile.PyCompileError as exc:
                        status, killers, detail = "INVALID", [], str(exc)
                    else:
                        status, killers, detail = test(work)
            results.append({"id": mutant["id"], "rule": mutant["rule"],
                            "expected": mutant["expected"], "status": status,
                            "killers": killers, "rationale": mutant["rationale"],
                            "detail": detail if status != "KILLED" else ""})
            print(f'{mutant["id"]}: {status} ({len(killers)} tests)')
    args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    canary = next((m for m in results if m["id"] == "CANARY"), None)
    if canary is None or canary["status"] not in ("CRASHED", "KILLED"):
        sys.exit("CANARY did not execute as expected")
    # Canary deliberately raises: a CRASHED canary proves isolation, not assertion quality.
    if any(m["status"] != m["expected"] for m in results if m["id"] != "CANARY"):
        sys.exit(1)
    print("Core mutation expectations satisfied (canary is execution-only).")

if __name__ == "__main__":
    main()
