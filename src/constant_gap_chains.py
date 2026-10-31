"""Propose certificates for constant-gap harmonic calendars (Theorem 9).

A divisor chain 1 = c_0 | c_1 | ... | c_k = t (each ratio an integer >= 2),
continued by doubling beyond t, serves a client of turnover q every c(q) days,
where c(q) is the largest chain element <= q. Upper bound: a probability vector
over chains whose expected ratio q/c(q) is at most RHO_UP for every integer q.
Lower bound: weights y_q on a unit-cost star such that every harmonic integer
period assignment costs at least RHO_LOW times the frequency bound.
SciPy/HiGHS only proposes weights. They are rounded to rationals, and every
reported bound is recomputed exactly by verification/verify_constant_gap_chains.py.

Usage: python src/constant_gap_chains.py [--out DIR] [--upper-cap N] [--lower-cap Q]
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]


def all_chains(N):
    out = []
    stack = [[1]]
    while stack:
        ch = stack.pop()
        out.append(tuple(ch))
        t = ch[-1]
        for m in range(2, N // t + 1):
            stack.append(ch + [t * m])
    return out


def c_trunc(ch, q):
    best = 1
    for c in ch:
        if c <= q:
            best = c
    return best


def c_tail(ch, q):
    t = ch[-1]
    if q < t:
        return c_trunc(ch, q)
    v = t
    while 2 * v <= q:
        v *= 2
    return v


def octave_ratio(a, b):
    r = F(a, b)
    while r >= 2:
        r /= 2
    while r < 1:
        r *= 2
    return r


def tail_left_limit(tD, t):
    r = octave_ratio(tD, t)
    return F(2) if r == 1 else r


def upper(N):
    chains = {}
    for ch in all_chains(N):
        ch = list(ch)
        while 2 * ch[-1] <= N:
            ch.append(2 * ch[-1])
        chains[tuple(ch)] = None
    chains = list(chains)
    T = max(ch[-1] for ch in chains)
    tops = sorted({ch[-1] for ch in chains})
    rows = [[q / c_tail(ch, q) for ch in chains] for q in range(1, T + 1)]
    rows += [[float(tail_left_limit(tD, ch[-1])) for ch in chains] for tD in tops]
    A = np.array(rows)
    m, n = A.shape
    res = linprog(np.r_[np.zeros(n), 1], A_ub=np.hstack([A, -np.ones((m, 1))]), b_ub=np.zeros(m),
                  A_eq=np.r_[np.ones(n), 0][None, :], b_eq=[1], bounds=[(0, None)] * (n + 1), method='highs')
    if not res.success:
        raise SystemExit(f'upper LP failed: {res.message}')
    x = [F(v).limit_denominator(10 ** 6) if v > 1e-9 else F(0) for v in res.x[:n]]
    s = sum(x)
    return [{'weight': str(w / s), 'chain': list(ch)} for w, ch in zip(x, chains) if w > 0], res.fun


def lower(Q):
    chains = all_chains(Q)
    A = np.array([[q / c_trunc(ch, q) for q in range(1, Q + 1)] for ch in chains])
    m, n = A.shape
    res = linprog(np.r_[np.zeros(n), -1], A_ub=np.hstack([-A, np.ones((m, 1))]), b_ub=np.zeros(m),
                  A_eq=np.r_[np.ones(n), 0][None, :], b_eq=[1], bounds=[(0, None)] * (n + 1), method='highs')
    if not res.success:
        raise SystemExit(f'lower LP failed: {res.message}')
    y = [F(v).limit_denominator(10 ** 6) if v > 1e-9 else F(0) for v in res.x[:n]]
    s = sum(y)
    return {str(q + 1): str(w / s) for q, w in enumerate(y) if w > 0}, -res.fun


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out', type=Path, default=ROOT / 'data')
    parser.add_argument('--upper-cap', type=int, default=256)
    parser.add_argument('--lower-cap', type=int, default=512)
    args = parser.parse_args(argv)
    simple = [{'weight': '12/29', 'chain': [1, 3, 6]}, {'weight': '10/29', 'chain': [1, 2, 4, 8]},
              {'weight': '5/29', 'chain': [1, 5]}, {'weight': '2/29', 'chain': [1, 4, 8]}]
    two = [{'weight': '4/7', 'chain': [1, 2]}, {'weight': '3/7', 'chain': [1, 3]}]
    mix, lp_up = upper(args.upper_cap)
    star, lp_lo = lower(args.lower_cap)
    record = {'two_chain_mixture': two, 'four_chain_mixture': simple,
              'certified_mixture': {'cap': args.upper_cap, 'lp_value': lp_up, 'support': mix},
              'lower_bound_star': {'cap': args.lower_cap, 'lp_value': lp_lo, 'leaf_weights_y': star},
              'note': 'Weights proposed numerically; all bounds are recomputed exactly by '
                      'verification/verify_constant_gap_chains.py.'}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'constant_gap_chain_certificates.json').write_text(json.dumps(record, indent=1) + '\n')
    print(json.dumps({'upper_lp': lp_up, 'support': len(mix), 'lower_lp': lp_lo, 'star_leaves': len(star)}))


if __name__ == '__main__':
    main()
