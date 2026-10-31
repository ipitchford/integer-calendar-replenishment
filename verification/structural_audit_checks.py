#!/usr/bin/env python3
"""Secondary audit of production code against the independent construction."""

import argparse
from fractions import Fraction as F
from itertools import product
import json
from math import lcm
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from independent_calendar_check import dyadic_period as independent_period
from replenishment import optimise_calendar, TreeInstance, paired_lower_bound, two_edge_optimum


def require(condition, message):
    """Explicit check that stays active under python -O (-O strips bare checks)."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")


def run(out=ROOT / "data"):
    rng = random.Random(20261101)
    sweep_cases = 0
    pair_cases = 0
    tree_cases = 0
    equality_schedules = 0
    positive_gaps = 0
    for n in range(1, 5):
        for tau in product(range(1, 9), repeat=n):
            weights = [F(rng.randint(0, 15), rng.randint(1, 5)) for _ in tau]
            candidates = sorted({F(1)} | {F(t, 1 << (t.bit_length()-1)) for t in tau})
            brute = []
            for alpha in candidates:
                periods = [independent_period(t, alpha) for t in tau]
                brute.append((sum((w*min(F(1), 1/p) for w, p in zip(weights, periods)), F(0)), alpha))
            expected_cost, expected_alpha = min(brute)
            actual = optimise_calendar(tau, weights)
            require((actual.cost, actual.alpha) == (expected_cost, expected_alpha), '(actual.cost, actual.alpha) == (expected_cost, expected_alpha)')
            require(actual.periods == tuple(independent_period(t, expected_alpha) for t in tau), 'actual.periods == tuple(independent_period(t, expected_alpha) for t in tau)')
            sweep_cases += 1

    for a in range(1, 17):
        for b in range(a, 41):
            for u, v in [(0, 1), (1, 0), (1, 1), (2, 7), (11, 3), (F(2, 3), F(4, 5))]:
                block_optimum = min((F(u*((d+a-1)//a)+v, d) for d in range(1, b+1)))
                require(two_edge_optimum(a, b, u, v) == block_optimum, 'two_edge_optimum(a, b, u, v) == block_optimum')
                pair_cases += 1

    for _ in range(750):
        n = rng.randint(1, 8)
        parents = tuple(rng.randrange(i+1) for i in range(n))
        lengths = tuple(F(rng.randint(0, 8), rng.randint(1, 4)) for _ in range(n))
        tau = tuple(rng.randint(1, 6) for _ in range(n))
        tree = TreeInstance(parents, lengths, tau)
        q = tree.edge_turnovers()
        w = [2*c for c in lengths]
        baseline = sum((weight/t for weight, t in zip(w, q)), F(0))
        certificate = paired_lower_bound(tree)
        allocated = [F(0)] * n
        penalty = F(0)
        for item in certificate["witness"]:
            i, j = item["ancestor"], item["descendant"]
            z, u, v = F(item["penalty"]), F(item["ancestor_allocation"]), F(item["descendant_allocation"])
            a, b = q[i], q[j]
            m, r = divmod(b, a)
            A, B = F(a-r, a*b), F(r, m*a*b)
            require(z >= 0 and min(A*u, B*v) == z, 'z >= 0 and min(A*u, B*v) == z')
            allocated[i] += u
            allocated[j] += v
            penalty += z
        require(all(0 <= x <= weight for x, weight in zip(allocated, w)), 'all(0 <= x <= weight for x, weight in zip(allocated, w))')
        require(certificate["base"] == baseline, 'certificate["base"] == baseline')
        require(certificate["penalty"] == penalty, 'certificate["penalty"] == penalty')
        require(certificate["bound"] == baseline+penalty, 'certificate["bound"] == baseline+penalty')
        cal = tree.calendar()
        require(certificate["bound"] <= cal.cost, 'certificate["bound"] <= cal.cost')
        actual_cal_cost = sum((tree.cost(cal.active(day)) for day in range(1, cal.cycle+1)), F(0))/cal.cycle
        require(actual_cal_cost == cal.cost, 'actual_cal_cost == cal.cost')

        if tree.lower_bound_attainable():
            # Build the exact attaining calendar independently, explicitly
            # allowing zero-cost ancestor and intermediate edges.
            periods = []
            for client in range(n):
                node = client+1
                while node and lengths[node-1] == 0:
                    node = parents[node-1]
                periods.append(q[node-1] if node else 1)
            cycle = lcm(*periods)
            exact_cost = sum((tree.cost(i for i, p in enumerate(periods) if day % p == 0)
                              for day in range(1, cycle+1)), F(0))/cycle
            require(exact_cost == baseline, 'exact_cost == baseline')
            require(certificate["penalty"] == 0, 'certificate["penalty"] == 0')
            equality_schedules += 1
        else:
            require(certificate["penalty"] > 0, 'certificate["penalty"] > 0')
            positive_gaps += 1
        tree_cases += 1

    # For turnovers in one octave, directly optimise the relaxation that only
    # requires each period to divide its maximum. The optimum is attained by
    # the dyadic a/a2 assignment, so this relaxation is exact for that family.
    star_cases = 0
    for M in range(2, 65):
        tau = list(range(M, 2*M))
        total = len(tau)
        for a in tau:
            cost = F(total + sum(t < a for t in tau), a)
            require(cost == 1, 'cost == 1')
        star_cases += 1

    result = {
        "status": "PASS",
        "seed": 20261101,
        "production_vs_independent_sweep_cases": sweep_cases,
        "two_edge_all_gap_comparisons": pair_cases,
        "random_tree_certificate_checks": tree_cases,
        "explicit_equality_calendars_checked": equality_schedules,
        "strict_incompatibility_penalties_checked": positive_gaps,
        "consecutive_star_harmonic_family_checks": star_cases,
        "scope": "Exact rational comparisons except the optional floating-point LP search, whose returned allocation is checked with exact fractions. No claim that these finite checks prove the general theorems.",
    }
    out.mkdir(parents=True, exist_ok=True)
    destination = out / "structural_audit_checks.json"
    destination.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "data", help="output directory (default: bundle data/)")
    run(parser.parse_args().out)
