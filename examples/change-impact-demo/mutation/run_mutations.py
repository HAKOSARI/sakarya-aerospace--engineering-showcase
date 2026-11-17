#!/usr/bin/env python3
"""Isolated, explicitly scoped mutation experiment. Never edits the source tree."""
import argparse
import hashlib
import platform
from time import perf_counter
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

def test(work, expected_tests=None, test_paths=None):
    xml_file = work / "mutation-junit.xml"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(work / "src") + os.pathsep + str(work / "data")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
           "--junitxml=" + str(xml_file)] + (test_paths or ["tests"])
    started = perf_counter()
    try:
        p = subprocess.run(cmd, cwd=work, env=env, capture_output=True,
                           text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", {}, "Timed out"
    status, info = classify(p.returncode, xml_file, expected_tests)
    info["elapsed_seconds"] = perf_counter() - started
    return status, info, (p.stdout + "\n" + p.stderr)[-2500:]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("mutation-results.json"))
    parser.add_argument("--shadow-selected", action="store_true",
                        help="Compare a fixed subset with the full suite; never replace full execution")
    args = parser.parse_args()
    mutants = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CATALOG.glob("*.json"))]
    if not mutants:
        sys.exit("No mutant JSON files found")
    # Fixed before execution; do not use observed killers to choose this list.
    selected = ["tests/test_camera_evidence.py", "tests/test_scope_evidence.py"]
    selection = {"paths": selected, "reason": "Direct import of camera_evidence; full suite remains authoritative",
                 "sha256": {p: hashlib.sha256((DEMO / p).read_bytes()).hexdigest() for p in selected}}
    report = {"schema": 2, "evidence_level": "SYNTHETIC_SOFTWARE_ONLY",
              "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
              "source_sha256": hashlib.sha256((DEMO / "src/camera_evidence.py").read_bytes()).hexdigest(),
              "python": platform.python_version(), "selection": selection if args.shadow_selected else None,
              "selection_enabled_in_ci": False, "controls": [], "results": []}
    results = report["results"]
    with tempfile.TemporaryDirectory(prefix="suhavx-mutation-") as tmp:
        base = Path(tmp) / "base"
        shutil.copytree(REPO, base, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "mutation-junit.xml"))
        status, baseline_info, log = test(base / DEMO_REL)
        report["controls"].append({"id": "CLEAN", "status": status, "info": baseline_info,
                                   "patch_applied": False, "target_reached": "unknown",
                                   "behavior_changed": "unknown", "detected": status == "KILLED"})
        if status != "SURVIVED":
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, indent=2) + "\n")
            sys.exit("Baseline must pass before mutation: " + status + "\n" + log)
        expected_tests = baseline_info["tests"]
        noop = Path(tmp) / "noop"
        shutil.copytree(base, noop)
        target = noop / DEMO_REL / "src/camera_evidence.py"
        target.write_text(target.read_text() + "\n# Semantically inert mutation control.\n")
        noop_status, noop_info, noop_log = test(noop / DEMO_REL, expected_tests)
        report["controls"].append({"id": "NOOP_COMMENT", "status": noop_status, "info": noop_info,
                                   "patch_applied": True, "target_reached": "unknown",
                                   "behavior_changed": "unknown", "detected": noop_status == "KILLED",
                                   "reason": "Comment-only edit; no assertion change in full suite is not exhaustive equivalence proof."})
        if noop_status != "SURVIVED":
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, indent=2) + "\n")
            sys.exit("No-op control must pass: " + noop_status + "\n" + noop_log)
        selected_count = None
        if args.shadow_selected:
            for label, root in [("CLEAN", base), ("NOOP_COMMENT", noop)]:
                sub_status, sub_info, _ = test(root / DEMO_REL, selected_count, selected)
                if label == "CLEAN":
                    selected_count = sub_info.get("tests")
                next(c for c in report["controls"] if c["id"] == label)["shadow"] = {"status": sub_status, "info": sub_info}
                if sub_status != "SURVIVED":
                    args.output.parent.mkdir(parents=True, exist_ok=True)
                    args.output.write_text(json.dumps(report, indent=2) + "\n")
                    sys.exit("Selected control failed; shadow comparison stopped")
        for mutant in mutants:
            work = Path(tmp) / mutant["id"]
            shutil.copytree(base, work)
            target = (work / DEMO_REL / mutant["file"]).resolve()
            applied = False
            if not target.is_relative_to(work.resolve()) or not target.is_file():
                status, info, detail = "INVALID", {}, "Invalid target path"
            else:
                source = target.read_text(encoding="utf-8")
                if source.count(mutant["old"]) != 1:
                    status, info, detail = "INVALID", {}, "Original text not uniquely found"
                else:
                    changed = source.replace(mutant["old"], mutant["new"])
                    target.write_text(changed, encoding="utf-8")
                    applied = changed != source and target.read_text(encoding="utf-8") == changed
                    try:
                        py_compile.compile(str(target), cfile=str(work / "mutant.pyc"), doraise=True)
                    except py_compile.PyCompileError as exc:
                        status, info, detail = "INVALID", {}, str(exc)
                    else:
                        status, info, detail = test(work / DEMO_REL, expected_tests)
            row = {"id": mutant["id"], "rule": mutant["rule"],
                   "expected": mutant["expected"], "status": status,
                   "patch_applied": applied, "target_reached": "unknown", "behavior_changed": "unknown",
                   "detected": True if status == "KILLED" else False if status == "SURVIVED" else "unknown",
                   "activation_reason": "No per-mutant reachability/infection instrumentation; canary does not establish this.",
                   "killers": info.get("assertion_failures", []), "assertion_failures": info.get("assertion_failures", []),
                   "crashes": info.get("crashes", []), "errors": info.get("errors", []),
                   "tests": info.get("tests"), "skipped": info.get("skipped"),
                   "elapsed_seconds": info.get("elapsed_seconds"),
                   "failure_heads": info.get("failure_heads", []),
                   "rationale": mutant["rationale"], "detail": detail if status != "KILLED" else ""}
            if args.shadow_selected and status in ("KILLED", "SURVIVED"):
                sub_status, sub_info, _ = test(work / DEMO_REL, selected_count, selected)
                full_failures = set(row["assertion_failures"])
                selected_failures = set(sub_info.get("assertion_failures", []))
                row["shadow"] = {"status": sub_status, "info": sub_info,
                                 "missed_failure_ids": sorted(full_failures - selected_failures),
                                 "unexpected_failure_ids": sorted(selected_failures - full_failures),
                                 "failure_retention": len(full_failures & selected_failures) / len(full_failures)
                                     if full_failures else None}
            results.append(row)
            print(f'{mutant["id"]}: {status} ({len(info.get("assertion_failures", []))} assertions)')
    canary = next((m for m in results if m["id"] == "CANARY"), None)
    canary_ok = canary is not None and canary["status"] == "KILLED" and any(
        "CANARY: isolated mutant was executed" in item["head"] for item in canary["failure_heads"])
    report["canary_execution_confirmed"] = canary_ok
    report["all_expected"] = canary_ok and all(m["status"] == m["expected"] for m in results)
    report["shadow_agrees"] = None if not args.shadow_selected else all(
        "shadow" in m and m["shadow"]["status"] == m["status"]
        and not m["shadow"]["missed_failure_ids"] and not m["shadow"]["unexpected_failure_ids"] for m in results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not report["all_expected"] or report["shadow_agrees"] is False:
        sys.exit(1)
    print("Mutation expectations satisfied. Activation unknown; subset remains shadow-only.")

if __name__ == "__main__":
    main()
