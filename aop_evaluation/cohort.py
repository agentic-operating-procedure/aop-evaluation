"""Cohort separation, pre-registration and promotion records (EV-P1 to EV-P9).

The cohort split is deterministic: a seeded hash of the case id assigns each
case to development or held-out, so the split is reproducible and the held-out
cohort is excluded from every compile that declares the same seed.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path


def split_cohorts(cases_path: str, seed: str = "cohort-seed-1", held_out_fraction: float = 0.25) -> dict:
    """Deterministically split a corpus into development and held-out
    cohorts. The seed travels into the compile provenance so a held-out
    cohort cannot leak into a later compile unnoticed."""
    dev, held = [], []
    with open(cases_path) as handle:
        for line in handle:
            if not line.strip():
                continue
            case = json.loads(line)
            digest = hashlib.sha256((seed + case["case_id"]).encode()).hexdigest()
            (held if int(digest[:8], 16) / 0xFFFFFFFF < held_out_fraction else dev).append(case)
    return {"seed": seed, "development": dev, "held_out": held,
            "development_cases": len(dev), "held_out_cases": len(held),
            "note": "the seed MUST be recorded in the compile provenance; compiles that consumed held-out cases are detectable by comparing digests"}


def pre_register(metrics: list[dict], promotion_thresholds: dict, sample_size: int, duration_days: int, analyses: list[str], registered_by: str) -> dict:
    """EV-P4: publish the protocol before the cases are observed."""
    record = {
        "pre_registration": {
            "metrics": metrics,
            "promotion_thresholds": promotion_thresholds,
            "sample_size": sample_size,
            "duration_days": duration_days,
            "analyses": analyses,
            "falsifiers": [a for a in analyses if "falsif" in a.lower()],
            "registered_by": registered_by,
            "registered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    }
    return record


def promotion_record(aop_ref: str, harness_version: str, component_matrix: dict,
                     cohorts: dict, results: dict, residual_risks: list[str],
                     risk_accepted_by: str, gates_passed: bool) -> dict:
    """EV-P8: the promotion record. A promotion decision goes to aop-governance;
    this is the evidence attachment."""
    return {
        "promotion_record": {
            "aop_ref": aop_ref,
            "harness_version": harness_version,
            "component_matrix": component_matrix,
            "cohorts": {k: v for k, v in cohorts.items() if isinstance(v, (int, str))},
            "results": results,
            "gates_passed": gates_passed,
            "residual_risks": residual_risks,
            "risk_accepted_by": risk_accepted_by,
            "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "note": "promotion is a governance decision (aop-governance); this record is its evidence",
        }
    }
