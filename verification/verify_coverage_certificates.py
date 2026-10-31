"""Verify all stored coverage optimum certificates using the standard library.

The original client turnovers and coverage features determine every state and
transition. No production calendar, benchmark module or optimisation solver is
imported. Integer potential inequalities certify a lower bound on every cycle;
the stored directed cycle certifies an equal achievable cost.

Run from any directory (also under python -O, -I or -S):
    python verify_coverage_certificates.py [--data DIR] [--report PATH]
By default the shipped data/coverage_equality_checks.json is verified and the
JSON report is written to the sibling data folder.
"""
from collections import deque
from fractions import Fraction
from pathlib import Path
import argparse
import json
import math


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    """Keep verification active even if Python is invoked with -O."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")


def coverage_model(turnovers, features, weights):
    """Construct all reachable ages and every feasible daily subset action."""
    n = len(turnovers)
    require(n > 0, "Empty client set")
    require(all(type(t) is int and t >= 1 for t in turnovers),
            "Turnovers must be positive integers")
    require(len(features) == len(weights), "Feature/weight length mismatch")
    require(all(type(f) is int and 0 < f < (1 << n) for f in features),
            "Feature masks must be nonempty client subsets")
    require(all(type(w) is int and w >= 0 for w in weights),
            "Stored benchmark weights must be nonnegative integers")

    actions = [
        (mask, sum(w for feature, w in zip(features, weights) if mask & feature))
        for mask in range(1 << n)
    ]
    states = [(0,) * n]
    index = {states[0]: 0}
    pending = deque([states[0]])
    transitions = []
    while pending:
        state = pending.popleft()
        for mask, cost in actions:
            target = tuple(0 if mask & (1 << i) else state[i] + 1
                           for i in range(n))
            if any(age >= tau for age, tau in zip(target, turnovers)):
                continue
            if target not in index:
                index[target] = len(states)
                states.append(target)
                pending.append(target)
            transitions.append((index[state], index[target], cost, mask))
    return states, transitions


def verify_record(record):
    name = record["id"]
    turnovers = record["turnovers"]
    features = record["feature_masks"]
    weights = record["weights"]
    states, transitions = coverage_model(turnovers, features, weights)
    certificate = record["certificate"]
    optimum = Fraction(record["exact_optimum"])
    require(Fraction(certificate["optimum"]) == optimum and optimum >= 0,
            f"{name}: inconsistent optimum")
    numerator, denominator = optimum.numerator, optimum.denominator
    require(certificate["potential_denominator"] == denominator,
            f"{name}: potential denominator mismatch")
    potential = certificate["potential"]
    require(len(states) == record["states"] == certificate["states"]
            == len(potential), f"{name}: state count mismatch")
    require(len(transitions) == record["arcs"] == certificate["arcs"],
            f"{name}: transition count mismatch")
    require(all(type(value) is int for value in potential),
            f"{name}: potential must be integral")

    # Every feasible periodic regime is reachable from all-zero ages: prepend
    # full service and follow the regime until each client has been served.
    # Summing these inequalities then bounds every feasible periodic mean.
    for source, target, cost, mask in transitions:
        require(potential[source] - potential[target]
                <= denominator * cost - numerator,
                f"{name}: failed integer potential inequality")

    state_ids = certificate["cycle_state_ids"]
    masks = certificate["cycle_actions"]
    require(len(state_ids) > 0 and len(state_ids) == len(masks),
            f"{name}: invalid attaining cycle length")
    require(all(type(i) is int and 0 <= i < len(states) for i in state_ids),
            f"{name}: invalid cycle state index")
    require(all(type(mask) is int and 0 <= mask < (1 << len(turnovers))
                for mask in masks), f"{name}: invalid cycle action")
    transition_by_action = {(source, mask): (target, cost)
                            for source, target, cost, mask in transitions}
    total_cost = 0
    for step, (source, mask) in enumerate(zip(state_ids, masks)):
        require((source, mask) in transition_by_action,
                f"{name}: cycle action is infeasible")
        target, cost = transition_by_action[source, mask]
        require(target == state_ids[(step + 1) % len(state_ids)],
                f"{name}: cycle does not close")
        total_cost += cost
    require(Fraction(total_cost, len(state_ids)) == optimum,
            f"{name}: cycle cost does not attain optimum")

    # Direct cyclic gap checks independently expose an incorrectly interpreted
    # day or action convention, in addition to the state-graph inequalities.
    for client, turnover in enumerate(turnovers):
        days = [day for day, mask in enumerate(masks) if mask & (1 << client)]
        require(bool(days), f"{name}: client omitted from attaining cycle")
        gaps = [right - left for left, right in zip(days, days[1:])]
        gaps.append(days[0] + len(masks) - days[-1])
        require(max(gaps) <= turnover, f"{name}: cyclic maximum gap exceeded")

    lower_bound = Fraction(0)
    client_lcms = [1] * len(turnovers)
    for feature, weight in zip(features, weights):
        if weight == 0:
            continue
        clients = [i for i in range(len(turnovers)) if feature & (1 << i)]
        q = min(turnovers[i] for i in clients)
        lower_bound += Fraction(weight, q)
        for i in clients:
            client_lcms[i] = math.lcm(client_lcms[i], q)
    equality = all(period <= tau for period, tau in zip(client_lcms, turnovers))
    require(client_lcms == record["client_lcms"],
            f"{name}: client LCM mismatch")
    require(lower_bound == Fraction(record["lower_bound"]) <= optimum,
            f"{name}: invalid elementary lower bound")
    require(equality == record["predicted_equality"] == (lower_bound == optimum),
            f"{name}: equality prediction mismatch")
    return len(transitions), len(state_ids), len(turnovers), equality


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=Path, default=ROOT / "data",
                        help="directory holding coverage_equality_checks.json (default: shipped data/)")
    parser.add_argument("--report", type=Path, default=None,
                        help="report path (default: data/coverage_certificate_verification.json)")
    args = parser.parse_args(argv)
    try:
        return verify(args)
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError, AttributeError) as error:
        raise SystemExit(f"CHECK FAILED: malformed certificate ({type(error).__name__}: {error})")


def verify(args):
    source = args.data / "coverage_equality_checks.json"
    data = json.loads(source.read_text())
    records = data["records"]
    require(len(records) == data["summary"]["cases"]
            == data["summary"]["exact_optima_certified"]
            == data["summary"]["complete_certificates_stored"],
            "Certificate record count mismatch")
    require(len({record["id"] for record in records}) == len(records),
            "Duplicate case identifiers")
    inequalities = cycle_steps = gap_checks = equality_cases = 0
    for record in records:
        edges, steps, clients, equality = verify_record(record)
        inequalities += edges
        cycle_steps += steps
        gap_checks += clients
        equality_cases += int(equality)
    require(equality_cases == data["summary"]["equality_cases"],
            "Equality summary mismatch")
    require(len(records) - equality_cases == data["summary"]["strict_gap_cases"],
            "Strict-gap summary mismatch")
    report = {
        "status": "PASS",
        "source": (source.resolve().relative_to(ROOT).as_posix()
                   if source.resolve().is_relative_to(ROOT) else str(source)),
        "exact_optima": len(records),
        "integer_transition_inequalities": inequalities,
        "attaining_cycle_steps": cycle_steps,
        "individual_cyclic_gap_checks": gap_checks,
        "equality_cases": equality_cases,
        "strict_gap_cases": len(records) - equality_cases,
        "solver_required": False,
        "benchmark_module_imported": False,
        "production_module_imported": False,
        "arithmetic": "Integers and fractions.Fraction only",
    }
    output = args.report or ROOT / "data" / "coverage_certificate_verification.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
