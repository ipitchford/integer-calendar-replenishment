"""Exact arithmetic calendar construction for recurring replenishment.

The core algorithm uses the Python standard library only. All costs, periods,
calendar membership decisions and sweep comparisons use fractions.Fraction.
The optional paired_lower_bound function imports scipy only when called.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from typing import Callable, Iterable, Sequence
from math import lcm


def require(condition, message):
    """Explicit internal check that stays active under python -O."""
    if not condition:
        raise RuntimeError(f"CHECK FAILED: {message}")


def dyadic_period(q: int, alpha: F) -> F:
    """Largest alpha * 2**k at most the positive integer q."""
    if not isinstance(q, int) or q < 1 or not (F(1) <= alpha < F(2)):
        raise ValueError("q must be a positive integer and 1 <= alpha < 2")
    p = alpha * (1 << (q.bit_length() - 1))
    return p if p <= q else p / 2


def day_is_active(day: int, period: F) -> bool:
    """Whether ceil(k*period) equals day for some positive integer k."""
    if day < 1 or period <= 0:
        raise ValueError("day and period must be positive")
    return (day * period.denominator // period.numerator
            > (day - 1) * period.denominator // period.numerator)


def frequency(period: F) -> F:
    return min(F(1), 1 / period)


@dataclass(frozen=True)
class Calendar:
    alpha: F
    periods: tuple[F, ...]
    cycle: int
    cost: F
    lower_bound: F
    candidates: tuple[tuple[F, F], ...]

    def active(self, day: int) -> tuple[int, ...]:
        return tuple(i for i, p in enumerate(self.periods)
                     if day_is_active(day, p))

    def as_dict(self) -> dict:
        return {
            "alpha": str(self.alpha),
            "periods": [str(p) for p in self.periods],
            "cycle": self.cycle,
            "cost": str(self.cost),
            "lower_bound": str(self.lower_bound),
            "certified_ratio_to_lower_bound": (
                str(self.cost / self.lower_bound) if self.lower_bound else None),
            "candidates": [{"alpha": str(a), "cost": str(c)}
                           for a, c in self.candidates],
        }


@dataclass(frozen=True)
class BranchCalendar:
    periods: tuple[F, ...]
    cycle: int
    cost: F
    lower_bound: F
    branch_cycles: tuple[int, ...]
    branch_alphas: tuple[F, ...]

    def active(self, day: int) -> tuple[int, ...]:
        return tuple(i for i, p in enumerate(self.periods)
                     if day_is_active(day, p))


def optimise_calendar(turnovers: Sequence[int],
                      chain_weights: Sequence[int | F]) -> Calendar:
    """Minimise sum_i w_i min(1,1/p_i(alpha)) by a breakpoint sweep.

    Weights can be tree edge charges after pairing each edge with the minimum
    descendant turnover, or greedy marginal increments of a submodular cost.
    This does not validate whether an externally supplied set function is
    submodular. Such validation can require exponentially many oracle calls.
    """
    if len(turnovers) != len(chain_weights) or not turnovers:
        raise ValueError("nonempty equally sized turnover and weight lists required")
    if any(not isinstance(q, int) or q < 1 for q in turnovers):
        raise ValueError("positive integer turnovers required")
    weights = tuple(F(w) for w in chain_weights)
    if any(w < 0 for w in weights):
        raise ValueError("nonnegative weights required")
    groups: dict[F, F] = {}
    daily, total = F(0), F(0)
    for q, w in zip(turnovers, weights):
        if q == 1:
            daily += w
        else:
            scale = 1 << (q.bit_length() - 1)
            mantissa = F(q, scale)
            a = w / scale
            groups[mantissa] = groups.get(mantissa, F(0)) + a
            total += a
    crossed = F(0)
    records: list[tuple[F, F]] = []
    for a in sorted({F(1)} | set(groups)):
        cost = daily + (total + crossed) / a
        records.append((a, cost))
        crossed += groups.get(a, F(0))
    alpha, cost = min(records, key=lambda ac: (ac[1], ac[0]))
    periods = tuple(dyadic_period(q, alpha) for q in turnovers)
    cycle = max(periods)
    if cycle.denominator != 1 or cycle > max(turnovers):
        raise AssertionError("breakpoint calendar period theorem violated")
    direct = sum((w * frequency(p) for w, p in zip(weights, periods)), F(0))
    if direct != cost:
        raise AssertionError("sweep and direct calendar costs disagree")
    lower = sum((w / q for w, q in zip(weights, turnovers)), F(0))
    return Calendar(alpha, periods, int(cycle), cost, lower, tuple(records))


def submodular_calendar(turnovers: Sequence[int],
                        cost_oracle: Callable[[frozenset[int]], int | F]):
    """Return calendar and client order for a promised monotone submodular cost.

    Clients use zero-based indices. The returned calendar follows the original
    client order, while its candidate costs use the sorted-chain increments.
    """
    n = len(turnovers)
    if F(cost_oracle(frozenset())) != 0:
        raise ValueError("normalised cost f(empty)=0 required")
    order = sorted(range(n), key=lambda i: (turnovers[i], i))
    prefix: set[int] = set()
    previous = F(0)
    weights = []
    for i in order:
        prefix.add(i)
        current = F(cost_oracle(frozenset(prefix)))
        weights.append(current - previous)
        previous = current
    cal = optimise_calendar([turnovers[i] for i in order], weights)
    original_periods = tuple(dyadic_period(q, cal.alpha) for q in turnovers)
    return Calendar(cal.alpha, original_periods, cal.cycle, cal.cost,
                    cal.lower_bound, cal.candidates), order, weights


@dataclass(frozen=True)
class TreeInstance:
    """Node 0 is the depot; node i+1 has parent parents[i].

    Parents must have smaller node labels, so no graph package is needed.
    Edge lengths and client turnovers are indexed by the child minus one.
    """
    parents: tuple[int, ...]
    lengths: tuple[F, ...]
    turnovers: tuple[int, ...]

    def __post_init__(self):
        n = len(self.parents)
        if n == 0 or len(self.lengths) != n or len(self.turnovers) != n:
            raise ValueError("nonempty equally sized tree fields required")
        if any(not 0 <= p < i + 1 for i, p in enumerate(self.parents)):
            raise ValueError("each parent label must be smaller than its child")
        if any(F(c) < 0 for c in self.lengths):
            raise ValueError("nonnegative edge lengths required")
        if any(not isinstance(q, int) or q < 1 for q in self.turnovers):
            raise ValueError("positive integer turnovers required")

    def edge_turnovers(self) -> tuple[int, ...]:
        q = list(self.turnovers)
        for node in range(len(q), 0, -1):
            parent = self.parents[node - 1]
            if parent:
                q[parent - 1] = min(q[parent - 1], q[node - 1])
        return tuple(q)

    def closure(self, clients: Iterable[int]) -> frozenset[int]:
        """Root-path closure; client indices are zero based."""
        used: set[int] = set()
        for i in clients:
            node = i + 1
            while node:
                used.add(node - 1)
                node = self.parents[node - 1]
        return frozenset(used)

    def cost(self, clients: Iterable[int]) -> F:
        return sum((2 * F(self.lengths[i]) for i in self.closure(clients)), F(0))

    def calendar(self) -> Calendar:
        return optimise_calendar(self.edge_turnovers(), [2 * F(c) for c in self.lengths])

    def branch_calendar(self) -> BranchCalendar:
        """Optimise disjoint depot branches independently; combine at the depot."""
        groups: dict[int, list[int]] = {}
        branch = []
        for i, parent in enumerate(self.parents):
            b = i if parent == 0 else branch[parent - 1]
            branch.append(b)
            groups.setdefault(b, []).append(i)
        q = self.edge_turnovers()
        periods = [F(0)] * len(q)
        cost, lower = F(0), F(0)
        cycles, alphas = [], []
        for clients in groups.values():
            cal = optimise_calendar([q[i] for i in clients],
                                    [2 * F(self.lengths[i]) for i in clients])
            for i, p in zip(clients, cal.periods):
                periods[i] = p
            cost += cal.cost
            lower += cal.lower_bound
            cycles.append(cal.cycle)
            alphas.append(cal.alpha)
        return BranchCalendar(tuple(periods), lcm(*cycles), cost, lower,
                              tuple(cycles), tuple(alphas))

    def ancestor_pairs(self):
        for desc in range(len(self.parents)):
            anc_node = self.parents[desc]
            while anc_node:
                yield anc_node - 1, desc
                anc_node = self.parents[anc_node - 1]

    def lower_bound_attainable(self) -> bool:
        q = self.edge_turnovers()
        return all(q[j] % q[i] == 0
                   for i, j in self.ancestor_pairs()
                   if self.lengths[i] > 0 and self.lengths[j] > 0)


def two_edge_optimum(a: int, b: int, ancestor_weight: int | F,
                     descendant_weight: int | F) -> F:
    """Exact nested two-clock optimum for 1 <= a <= b (weights already doubled)."""
    if not 1 <= a <= b:
        raise ValueError("require 1 <= a <= b")
    u, v = F(ancestor_weight), F(descendant_weight)
    if min(u, v) < 0:
        raise ValueError("nonnegative weights required")
    m, r = divmod(b, a)
    if r == 0:
        return u / a + v / b
    return min(u / a + v / (m * a), ((m + 1) * u + v) / b)


def paired_lower_bound(tree: TreeInstance) -> dict:
    """Optional LP strengthening with a rationally verified feasible witness.

    The floating-point LP selects a witness. Rational reconstruction and an
    exact common rescaling enforce every capacity inequality before the
    reported lower bound is formed. The result is therefore a valid rational
    lower-bound certificate even if the floating-point optimum is inaccurate.
    """
    from scipy.optimize import linprog
    import numpy as np
    q = tree.edge_turnovers()
    weights = tuple(2 * F(c) for c in tree.lengths)
    base = sum((w / t for w, t in zip(weights, q)), F(0))
    pairs = []
    for i, j in tree.ancestor_pairs():
        a, b = q[i], q[j]
        m, r = divmod(b, a)
        if r and weights[i] and weights[j]:
            A, B = F(a - r, a * b), F(r, m * a * b)
            pairs.append((i, j, A, B))
    if not pairs:
        return {"bound": base, "base": base, "penalty": F(0),
                "witness": [], "solver_status": "no incompatible pairs"}
    matrix = np.zeros((len(q), len(pairs)))
    for k, (i, j, A, B) in enumerate(pairs):
        matrix[i, k], matrix[j, k] = float(1 / A), float(1 / B)
    result = linprog(-np.ones(len(pairs)), A_ub=matrix,
                     b_ub=np.array([float(w) for w in weights]),
                     bounds=(0, None), method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    z = [F(max(0.0, float(x))).limit_denominator(10**8) for x in result.x]
    consumed = [F(0) for _ in q]
    for x, (i, j, A, B) in zip(z, pairs):
        consumed[i] += x / A
        consumed[j] += x / B
    shrink = min([F(1)] + [w / c for w, c in zip(weights, consumed) if c])
    z = [x * shrink for x in z]
    consumed = [c * shrink for c in consumed]
    require(all(c <= w for c, w in zip(consumed, weights)), 'all(c <= w for c, w in zip(consumed, weights))')
    penalty = sum(z, F(0))
    witness = [{"ancestor": i, "descendant": j, "penalty": str(x),
                "ancestor_allocation": str(x / A),
                "descendant_allocation": str(x / B)}
               for x, (i, j, A, B) in zip(z, pairs) if x]
    return {"bound": base + penalty, "base": base, "penalty": penalty,
            "witness": witness, "solver_status": result.message}


if __name__ == "__main__":
    import json
    example = TreeInstance((0, 1), (F(1), F(2)), (2, 3))
    cal = example.calendar()
    report = cal.as_dict()
    report["daily_clients_1_based"] = [[i + 1 for i in cal.active(t)]
                                       for t in range(1, cal.cycle + 1)]
    report["daily_tour_costs"] = [str(example.cost(cal.active(t)))
                                  for t in range(1, cal.cycle + 1)]
    report["two_edge_optimum"] = str(two_edge_optimum(2, 3, 2, 4))
    print(json.dumps(report, indent=2))
