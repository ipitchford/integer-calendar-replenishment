"""Verify supplied optimum certificates using the standard library only.

No optimisation solver and no production calendar module are imported.
The finite age-state graph is reconstructed from the original tree and client
turnovers, then every integer dual inequality and the attaining cycle is checked.
Every check is an explicit test that remains active under python -O.

Usage: python verify_exact_certificates.py [--data DIR] [--report PATH]
By default the shipped data/small_tree_exact_certificates.json is verified.
"""
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    """Explicit check that stays active under python -O (-O strips bare checks)."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")


def is_int(value):
    return type(value) is int


def model(parents, lengths, taus):
    n = len(taus)
    actions = {}
    for mask in range(1 << n):
        visited = set()
        for i in range(n):
            if mask & (1 << i):
                node = i + 1
                while node:
                    visited.add(node - 1)
                    node = parents[node - 1]
        active_mask = sum(1 << i for i in visited)
        actions[active_mask] = sum(2 * lengths[i] for i in visited)
    actions = sorted(actions.items())
    states = [(0,) * n]
    index = {states[0]: 0}
    pending = deque([states[0]])
    transitions = []
    while pending:
        state = pending.popleft()
        for mask, cost in actions:
            new = tuple(0 if mask & (1 << i) else state[i] + 1 for i in range(n))
            if any(age >= tau for age, tau in zip(new, taus)):
                continue
            if new not in index:
                index[new] = len(states)
                states.append(new)
                pending.append(new)
            transitions.append((index[state], index[new], cost, mask))
    return states, transitions


def check_record(record):
    """Check one stored tree certificate; return (arcs, cycle steps, pair allocations)."""
    name = record.get("id", "?")
    parents, lengths, taus = record["parents"], record["lengths"], record["turnovers"]
    n = len(taus)
    require(n > 0 and len(parents) == n == len(lengths), f"{name}: tree field lengths differ")
    require(all(is_int(p) and 0 <= p <= k for k, p in enumerate(parents)),
            f"{name}: each parent label must be smaller than its child")
    require(all(is_int(c) and c >= 0 for c in lengths), f"{name}: lengths must be nonnegative integers")
    require(all(is_int(t) and t >= 1 for t in taus), f"{name}: turnovers must be positive integers")
    states, arcs = model(parents, lengths, taus)
    cert = record["exact_optimum_certificate"]
    mu = F(cert["optimum"])
    require(mu >= 0, f"{name}: negative optimum")
    potentials = cert["potential"]
    require(all(is_int(h) for h in potentials), f"{name}: potentials must be integers")
    require(len(states) == cert["states"] == len(potentials), f"{name}: state count mismatch")
    require(len(arcs) == cert["arcs"], f"{name}: transition count mismatch")
    require(is_int(cert["potential_denominator"]) and mu.denominator == cert["potential_denominator"],
            f"{name}: potential denominator mismatch")
    # h(u) - h(v) <= b*cost - a on every arc proves that no cycle has mean below a/b.
    for u, v, cost, mask in arcs:
        require(potentials[u] - potentials[v] <= cost * mu.denominator - mu.numerator,
                f"{name}: failed integer potential inequality on arc {u}->{v}")
    lookup = {(u, mask): (v, cost) for u, v, cost, mask in arcs}
    ids, masks = cert["cycle_state_ids"], cert["cycle_actions"]
    require(isinstance(ids, list) and isinstance(masks, list) and len(ids) > 0
            and len(ids) == len(masks), f"{name}: invalid attaining cycle length")
    require(all(is_int(i) and 0 <= i < len(states) for i in ids), f"{name}: cycle state index out of range")
    require(all(is_int(m) and 0 <= m < (1 << n) for m in masks), f"{name}: invalid cycle action")
    total = 0
    for j, (u, mask) in enumerate(zip(ids, masks)):
        require((u, mask) in lookup, f"{name}: cycle step {j} is not a feasible transition")
        v, cost = lookup[u, mask]
        require(v == ids[(j + 1) % len(ids)], f"{name}: attaining cycle does not close at step {j}")
        total += cost
    require(F(total, len(ids)) == mu, f"{name}: cycle mean {F(total, len(ids))} does not attain optimum {mu}")
    # Check the pooled lower-bound witness directly from its exact weights.
    # The q recursion below relies on parent labels being smaller (checked above).
    q = list(taus)
    for node in range(n, 0, -1):
        par = parents[node - 1]
        if par:
            q[par - 1] = min(q[par - 1], q[node - 1])
    used = [F(0) for _ in q]
    penalty = F(0)
    allocations = 0
    for entry in record["paired_lower_bound_witness"]:
        i, j = entry["ancestor"], entry["descendant"]
        require(is_int(i) and is_int(j) and 0 <= i < n and 0 <= j < n, f"{name}: pair index out of range")
        p = parents[j]
        lineage = set()
        while p:
            lineage.add(p - 1)
            p = parents[p - 1]
        require(i in lineage, f"{name}: pair ({i},{j}) is not ancestor/descendant")
        a, b = q[i], q[j]
        m, r = divmod(b, a)
        require(r > 0, f"{name}: pair ({i},{j}) has divisible edge turnovers")
        A, B = F(a - r, a * b), F(r, m * a * b)
        z = F(entry["penalty"])
        u, v = F(entry["ancestor_allocation"]), F(entry["descendant_allocation"])
        require(z >= 0 and A * u == B * v == z, f"{name}: pair ({i},{j}) allocation inconsistent with penalty")
        used[i] += u
        used[j] += v
        penalty += z
        allocations += 1
    require(all(x <= 2 * c for x, c in zip(used, lengths)), f"{name}: pair allocations exceed edge weights")
    require(sum((F(2 * c, t) for c, t in zip(lengths, q)), F(0)) + penalty <= mu,
            f"{name}: pooled lower bound exceeds certified optimum")
    return len(arcs), len(ids), allocations


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=Path, default=ROOT / "data",
                        help="directory holding small_tree_exact_certificates.json (default: shipped data/)")
    parser.add_argument("--certificates", type=Path, default=None,
                        help="explicit certificate file (default: <data>/small_tree_exact_certificates.json)")
    parser.add_argument("--report", type=Path, default=None,
                        help="report path (default: data/certificate_verification.json in the bundle)")
    args = parser.parse_args(argv)
    report_path = args.report or ROOT / "data" / "certificate_verification.json"
    try:
        records = json.loads((args.certificates or args.data / "small_tree_exact_certificates.json").read_text())
        require(isinstance(records, list) and len(records) > 0, "no certificate records")
        ids = [record.get("id") for record in records]
        require(len(set(ids)) == len(ids), "duplicate case identifiers")
        transitions_checked = cycle_steps = pair_allocations = 0
        for record in records:
            arcs, steps, allocations = check_record(record)
            transitions_checked += arcs
            cycle_steps += steps
            pair_allocations += allocations
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise SystemExit(f"CHECK FAILED: malformed certificate ({type(error).__name__}: {error})")
    report = {"status": "PASS", "exact_optima": len(records),
              "integer_transition_inequalities": transitions_checked,
              "attaining_cycle_steps": cycle_steps,
              "rational_pair_allocations": pair_allocations,
              "solver_required": False, "production_module_imported": False}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
