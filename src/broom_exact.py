"""Exactly certified optima of 'broom' trees (Remark on the frequency bound).

A trunk edge of length W joins the depot to a hub; M leaves of length ell hang
from the hub with turnovers M, ..., 2M-1. The hub carries a client of turnover M,
which is served free whenever the trunk is used. The optimum is computed with
the independent age-state model of benchmark_small_trees.py and certified by an
integer potential; the records use the format checked by
verification/verify_exact_certificates.py --certificates <file>.

Usage: python src/broom_exact.py [--out DIR] [M ...]   (default M = 2 3 4)
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from benchmark_small_trees import exact_optimum  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out', type=Path, default=ROOT / 'data')
    parser.add_argument('M', nargs='*', type=int, default=[2, 3, 4])
    args = parser.parse_args(argv)
    records, summary = [], []
    for M in args.M:
        W, ell = M, 2          # round-trip trunk weight 2M, leaf weight 4: trunk/leaf ratio M/2
        parents = [0] + [1] * M
        lengths = [W] + [ell] * M
        turnovers = [M] + list(range(M, 2 * M))
        mu, cert = exact_optimum(parents, lengths, turnovers)
        L = F(2 * W, M) + sum(F(2 * ell, q) for q in range(M, 2 * M))
        records.append({'id': f'broom_M{M}', 'parents': parents, 'lengths': lengths,
                        'turnovers': turnovers, 'exact_optimum_certificate': cert,
                        'paired_lower_bound_witness': []})
        summary.append({'M': M, 'optimum': str(mu), 'frequency_bound_L_T': str(L),
                        'ratio_OPT_over_L_T': str(mu / L), 'ratio_float': float(mu / L),
                        'states': cert['states'], 'arcs': cert['arcs']})
        print(json.dumps(summary[-1]), flush=True)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'broom_exact_certificates.json').write_text(json.dumps(records) + '\n')
    (args.out / 'broom_summary.json').write_text(json.dumps(summary, indent=2) + '\n')


if __name__ == '__main__':
    main()
