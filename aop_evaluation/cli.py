"""Command line interface for the evaluation tier.

    baseline   Extract the human baseline from an observed case corpus.
    shadow     Run the shadow-mode comparison of agent choices against human choices.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .metrics import baseline
from .shadow import shadow_evaluate, compare_with_baseline


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aop_evaluation", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("baseline")
    p.add_argument("cases", help="JSONL observed case corpus")
    p.add_argument("--out", default="-")

    p = sub.add_parser("shadow")
    p.add_argument("--aop", required=True)
    p.add_argument("--cases", required=True)
    p.add_argument("--harness-home", default=None)
    p.add_argument("--actions", default=None, help="comma-separated action filter; default evaluates every action the agent would propose")
    p.add_argument("--cohort", default="development", choices=["development", "held-out", "prospective"],
                   help="the cohort label; EV-P2 requires the label to match the corpus provenance")
    p.add_argument("--out", default="-")
    p.add_argument("--report-dir", default=None)

    args = parser.parse_args(argv)

    if args.command == "baseline":
        cases = [json.loads(l) for l in open(args.cases) if l.strip()]
        result = baseline(cases)
    else:
        harness_home = args.harness_home or str(Path(__file__).resolve().parent.parent.parent / "aop-reference-harness")
        actions = args.actions.split(",") if args.actions else None
        report = shadow_evaluate(args.aop, args.cases, harness_home, actions, cohort_label=args.cohort)
        bl = baseline([json.loads(l) for l in open(args.cases) if l.strip()])
        result = dict(report)
        result["phase5_reading"] = compare_with_baseline(report, bl)

    text = json.dumps(result, indent=2)
    if args.out == "-":
        print(text)
    else:
        Path(args.out).write_text(text + "\n")
        if args.report_dir:
            Path(args.report_dir).mkdir(parents=True, exist_ok=True)
            name = ("shadow-%s.json" % result.get("ran_at", "run")).replace(":", "")
            (Path(args.report_dir) / name).write_text(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
