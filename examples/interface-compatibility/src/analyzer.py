"""Synthetic interface compatibility analysis; NOT flight approval."""
from __future__ import annotations
import json
from pathlib import Path

RANK = {"COMPATIBLE": 0, "REVIEW": 1, "INCOMPATIBLE": 2}

def evaluate(spec: dict) -> dict:
    checks = []
    def add(name, status, reason):
        checks.append({"check": name, "status": status, "reason": reason})

    producer = spec.get("producer")
    consumer = spec.get("consumer")
    if not isinstance(producer, dict) or not isinstance(consumer, dict):
        add("completeness", "REVIEW", "Producer or consumer specification missing")
        return result(spec, checks)

    required = ("format", "transport", "frame_rate_fps", "frame_size_bytes")
    consumer_required = ("accepted_formats", "transport", "capacity_mbps",
                         "processing_rate_fps", "buffer_frames", "drop_tolerance_pct",
                         "max_latency_ms", "latency_components")
    missing = [f"producer.{k}" for k in required if k not in producer]
    missing += [f"consumer.{k}" for k in consumer_required if k not in consumer]
    if missing:
        add("completeness", "REVIEW", "Missing: " + ", ".join(missing))
        return result(spec, checks)

    if producer["format"] not in consumer["accepted_formats"]:
        add("format", "REVIEW" if consumer.get("converter_available") else "INCOMPATIBLE",
            "Image encoding mismatch; adapter verification required" if consumer.get("converter_available") else "No supported encoding or converter")
    else:
        add("format", "COMPATIBLE", "Encoding accepted")

    if producer["transport"] != consumer["transport"]:
        add("protocol", "REVIEW" if consumer.get("gateway_available") else "INCOMPATIBLE",
            "Transport mismatch; gateway requires verification" if consumer.get("gateway_available") else "Direct transport mismatch")
    else:
        add("protocol", "COMPATIBLE", "Transport matches")

    fps = float(producer["frame_rate_fps"])
    frame_bytes = float(producer["frame_size_bytes"])
    capacity = float(consumer["capacity_mbps"])
    if min(fps, frame_bytes, capacity) <= 0:
        add("bandwidth", "REVIEW", "Invalid or non-positive bandwidth inputs")
    else:
        # Assumes declared frame_size_bytes is a conservative upper bound.
        # overhead_fraction includes protocol and link overhead.
        overhead = float(spec.get("overhead_fraction", 0.0))
        if not 0 <= overhead < 1:
            add("bandwidth", "REVIEW", "Invalid overhead fraction")
        else:
            required_mbps = fps * frame_bytes * 8 / 1_000_000 / (1 - overhead)
            status = "INCOMPATIBLE" if required_mbps > capacity else "COMPATIBLE"
            add("bandwidth", status, f"Required {required_mbps:.3f} Mbps; usable capacity {capacity:.3f} Mbps")

    process = float(consumer["processing_rate_fps"])
    tolerance = float(consumer["drop_tolerance_pct"])
    policy = consumer.get("buffer_policy")
    if process <= 0 or fps <= 0 or not 0 <= tolerance <= 100 or not isinstance(consumer["buffer_frames"], int) or consumer["buffer_frames"] < 0:
        add("buffer", "REVIEW", "Invalid buffer inputs")
    elif policy not in ("DROP_OLDEST", "BLOCK"):
        add("buffer", "REVIEW", "Missing or unsupported buffer policy")
    elif fps > process:
        loss = (fps - process) / fps * 100
        if policy == "BLOCK":
            add("buffer", "REVIEW", "Flow-control behavior and effective source rate not specified")
        else:
            add("buffer", "INCOMPATIBLE" if loss > tolerance else "REVIEW",
                f"Steady-state minimum drop rate approximately {loss:.2f}% (tolerance {tolerance:.2f}%)")
    else:
        add("buffer", "COMPATIBLE", "Sustained consumer capacity meets producer rate")

    components = consumer["latency_components"]
    if not isinstance(components, list) or not components or any(
        not isinstance(c, dict) or "worst_ms" not in c or "source" not in c for c in components
    ):
        add("latency", "REVIEW", "Incomplete latency breakdown")
    else:
        worst = sum(float(c["worst_ms"]) for c in components)
        budget = float(consumer["max_latency_ms"])
        if any(float(c["worst_ms"]) < 0 for c in components) or budget <= 0:
            add("latency", "REVIEW", "Invalid latency input")
        elif worst > budget:
            add("latency", "INCOMPATIBLE", f"Assumed worst-case {worst:.2f} ms exceeds {budget:.2f} ms budget")
        elif any(c["source"] != "MEASURED" for c in components):
            add("latency", "REVIEW", f"Assumed worst-case {worst:.2f} ms within budget, but not fully measured")
        else:
            add("latency", "COMPATIBLE", f"Measured bound {worst:.2f} ms within budget")

    return result(spec, checks)

def result(spec, checks):
    return {"scenario": spec.get("id", "unknown"),
            "overall": max((c["status"] for c in checks), key=lambda s: RANK[s], default="REVIEW"),
            "checks": checks,
            "disclaimer": "Synthetic engineering screening only; no certification, qualification, safety or airworthiness approval."}

def evidence_applicability(record: dict) -> dict:
    required = ("config_same", "contract_same", "scope_same", "assumptions_valid", "traceability_complete")
    if any(k not in record for k in required):
        status = "REVIEW"
        reason = "Incomplete evidence applicability record"
    elif not record["scope_same"] or not record["assumptions_valid"] or not record["contract_same"]:
        status = "REVERIFY"
        reason = "Evidence scope, assumptions or interface contract changed"
    elif not record["config_same"] or not record["traceability_complete"]:
        status = "REVIEW"
        reason = "Configuration changed or traceability incomplete"
    else:
        status = "REUSE"
        reason = "Candidate for reuse subject to human engineering review"
    return {"decision": status, "reason": reason,
            "disclaimer": "Advisory only; REUSE does not grant engineering or certification approval."}

def markdown_report(report: dict) -> str:
    lines = [f"# Interface Assessment: {report['scenario']}", "",
             f"**Result:** {report['overall']}", "",
             "| Check | Status | Reason |", "|---|---|---|"]
    for c in report["checks"]:
        lines.append(f"| {c['check']} | {c['status']} | {c['reason']} |")
    lines.extend(["", report["disclaimer"], ""])
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    report = evaluate(json.loads(args.fixture.read_text(encoding="utf-8")))
    output = json.dumps(report, indent=2, sort_keys=True)
    if args.json:
        args.json.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    if args.markdown:
        args.markdown.write_text(markdown_report(report), encoding="utf-8")

if __name__ == "__main__":
    main()
