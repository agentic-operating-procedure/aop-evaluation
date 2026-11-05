# AOP Evaluation

`aop-evaluation` is the single authority for whether the method produces a measured result: the metric definitions, the baseline extraction from observed human execution, the shadow-mode evaluation comparing agent choices with human choices, and the reproducibility protocol.

| Field | Value |
|---|---|
| Authority | Whether the method produces a measured result: baselines, shadow mode, metrics, reproducibility |
| Tier | Evaluation |
| Landing wave | 5 |
| Version | 0.3.0 |
| Status | Stable |
| Licence | MIT |

## What this repository owns

- The metric definitions and their canonical bindings: mean time to detect, AI incident escalation compliance and cell outage rate bind to `dea:metric-*` records in the OpenDEA metrics catalog; MTTR-p50, first-pass resolution, exception rate, escalation precision and drift detection latency carry declared gaps to lodge as contributions (NM-INT-5).
- Baseline extraction: the human baseline (NM-ASR-2) computed from the observed corpus.
- Shadow-mode evaluation: the compiled AOP runs in observation-only mode; the agent's dispositions are compared with the human's choices on the same cases; the output is the agreement report and the discrepancy list for review.
- The Phase 5 gate reading: the shadow run reports agreement against the human baseline against the declared promotion band.

## What this repository does not own

- The harness being evaluated. That is `aop-reference-harness`, loaded from its checkout.
- The conformance of what it measures. That is `aop-conformance`.
- The metrics that are properties of a specific domain rather than of the method.

## What the fixture result does and does not show

The fixture shadow run reports agreement 1.0 against the corpus. That number is honest and narrow: the corpus is the same observation the AOP's rules were compiled from, so the run validates rule fidelity against the observed human decisions, which is exactly what compilation claims. It does not show generalisation to live cases; that claim belongs to the adoption pilot on live observation, which is Wave 6 and CR-006's exemplar programme.

## Running

```
python3 -m aop_evaluation baseline <cases.jsonl>
python3 -m aop_evaluation shadow --aop <compiled-aop.json> --cases <cases.jsonl> --report-dir reports
```

## Documentation

| Document | Scope |
|---|---|
| [The reproducibility protocol](./docs/aop-reproducibility-protocol-evaluation-scope.md) | What a third party must be able to reproduce, and how |
