"""Exact verifier for the constant-gap harmonic calendar bounds (Theorem 9).

Standard library only; no assert statements (safe under python -O).
Upper bounds: for a mixture of divisor chains (continued by doubling beyond the
top element t), the expected ratio E[q/c(q)] is computed exactly for every
integer q below the largest top, and for larger q through the exact left
limits of the tail envelope (Lemma 4 of the manuscript). Lower bound: every
divisor chain with elements <= Q is enumerated and its weighted star cost
sum_q y_q q/c(q) is computed exactly; the minimum is the certified lower bound.

Usage: python verify_constant_gap_chains.py [--data DIR] [--report PATH]
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]


def require(cond, msg):
    if not cond:
        raise SystemExit(f'CHECK FAILED: {msg}')


def is_chain(ch):
    return (isinstance(ch, list) and len(ch) >= 1 and ch[0] == 1
            and all(isinstance(c, int) and c >= 1 for c in ch)
            and all(b % a == 0 and b // a >= 2 for a, b in zip(ch, ch[1:])))


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


def mixture_bound(support):
    require(len(support) >= 1, 'empty mixture')
    ws = [F(e['weight']) for e in support]
    chs = [e['chain'] for e in support]
    require(all(w > 0 for w in ws) and sum(ws) == 1, 'weights must be positive and sum to one')
    require(all(is_chain(ch) for ch in chs), 'invalid divisor chain')
    T = max(ch[-1] for ch in chs)
    worst, where = F(0), None
    for q in range(1, T + 1):
        v = sum(w * F(q, c_tail(ch, q)) for w, ch in zip(ws, chs))
        # independent sanity: every chosen period is a feasible, harmonic, constant gap
        require(all(1 <= c_tail(ch, q) <= q for ch in chs), 'period exceeds turnover')
        if v > worst:
            worst, where = v, f'q={q}'
    for tD in sorted({ch[-1] for ch in chs}):
        v = sum(w * (F(2) if octave_ratio(tD, ch[-1]) == 1 else octave_ratio(tD, ch[-1]))
                for w, ch in zip(ws, chs))
        if v > worst:
            worst, where = v, f'tail left limit at log2({tD})'
    # cross-check the tail envelope on explicit large integers just below each breakpoint
    for tD in sorted({ch[-1] for ch in chs}):
        for k in (6, 10):
            q = tD * 2 ** k - 1
            if q >= T:
                v = sum(w * F(q, c_tail(ch, q)) for w, ch in zip(ws, chs))
                require(v <= worst, 'integer tail value exceeds envelope bound')
    return worst, where


def all_chains(N):
    out, stack = [], [[1]]
    while stack:
        ch = stack.pop()
        out.append(ch)
        t = ch[-1]
        for m in range(2, N // t + 1):
            stack.append(ch + [t * m])
    return out


def star_bound(weights):
    ys = {int(q): F(v) for q, v in weights.items()}
    require(all(q >= 1 for q in ys) and all(v > 0 for v in ys.values()), 'invalid star weights')
    require(sum(ys.values()) == 1, 'star weights must sum to one (frequency bound normalised to 1)')
    Q = max(ys)
    best, arg, count = None, None, 0
    for ch in all_chains(Q):
        count += 1
        v = sum(y * F(q, c_trunc(ch, q)) for q, y in ys.items())
        if best is None or v < best:
            best, arg = v, ch
    # completeness: compare with an independent divisor-recursion count of all chains <= Q
    ending = {1: 1}
    for t in range(2, Q + 1):
        ending[t] = sum(ending[d] for d in range(1, t // 2 + 1) if t % d == 0)
    require(count == sum(ending.values()), 'chain enumeration is incomplete')
    return best, arg, count, Q


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--data', type=Path, default=ROOT / 'data')
    parser.add_argument('--report', type=Path, default=ROOT / 'logs' / 'constant_gap_chain_verification.json')
    args = parser.parse_args(argv)
    try:
        rec = json.loads((args.data / 'constant_gap_chain_certificates.json').read_text())
        two, w2 = mixture_bound(rec['two_chain_mixture'])
        four, w4 = mixture_bound(rec['four_chain_mixture'])
        up, wup = mixture_bound(rec['certified_mixture']['support'])
        lo, lo_chain, nchains, Q = star_bound(rec['lower_bound_star']['leaf_weights_y'])
    except (KeyError, TypeError, ValueError, ZeroDivisionError, AttributeError) as error:
        raise SystemExit(f'CHECK FAILED: malformed certificate ({type(error).__name__}: {error})')
    require(two == F(12, 7), f'two-chain bound is {two}, expected 12/7')
    require(four == F(48, 29), f'four-chain bound is {four}, expected 48/29')
    require(lo <= up, 'lower bound exceeds upper bound')
    require(up <= F('1.60139'), f'certified upper bound {float(up)} exceeds the stated 1.60139')
    require(lo >= F('1.60010'), f'certified lower bound {float(lo)} is below the stated 1.60010')
    # 1/ln 2 < 1.4427 < lower bound, so the harmonic constant-gap class is strictly worse
    require(lo > F(14427, 10000), 'lower bound does not exceed 1.4427 > 1/ln 2')
    report = {'status': 'PASS', 'two_chain_bound': str(two), 'four_chain_bound': str(four),
              'certified_upper_bound': str(up), 'certified_upper_bound_float': float(up),
              'upper_support_size': len(rec['certified_mixture']['support']), 'upper_attained_at': wup,
              'certified_lower_bound': str(lo), 'certified_lower_bound_float': float(lo),
              'lower_bound_star_turnovers': sorted(int(q) for q in rec['lower_bound_star']['leaf_weights_y']),
              'chains_enumerated_for_lower_bound': nchains, 'lower_bound_cap': Q,
              'minimising_chain': lo_chain, 'solver_required': False}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
