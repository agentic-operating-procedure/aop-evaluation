# AOP Independent Evaluation Protocol: Cohorts, Pre-registration and Promotion (Evaluation Scope)

Normative within the evaluation tier. This document is the CR-014 protocol: the rules that make an evaluation claim independent evidence rather than a score on the corpus the rules were compiled from. It supersedes the fixture-only framing where they conflict; the fixture results remain valid as rule-fidelity demonstrations and are labelled as such.

## 1. The cohort separation

EV-P1: Every evaluation names its cohorts, and the cohorts are separated by construction:

| Cohort | Definition | Permitted use |
|---|---|---|
| Development | The corpus the rules were mined or refined from | Compilation and rule refinement only |
| Held-out | Observed cases excluded from every compile, sampled before refinement begins | Shadow-mode comparison; agreement claims |
| Prospective | Live cases observed after the AOP version was bound, run in shadow or bounded mode | Generalisation claims and the live-value claim |

EV-P2: The same cases MUST NOT serve as both rule-mining input and the sole evaluation set. A claim whose only evidence is development-corpus agreement is a rule-fidelity claim and MUST be labelled as one (the fixture results carry this label already).

EV-P3: Cohort composition is published with every result: sizes, sampling method, inclusion and exclusion counts with reasons, date ranges, and known coverage gaps (the substrate's corpus quality facts, CG-S16).

## 2. Pre-registration

EV-P4: Before a prospective run, the protocol is pre-registered: the metrics, the promotion thresholds, the sample size and duration, and the analyses (including the negative-result analyses) are published before the cases are observed. A post-hoc threshold is not a promotion gate.

EV-P5: Pre-registration includes the failure analyses: what result would falsify the claim that the AOP improves the process, and what result would trigger demotion.

## 3. What is measured

EV-P6: Agreement with historical human choices is necessary but not sufficient. The metric set for an independent evaluation adds:

- Adjudicated outcome correctness, with independent labels where the domain allows, and inter-rater disagreement reported where relevant.
- Outcome quality, time and cost against the human baseline (NM-ASR-2), not only disposition match.
- Unsafe action rate, missed escalation, unnecessary escalation, recovery success, drift detection delay.
- Uncertainty: confidence intervals or equivalent, not point estimates alone.

EV-P7: Human agreement is not the target where existing human practice is inconsistent or wrong; where the baseline is known-weak, the evaluation states it and the adjudicated-correctness metrics carry the claim.

## 4. Promotion and the promotion record

EV-P8: Promotion to a wider operating mode requires the pre-registered gates to pass on held-out and prospective cohorts. The promotion record identifies: the AOP version and digest, the harness version, the component matrix (NM-VER-8), the population and operating envelope, the cohorts and their sizes, the results with uncertainty, the residual risks, and who accepted the residual risk.

EV-P9: Elapsed time and successful happy paths alone are never sufficient. Demotion and emergency-stop criteria are declared with the promotion criteria and are measurable (CR-019 binds them to the adoption tiers).

## 5. Independence and replication

EV-P10: An evaluation claim is independent when the cohort, the ground truth, or the evaluator is outside the authoring path (CR-018 owns the governance of independence). The reproducibility protocol (existing) governs third-party reproduction; this protocol governs what the programme itself must run before claiming generalisation.

EV-P11: Negative results are published alongside positive ones, in the same format, with the same provenance discipline. A negative result is a result.

## 6. What this protocol does not fix

Sample-size formulas and statistical methodology are domain choices declared in the pre-registration; the protocol requires uncertainty reporting and pre-declared analyses, not a specific test. Live operational authority remains a governance decision (promotion records go to `aop-governance`), never an evaluation-tier output alone.
