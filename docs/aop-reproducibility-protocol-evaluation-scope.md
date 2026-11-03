# AOP Reproducibility Protocol (Evaluation Scope)

Informative. This document states what a third party must be able to reproduce from the published artefacts alone, and how. It is the contract behind Demonstrated-level authority: a claim that cannot be reproduced by someone outside the programme is an assertion, not a result.

## 1. What must be reproducible

| Claim | Reproduction |
|---|---|
| The baseline is what the corpus says it is | Run `baseline` on the published case corpus; the numbers must match the published baseline to the stated precision |
| The compiled AOP encodes the observed rules | Run the toolkit compile chain (SOP + corpus + manifest) and compare the digest of the result with the published version |
| The agent's shadow dispositions match human choices at the reported rate | Run `shadow` with the published AOP and the same corpus; the agreement rate and the discrepancy list must match |
| The harness enforces what it claims | Run the conformance suite (HAR-1) against the harness checkout; every check must pass |
| The published provenance reaches the observed cases | Run the registry verify against the published version and the corpus |

## 2. The conditions of reproduction

- No installation: the reference implementations run from their checkouts with the standard library only. A third party clones the repositories and runs the commands; nothing else.
- Determinism: the corpus generator is seeded; the same invocation produces the same corpus; the comparator is deterministic. A reproduction that differs is a defect to file as a finding, not a difference to argue.
- Version pinning: every published result states the versions of the artefacts it used (AOP version, corpus provenance versions, profile version). Results are re-run or explicitly marked stale when any pinned version changes (cascade gate I2).

## 3. What the protocol does not claim

The fixture corpus is synthetic. The published fixture results demonstrate that the chain runs and the numbers are computable; they do not demonstrate performance on live operations. Live claims come from the adoption pilot (Wave 6, CR-006's exemplar programme), run under this same protocol against live observation, with the corpus provenance declaring its capture surface and stitching versions (CG-S14, CG-O1).

## 4. Reporting

A published result carries: the claim, the reproduction command sequence, the pinned versions, the computed numbers, and the date. The shadow report format is machine-readable (JSON) so a third party's reproduction can be diffed against the published report rather than eyeballed.
