#!/usr/bin/env python3
"""Sample-size helper for AB experiment planning.

Supports stable first-pass calculations for:
- conversion/proportion metrics with equal group allocation
- mean/per-user-value metrics with equal group allocation

Outputs JSON so another agent can paste the result into a Feishu plan or review.
"""

from __future__ import annotations

import argparse
import json
import math
from statistics import NormalDist


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return parsed


def ratio_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0 or parsed > 1:
        raise argparse.ArgumentTypeError("must be in (0, 1]")
    return parsed


def resolve_delta(baseline: float | None, mde: float | None, relative_mde: float | None) -> float:
    if mde is not None and relative_mde is not None:
        raise ValueError("Use either --mde or --relative-mde, not both.")
    if mde is not None:
        return mde
    if relative_mde is not None:
        if baseline is None:
            raise ValueError("--relative-mde requires --baseline.")
        return baseline * relative_mde
    raise ValueError("Provide --mde or --relative-mde.")


def conversion_sample_size(
    baseline: float,
    delta: float,
    alpha: float,
    power: float,
) -> int:
    p1 = baseline
    p2 = baseline + delta
    if p1 <= 0 or p1 >= 1:
        raise ValueError("--baseline for conversion metrics must be in (0, 1).")
    if p2 <= 0 or p2 >= 1:
        raise ValueError("baseline + MDE for conversion metrics must be in (0, 1).")

    z_alpha = NormalDist().inv_cdf(1 - alpha / 2)
    z_beta = NormalDist().inv_cdf(power)
    pooled = (p1 + p2) / 2
    numerator = (
        z_alpha * math.sqrt(2 * pooled * (1 - pooled))
        + z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    )
    return math.ceil((numerator / abs(delta)) ** 2)


def mean_sample_size(stddev: float, delta: float, alpha: float, power: float) -> int:
    z_alpha = NormalDist().inv_cdf(1 - alpha / 2)
    z_beta = NormalDist().inv_cdf(power)
    return math.ceil(2 * ((z_alpha + z_beta) * stddev / abs(delta)) ** 2)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Calculate first-pass AB sample size.")
    parser.add_argument("--metric", choices=["conversion", "mean"], required=True)
    parser.add_argument("--baseline", type=positive_float)
    parser.add_argument("--mde", type=positive_float, help="Absolute minimum detectable effect.")
    parser.add_argument(
        "--relative-mde",
        type=positive_float,
        help="Relative MDE. Example: 0.1 means a 10 percent lift from baseline.",
    )
    parser.add_argument("--stddev", type=positive_float, help="Required for mean metrics.")
    parser.add_argument("--groups", type=int, default=2, help="Total number of experiment groups.")
    parser.add_argument("--alpha", type=ratio_float, default=0.05)
    parser.add_argument("--power", type=ratio_float, default=0.80)
    parser.add_argument("--daily-traffic", type=positive_float)
    parser.add_argument("--duration-days", type=positive_float)
    parser.add_argument("--gray-cap", type=ratio_float, default=1.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.groups < 2:
        raise SystemExit("--groups must be >= 2")

    delta = resolve_delta(args.baseline, args.mde, args.relative_mde)
    caveats = [
        "Assumes independent users, equal group allocation, two-sided alpha, and user-level analysis.",
        "Does not adjust for multiple comparisons when more than two groups are used.",
    ]

    if args.metric == "conversion":
        if args.baseline is None:
            raise SystemExit("--baseline is required for conversion metrics.")
        per_group = conversion_sample_size(args.baseline, delta, args.alpha, args.power)
    else:
        if args.stddev is None:
            raise SystemExit("--stddev is required for mean metrics.")
        per_group = mean_sample_size(args.stddev, delta, args.alpha, args.power)

    total_required = per_group * args.groups
    result = {
        "metric_type": args.metric,
        "alpha": args.alpha,
        "power": args.power,
        "groups": args.groups,
        "per_group_required_sample": per_group,
        "total_required_sample": total_required,
        "caveats": caveats,
    }

    if args.daily_traffic is not None and args.duration_days is not None:
        available_at_full_traffic = args.daily_traffic * args.duration_days
        required_gray_ratio = total_required / available_at_full_traffic
        feasible_at_gray_cap = available_at_full_traffic * args.gray_cap
        result.update(
            {
                "daily_traffic": args.daily_traffic,
                "duration_days": args.duration_days,
                "gray_cap": args.gray_cap,
                "available_sample_at_full_traffic": math.floor(available_at_full_traffic),
                "required_gray_ratio": required_gray_ratio,
                "feasible_at_gray_cap": feasible_at_gray_cap >= total_required,
            }
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
