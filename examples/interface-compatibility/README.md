# UAV Interface Compatibility & Evidence Checker — Synthetic POC

**Status:** experimental engineering demonstrator; no certification, qualification, safety or airworthiness decisions.

This independent example checks declared image format, transport, bandwidth, steady-state frame handling and assumed end-to-end latency. It emits deterministic JSON and Markdown reports. All input values are synthetic.

## Engineering corrections to Revision 2

- 1280 × 960 × 8 × 30 = **294.912 Mbit/s** uncompressed payload.
- 40 KiB/frame at 30 fps is **9.8304 Mbit/s**, not 118 Mbit/s. Compression ratios are **not** assumed without measured evidence. Supply a conservative frame-size upper bound.
- A 30 fps producer with a 15 fps sustained consumer must discard approximately **50%** of frames in steady state unless the producer is throttled or processing is changed. A three-frame buffer cannot eliminate the sustained mismatch.
- The sum of Revision 2 worst-case components (5.4 + 2 + 2 + 67 + 70 + 25) is **171.4 ms**, not 160.9 ms. These figures are illustrative, not validated measurements.
- A worst-case budget exceedance is INCOMPATIBLE **under stated assumptions**; missing timing information is REVIEW.
- The latency model only sums explicitly provided components. It does not automatically add frame period or infer real-time guarantees. Components tagged ESTIMATED/ASSUMED require REVIEW unless a stricter failure is found.
- REUSE means evidence *candidate* for human review, never automatic acceptance.

## Run

```bash
python -m unittest discover -s examples/interface-compatibility/tests -p "test_*.py" -v
python examples/interface-compatibility/src/analyzer.py examples/interface-compatibility/data/baseline.json --json /tmp/interface-report.json --markdown /tmp/interface-report.md
```

## Scope and limitations

The frame-drop approximation assumes constant production and sustained consumption, no throttling and a DROP_OLDEST policy. Buffer size affects transient behavior, but cannot fix long-run throughput mismatch. A real implementation needs queue scheduling, packetization, burst behavior, measurement uncertainty, loss, jitter, clock synchronization, codec throughput, and hardware-in-the-loop measurements. The POC uses explicit synthetic assumptions and does not validate physical equipment.

No existing code or pull request is modified.
