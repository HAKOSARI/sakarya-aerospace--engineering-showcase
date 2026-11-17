#!/usr/bin/env python3
"""Pinned-source synthetic diagnostic. Exit 0 only when every comparison passes."""
import argparse
from dataclasses import replace
from datetime import date, timedelta
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[3]
SOURCE = 'examples/change-impact-demo/src/camera_evidence.py'
VOCAB = ('EO_CAMERA', 'IR_CAMERA', 'GIMBAL', 'LASER_RANGEFINDER', 'MISSION_COMPUTER')


def evaluate(module, inject_oracle_failure=False):
    baseline = module.ChangeBaseline(frozenset(), 'IF-1', 'CFG-1', date(2026, 11, 17))
    evidence = module.Evidence('EV-1', 'TEST-1', 'IF-1', 'CFG-1', baseline.evaluation_date,
                               'PASS', True, frozenset(VOCAB))
    template = module.RequirementCase('REQ-1', frozenset(), evidence, frozenset(VOCAB))
    comparisons = []

    def check(kind, label, case, expected, target=baseline):
        actual = module.recommend(case, target)
        wanted = (*expected, False)
        observed = (actual.outcome, actual.rule_id, actual.accepted)
        comparisons.append({'group': kind, 'id': label, 'expected': wanted,
                            'actual': observed, 'pass': observed == wanted})

    if frozenset(VOCAB) != module.SUBSYSTEM_IDS:
        raise ValueError('Diagnostic vocabulary does not match source vocabulary')
    for required in range(1, 32):
        for tested in range(1, 32):
            req = frozenset(n for i, n in enumerate(VOCAB) if required & (1 << i))
            covered = frozenset(n for i, n in enumerate(VOCAB) if tested & (1 << i))
            expected = ('REUSE', 'R6') if required & tested == required else ('REVERIFY', 'R7')
            if inject_oracle_failure and (required, tested) == (1, 1):
                expected = ('REVIEW', 'R4')
            check('scope_pairs', f'{required}:{tested}',
                  replace(template, requirement_scope=req, evidence=replace(evidence, tested_scope=covered)), expected)
    for age in (-1, 0, 364, 365, 366):
        expected = ('REVIEW', 'R5') if age < 0 or age > 365 else ('REUSE', 'R6')
        check('dates', str(age), replace(template, evidence=replace(
            evidence, date=baseline.evaluation_date - timedelta(days=age))), expected)
    for label, scope in [('missing', None), ('empty', frozenset()), ('unknown', frozenset({'UNKNOWN'}))]:
        check('invalid_scope', label, replace(template, evidence=replace(evidence, tested_scope=scope)), ('REVIEW', 'R4'))
    return comparisons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-commit', required=True, help='Full 40-character immutable commit SHA')
    parser.add_argument('--source-sha256', required=True, help='Expected digest of that commit source')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--inject-oracle-failure', action='store_true', help='Negative execution control only')
    args = parser.parse_args()
    report = {'evidence_level': 'SYNTHETIC_SOFTWARE_ONLY', 'source_commit': args.source_commit,
              'expected_source_sha256': args.source_sha256, 'python': platform.python_version(),
              'source_path': SOURCE, 'raw_result_path': str(args.output),
              'negative_control': args.inject_oracle_failure, 'all_pass': False}
    try:
        if not re.fullmatch(r'[0-9a-f]{40}', args.source_commit):
            raise ValueError('Full commit SHA required; symbolic refs are not accepted')
        if not re.fullmatch(r'[0-9a-f]{64}', args.source_sha256):
            raise ValueError('64-character SHA-256 required')
        source = subprocess.run(['git', 'show', f'{args.source_commit}:{SOURCE}'], cwd=REPO,
                                check=True, capture_output=True).stdout
        report['source_sha256'] = hashlib.sha256(source).hexdigest()
        if report['source_sha256'] != args.source_sha256:
            raise ValueError('Commit/source digest mismatch: stopped before module execution')
        # Import the actual git blob, not a second source copy embedded in this script.
        with tempfile.TemporaryDirectory(prefix='suhavx-diagnostic-') as temp:
            path = Path(temp) / 'camera_evidence.py'
            path.write_bytes(source)
            spec = importlib.util.spec_from_file_location('pinned_camera_evidence', path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            report['comparisons'] = evaluate(module, args.inject_oracle_failure)
        report['comparison_count'] = len(report['comparisons'])
        report['mismatch_count'] = sum(not row['pass'] for row in report['comparisons'])
        report['all_pass'] = report['mismatch_count'] == 0
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('source_commit', 'all_pass', 'negative_control')}))
    return 0 if report['all_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
