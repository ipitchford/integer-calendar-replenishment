#!/usr/bin/env python3
"""Independent, standard-library verification of the harmonic calendar theorem.

This checker was written from the mathematical construction, without reading or
importing the production solver. It uses explicit ceiling-event generation and
exhaustive finite set tables. Run from any directory; its default output is the
bundle/data directory adjoining this source directory.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import random


def require(condition, message):
    """Explicit check that stays active under python -O (-O strips bare checks)."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")


def dyadic_period(turnover: int, alpha: Fraction) -> Fraction:
    value = alpha
    while value > turnover:
        value /= 2
    while value * 2 <= turnover:
        value *= 2
    return value


def explicit_days(period: Fraction, horizon: int) -> set[int]:
    """Generate ceil(k*period), including duplicates before set coalescence."""
    event_count = Fraction(horizon) / period
    require(event_count.denominator == 1, 'event_count.denominator == 1')
    result = set()
    for k in range(1, int(event_count) + 1):
        event = k * period
        result.add((event.numerator + event.denominator - 1) // event.denominator)
    return result


def rank_binary(vectors: list[int]) -> int:
    basis: dict[int, int] = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in basis:
                vector ^= basis[pivot]
            else:
                basis[pivot] = vector
                break
    return len(basis)


def submodular_increments(table: list[Fraction], taus: tuple[int, ...]):
    n = len(taus)
    order = sorted(range(n), key=lambda i: (taus[i], i))
    increments = [Fraction(0)] * n
    prefix = 0
    for i in order:
        old = table[prefix]
        prefix |= 1 << i
        increments[i] = table[prefix] - old
    require(all(a >= 0 for a in increments), 'all(a >= 0 for a in increments)')
    for mask in range(1 << n):
        modular = sum((increments[i] for i in range(n) if mask >> i & 1), Fraction(0))
        require(table[mask] >= modular, 'table[mask] >= modular')
    return increments


def ln_two_upper_bound(terms: int = 45) -> Fraction:
    # log(2)=2*atanh(1/3); the geometric-tail bound is rigorous.
    x = Fraction(1, 3)
    lower = 2 * sum((x ** (2*j+1) / (2*j+1) for j in range(terms)), Fraction(0))
    tail = 2 * x ** (2*terms+1) / ((2*terms+1) * (1-x*x))
    return lower + tail


def as_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def run(max_n: int, max_tau: int, grid_steps: int, seed: int) -> dict:
    rng = random.Random(seed)
    log_upper = ln_two_upper_bound()
    stats = {
        "ordered_turnover_instances": 0,
        "candidate_calendars": 0,
        "individual_cyclic_gap_checks": 0,
        "submodular_cost_instances": 0,
        "exact_cost_equalities": 0,
        "certified_approximation_bounds": 0,
        "continuum_grid_comparisons": 0,
        "saturated_subday_clocks": 0,
    }
    worst = {name: {"ratio": 0.0} for name in ("modular", "coverage", "binary_matroid_rank")}
    grid = [Fraction(grid_steps + j, grid_steps) for j in range(grid_steps)]
    grid_frequencies = [
        [float(min(Fraction(1), 1/dyadic_period(t, alpha))) for t in range(1, max_tau+1)]
        for alpha in grid
    ]
    candidate_cache = {}

    for n in range(1, max_n+1):
        for taus in product(range(1, max_tau+1), repeat=n):
            stats["ordered_turnover_instances"] += 1
            candidates = sorted({Fraction(1)} | {
                Fraction(t, 1 << (t.bit_length()-1)) for t in taus
            })
            weights = [Fraction(rng.randint(1, 11), rng.randint(1, 5)) for _ in taus]
            covers = [(rng.randint(1, (1 << n)-1), Fraction(rng.randint(1, 9), rng.randint(1, 4)))
                      for _ in range(n+2)]
            vectors = [rng.randint(1, 7) for _ in taus]
            tables = {
                "modular": [sum((weights[i] for i in range(n) if mask >> i & 1), Fraction(0))
                            for mask in range(1 << n)],
                "coverage": [sum((weight for cover, weight in covers if cover & mask), Fraction(0))
                             for mask in range(1 << n)],
                "binary_matroid_rank": [Fraction(rank_binary([vectors[i] for i in range(n) if mask >> i & 1]))
                                        for mask in range(1 << n)],
            }
            increments = {name: submodular_increments(table, taus) for name, table in tables.items()}
            lower_bounds = {name: sum((a/t for a, t in zip(inc, taus)), Fraction(0))
                            for name, inc in increments.items()}
            daily_parts = {name: sum((a for a, t in zip(inc, taus) if t == 1), Fraction(0))
                           for name, inc in increments.items()}
            best = {name: None for name in tables}
            best_alpha = {}
            stats["submodular_cost_instances"] += len(tables)

            for alpha in candidates:
                cache_key = (taus, alpha)
                if cache_key not in candidate_cache:
                    periods = [dyadic_period(t, alpha) for t in taus]
                    common = max(periods)
                    require(common.denominator == 1, 'common.denominator == 1')
                    horizon = int(common)
                    require(1 <= horizon <= max(taus), '1 <= horizon <= max(taus)')
                    days = [explicit_days(p, horizon) for p in periods]
                    candidate_cache[cache_key] = (periods, horizon, days)
                periods, horizon, days = candidate_cache[cache_key]
                stats["candidate_calendars"] += 1

                for t, p, visits in zip(taus, periods, days):
                    require(visits, 'visits')
                    ordered = sorted(visits)
                    gaps = [b-a for a, b in zip(ordered, ordered[1:]+[ordered[0]+horizon])]
                    require(max(gaps) <= t, (taus, alpha, p, gaps))
                    require(Fraction(len(visits), horizon) == min(Fraction(1), 1/p), 'Fraction(len(visits), horizon) == min(Fraction(1), 1/p)')
                    for day in range(1, horizon+1):
                        floor_test = Fraction(day) // p > Fraction(day-1) // p
                        require((day in visits) == floor_test, '(day in visits) == floor_test')
                    stats["individual_cyclic_gap_checks"] += 1
                    stats["saturated_subday_clocks"] += int(p < 1)

                order = sorted(range(n), key=lambda i: (taus[i], i))
                require(all(days[j] <= days[i] for i, j in zip(order, order[1:])), 'all(days[j] <= days[i] for i, j in zip(order, order[1:]))')
                masks = [sum(1 << i for i in range(n) if day in days[i]) for day in range(1, horizon+1)]

                for name, table in tables.items():
                    direct = sum((table[mask] for mask in masks), Fraction(0)) / horizon
                    formula = sum((a * min(Fraction(1), 1/p)
                                   for a, p in zip(increments[name], periods)), Fraction(0))
                    require(direct == formula, (name, taus, alpha, direct, formula))
                    stats["exact_cost_equalities"] += 1
                    if best[name] is None or direct < best[name]:
                        best[name] = direct
                        best_alpha[name] = alpha

            for name, incumbent in best.items():
                lower = lower_bounds[name]
                mandatory = daily_parts[name]
                # This is stronger than checking a rounded numerical 1/log(2).
                require((incumbent-mandatory) * log_upper <= lower-mandatory, '(incumbent-mandatory) * log_upper <= lower-mandatory')
                require(incumbent >= lower, 'incumbent >= lower')
                stats["certified_approximation_bounds"] += 1
                inc_float = [float(a) for a in increments[name]]
                grid_min = min(sum(a * frequencies[t-1] for a, t in zip(inc_float, taus))
                               for frequencies in grid_frequencies)
                require(float(incumbent) <= grid_min + 1e-11, 'float(incumbent) <= grid_min + 1e-11')
                stats["continuum_grid_comparisons"] += 1
                ratio = float(incumbent/lower) if lower else 1.0
                if ratio > worst[name]["ratio"]:
                    worst[name] = {
                        "ratio": ratio,
                        "turnovers": list(taus),
                        "selected_alpha": as_text(best_alpha[name]),
                        "cost": as_text(incumbent),
                        "lower_bound": as_text(lower),
                    }

    sharpness = []
    for exponent in range(13):
        M = 1 << exponent
        lower = sum((Fraction(1, q) for q in range(M, 2*M)), Fraction(0))
        # Check every breakpoint through M=128, then representative endpoints
        # and interior breakpoints; the algebraic formula is exact for all r.
        rs = range(M, 2*M) if M <= 128 else sorted({M, M+1, 5*M//4, 3*M//2, 7*M//4, 2*M-1})
        for r in rs:
            cost = Fraction(2*(r-M), r) + Fraction(2*M-r, r)
            require(cost == 1, 'cost == 1')
        sharpness.append({
            "M": M,
            "best_global_clock_cost": 1,
            "true_optimum": float(lower),
            "approximation_ratio": float(1/lower),
            "checked_breakpoints": len(rs),
        })
    require(all(a["approximation_ratio"] < b["approximation_ratio"] for a, b in zip(sharpness, sharpness[1:])), 'all(a["approximation_ratio"] < b["approximation_ratio"] for a, b in zip(sharpness, sharpness[1:]))')
    require(sharpness[-1]["approximation_ratio"] < 1/math.log(2), 'sharpness[-1]["approximation_ratio"] < 1/math.log(2)')

    return {
        "status": "PASS",
        "checker": "independent_calendar_check.py",
        "independence": "Written from theorem notes; does not import or inspect the production implementation.",
        "parameters": {"max_clients": max_n, "max_turnover": max_tau,
                       "alpha_grid_steps": grid_steps, "seed": seed},
        "arithmetic": "fractions.Fraction for all calendar, cost, lower-bound and sharpness equalities; rigorous rational upper bound on log(2) for approximation certification; floating point only for auxiliary grid comparison and displayed ratios.",
        "statistics": stats,
        "worst_observed_cost_to_lower_bound": worst,
        "global_clock_sharpness_family": sharpness,
        "limits": "Finite checks support but do not prove the theorem. The sharpness family constrains the specified global-clock family, not all algorithms. Grid comparisons are auxiliary and do not substitute for the exact breakpoint proof.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--max-tau", type=int, default=8)
    parser.add_argument("--grid-steps", type=int, default=128)
    parser.add_argument("--seed", type=int, default=20261031)
    parser.add_argument("--output", type=Path, default=None,
                        help="output file (default: OUT/independent_checks.json)")
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[1]/"data",
                        help="output directory (default: bundle data/)")
    args = parser.parse_args()
    if args.output is None:
        args.output = args.out / "independent_checks.json"
    result = run(args.max_n, args.max_tau, args.grid_steps, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(args.output), **result["statistics"]}))


if __name__ == "__main__":
    main()
