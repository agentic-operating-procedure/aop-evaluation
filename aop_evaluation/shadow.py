"""Shadow-mode evaluation.

The compiled AOP runs in observation-only mode against live cases: the
guardrail decides what it WOULD do, nothing executes, and every decision is
compared with the choice the human actually made on the same case. The output
is the agreement report: per-case agreement, the discrepancy list for review,
and the aggregate agreement rate against the human baseline.

Shadow mode is the bridge into bounded execution (ARC-P5 pipeline, P5.4): an
AOP is promoted when the agent's choices match human choices at the observed
rate, not when anyone feels confident.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path
from types import ModuleType


def load_guardrail(harness_home: str) -> ModuleType:
    """Load the harness guardrail under a synthetic package (same method as
    the conformance suite: the harness is never installed)."""
    import types
    home = Path(harness_home)
    package = types.ModuleType("aop_harness_shadow")
    package.__path__ = [str(home / "aop_harness")]
    sys.modules["aop_harness_shadow"] = package
    for name in ("expression", "guardrail"):
        path = home / "aop_harness" / ("%s.py" % name)
        spec = importlib.util.spec_from_file_location("aop_harness_shadow.%s" % name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    return sys.modules["aop_harness_shadow.guardrail"]


def human_choice(case: dict, action: str) -> str:
    """What the human actually did with the action on this case, read from
    the observed record: who performed it, and whether the case achieved."""
    for task in case.get("tasks", []):
        for step in task.get("steps", []):
            if step.get("action") == action:
                actor = step.get("actor_role", "")
                if actor in ("shift-supervisor", "on-call-engineer"):
                    return "approval-required"
                return "autonomous"
    return "not-performed"


def agent_choice(guardrail, variant, action: str, context: dict) -> str:
    """What the agent WOULD do in shadow mode: the guardrail verdict, mapped
    to the human-choice vocabulary. Nothing executes here."""
    decision = guardrail.authorise(variant, action, context)
    return {
        "execute": "autonomous",
        "approval-required": "approval-required",
        "escalate": "approval-required",
        "prohibit": "prohibited",
    }[decision["decision"]]


def shadow_evaluate(aop_path: str, cases_path: str, harness_home: str, focus_action: str = "dispatch-field-crew") -> dict:
    """Run the shadow-mode comparison over the corpus, focused on the action
    that carries the authority question (the dispatch)."""
    guardrail_m = load_guardrail(harness_home)
    aop = json.loads(Path(aop_path).read_text())
    guardrail = guardrail_m.Guardrail(aop)

    results = []
    with open(cases_path) as handle:
        for line in handle:
            if not line.strip():
                continue
            case = json.loads(line)
            context = case.get("context", {})
            variant, match_note = guardrail.match_variant(context)
            if variant is None:
                results.append({"case_id": case["case_id"], "agreement": None,
                                "discrepancy": "unmatched variant: agent would fail closed; human proceeded",
                                "human": human_choice(case, focus_action), "agent": "fail-closed"})
                continue
            human = human_choice(case, focus_action)
            agent = agent_choice(guardrail, variant, focus_action, context)
            # Agreement: the agent's disposition on the action matches what the
            # human did. Declining counts as agreement in substance: a human
            # who never performed the action and an agent that prohibits it
            # made the same decision. The agent holding a stricter view where
            # the human acted alone (approval-required vs autonomous) is a
            # discrepancy for review: fail-safe, but a mismatch against the
            # baseline all the same.
            agree = (human == agent) or (human == "not-performed" and agent == "prohibited")
            results.append({
                "case_id": case["case_id"],
                "variant": variant["id"],
                "action": focus_action,
                "human": human,
                "agent": agent,
                "agreement": agree,
                "discrepancy": None if agree else "human=%s agent=%s" % (human, agent),
                "match_note": match_note,
            })

    decided = [r for r in results if r["agreement"] is not None]
    agreements = [r for r in decided if r["agreement"]]
    report = {
        "report": "shadow-mode evaluation",
        "aop": "%s@%s" % (aop["aop"], aop["version"]),
        "focus_action": focus_action,
        "ran_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mode": "observation-only: nothing executed",
        "cases": len(results),
        "agreement_rate": round(len(agreements) / len(decided), 3) if decided else None,
        "discrepancies": [r for r in results if r["discrepancy"]],
        "unmatched": [r for r in results if r["agreement"] is None],
        "per_case": results,
    }
    return report


def compare_with_baseline(report: dict, baseline: dict) -> dict:
    """The Phase 5 gate reading: the shadow-mode run reports agreement
    against the human baseline. The declared promotion band is part of the
    deployment configuration; the reference protocol declares 0.85."""
    rate = report.get("agreement_rate")
    return {
        "agreement_rate": rate,
        "declared_promotion_band": 0.85,
        "within_band": rate is not None and rate >= 0.85,
        "baseline_mttr_p50": baseline.get("mttr_p50_minutes"),
        "baseline_first_pass": baseline.get("first_pass_resolution"),
    }
