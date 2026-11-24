# Changelog

All notable changes to this repository are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is semantic: the major version changes when a metric definition or the shadow-mode comparison semantics change, the minor version when substantive evaluation content is added, and the patch version for corrections that do not change meaning.

## [Unreleased]

## [0.3.0] - 2026-11-05

### Added (Wave H4: CR-014)

- The independent evaluation protocol: cohort separation (development, held-out, prospective), pre-registration with falsifiers, the extended metric set (adjudicated correctness, unsafe action rate, uncertainty), promotion records, negative results published, independence defined.
- The cohort module: deterministic seeded split, pre-registration records, promotion records.
- Shadow reports carry the cohort label and the claim class (rule-fidelity versus generalisation): a development-corpus result can no longer pass as a generalisation claim.

## [0.2.0] - 2026-11-05

### Added (Wave H2: CR-013)

- Origin filtering: agent-originated cases are excluded from baseline mining by default; the protected human reservoir is the human-originated set; the corpus quality block reports the origin mix and undeclared origins (NM-CTL-6, CG-S15).

## [0.1.1] - 2026-11-05

### Changed

- The shadow comparator measures authority fidelity: the agent agrees when it is not more permissive than the human on the same action. Conservative deviations (agent declines where the human acted with approval) are surfaced separately for rule refinement, and only more-permissive behaviour counts as a violation. Approver roles derive from approval-kind handoffs and escalation routes, not from every handoff recipient.
- The comparison is per action the agent would propose, not per case on a single focus action.

Found and corrected against the 5G exemplar corpus; the fault management regression reports agreement 1.0 unchanged.


## [0.1.0] - 2026-11-04

### Evaluation foundations

- Published the metric definitions with canonical OpenDEA bindings: three metrics bound to dea:metric-* records, five with declared gaps to lodge as contributions (NM-INT-5).
- Published baseline extraction: the human baseline computed from the observed corpus (NM-ASR-2).
- Published shadow-mode evaluation: observation-only comparison of agent dispositions with human choices on the same cases, declining-in-substance counting as agreement, discrepancies listed for review, and the Phase 5 gate reading against the declared 0.85 promotion band.
- The fixture shadow run reports agreement 1.0 within the promotion band, framed honestly as rule fidelity against the compiled corpus, not live generalisation.
- Published the reproducibility protocol: standard library only, deterministic, version-pinned, machine-diffable reports.
[0.1.0]: https://github.com/agentic-operating-procedure/aop-evaluation/releases/tag/v0.1.0
[0.1.1]: https://github.com/agentic-operating-procedure/aop-evaluation/compare/v0.1.0...v0.1.1
[Unreleased]: https://github.com/agentic-operating-procedure/aop-evaluation/compare/v0.3.0...HEAD
[0.2.0]: https://github.com/agentic-operating-procedure/aop-evaluation/compare/v0.1.1...v0.2.0
[0.3.0]: https://github.com/agentic-operating-procedure/aop-evaluation/compare/v0.2.0...v0.3.0
