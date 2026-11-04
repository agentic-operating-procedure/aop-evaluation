"""Metric definitions.

The names and definitions here are the canonical metric registry for the
programme. The substrate's case corpus (aop-context-graph) supplies the raw
counts; the human baseline is extracted from the observed corpus; the metrics
bind to canonical OpenDEA metric records where they exist (NM-INT-5), with
gaps declared where they do not.
"""

from __future__ import annotations

from statistics import median

# Canonical binding: metric name -> dea:metric-* reference or declared gap.
METRIC_BINDINGS = {
    "mean_time_to_detect": {"metric_ref": "dea:metric-mean-time-to-detect", "directionality": "lower_is_better"},
    "ai_incident_escalation_compliance": {"metric_ref": "dea:metric-ai-incident-escalation-compliance", "directionality": "higher_is_better"},
    "cell_outage_rate": {"metric_ref": "dea:metric-cell-outage-rate", "directionality": "lower_is_better"},
    "mttr_p50_minutes": {"gap": "No canonical dea:metric-* for p50 mean time to restore in network fault management; lodge a metric contribution to dea-catalog-metrics."},
    "first_pass_resolution": {"gap": "No canonical dea:metric-* for first-pass fix rate in network fault management; lodge a metric contribution to dea-catalog-metrics."},
    "exception_rate": {"gap": "No canonical dea:metric-* for case-level exception rate in network fault management; lodge a metric contribution."},
    "escalation_precision": {"gap": "No canonical dea:metric-* for escalation precision in network fault management; lodge a metric contribution."},
    "drift_detection_latency": {"gap": "No canonical dea:metric-* for drift detection latency; lodge a metric contribution."},
}


def cycle_time_p50(cases: list[dict]) -> float | None:
    """Median case cycle time from observed outcome.cycle_time values."""
    values = [c.get("outcome", {}).get("cycle_time") for c in cases if c.get("outcome", {}).get("cycle_time") is not None]
    return round(median(values), 1) if values else None


def first_pass_resolution(cases: list[dict]) -> float | None:
    """Share of achieved outcomes that needed no rework beyond the anticipated set."""
    outcomes = [c.get("outcome", {}) for c in cases]
    achieved = [o for o in outcomes if o.get("result") == "achieved"]
    if not outcomes:
        return None
    first_pass = [o for o in achieved if o.get("first_pass") is True]
    return round(len(first_pass) / len(outcomes), 3)


def exception_rate(cases: list[dict]) -> float:
    """Exceptions per case across the corpus."""
    total = sum(
        1
        for c in cases
        for t in c.get("tasks", [])
        for s in t.get("steps", [])
        for _e in s.get("exceptions", [])
    )
    return round(total / len(cases), 3) if cases else 0.0


def escalation_precision(cases: list[dict], warrant_threshold: float = 0.5) -> float | None:
    """Of the escalated cases, the proportion where escalation was
    retrospectively warranted: the observed outcome was not_achieved or the
    case carried a critical exception."""
    escalated = 0
    warranted = 0
    for c in cases:
        has_escalation = any(
            s.get("exceptions") and any(e.get("escalation") for e in s["exceptions"])
            for t in c.get("tasks", [])
            for s in t.get("steps", [])
        )
        if not has_escalation:
            continue
        escalated += 1
        outcome = c.get("outcome", {}).get("result")
        critical = any(
            e.get("severity") == "critical"
            for t in c.get("tasks", [])
            for s in t.get("steps", [])
            for e in s.get("exceptions", [])
        )
        if outcome == "not_achieved" or critical:
            warranted += 1
    return round(warranted / escalated, 3) if escalated else None


def filter_human(cases: list[dict]) -> tuple[list[dict], list[dict]]:
    """NM-CTL-6 / CR-013: split the corpus by case origin. Human-originated
    cases form the baseline and the protected reservoir; agent-originated
    cases are excluded from baseline mining by default. Cases without a
    declared origin are treated as human (pre-dating origin tagging) and the
    undeclared share is reported."""
    human = [c for c in cases if c.get("origin", "human") != "agent"]
    agent = [c for c in cases if c.get("origin") == "agent"]
    undeclared = sum(1 for c in cases if "origin" not in c)
    return human, agent


def baseline(cases: list[dict], exclude_agent_origin: bool = True) -> dict:
    """The human baseline: the observed human values for the domain metrics
    (NM-ASR-2), extracted from the observed corpus. Agent-originated cases
    are excluded by default (loop hygiene, CR-013); the corpus quality block
    reports the origin mix and any undeclared origins."""
    if exclude_agent_origin:
        human, agent = filter_human(cases)
    else:
        human, agent = cases, []
    return {
        "mttr_p50_minutes": cycle_time_p50(human),
        "first_pass_resolution": first_pass_resolution(human),
        "exception_rate": exception_rate(human),
        "escalation_precision": escalation_precision(human),
        "metric_bindings": METRIC_BINDINGS,
        "corpus_quality": {
            "total_cases": len(cases),
            "human_or_undeclared": len(human),
            "agent_origin_excluded": len(agent),
            "undeclared_origin": sum(1 for c in cases if "origin" not in c),
            "reservoir_note": "agent-originated cases are excluded from the baseline and the protected human reservoir is the human-originated set (CR-013)",
        },
    }
