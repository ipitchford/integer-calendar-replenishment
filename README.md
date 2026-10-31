# Integer calendars for fixed-turnover replenishment

A 1/ln 2 guarantee on trees, the price of short cycles and the price of constant gaps.

Release 1.0.0-candidate (31 October 2026). DOI [10.5281/zenodo.23845965](https://doi.org/10.5281/zenodo.23845965). Repository: https://github.com/ipitchford/integer-calendar-replenishment. Author: Anonymous. Text and data CC0-1.0; code MIT.
`SHA256SUMS` lists the exact released files.

## In plain terms

A depot must revisit each client at least once every few days (the client's *turnover time*) and wants the
long-run average daily routing cost to be low. Bosman et al. (Algorithmica, 2022) gave a calendar costing at
most twice the optimum on tree networks and asked whether the factor two could be improved. This package
shows that it can:

- **Main result (Theorem 1, Corollary 1).** Rounding the event times of real-valued "power-of-two" clocks up
  to whole days, with the clocks' offset chosen by a logarithmic averaging argument, gives a feasible calendar
  costing at most **1/ln 2 ≈ 1.4427** times the optimum. It is computed deterministically in O(n log n) time,
  and the result holds for every monotone submodular daily cost (tree routing is one case).
- **Tightness (Theorem 7, Corollary 2).** The calendar repeats within the longest turnover time. For every
  calendar with that property, 1/ln 2 is the exact worst-case price, and the analysis of the algorithm is tight.
- **Constant gaps (Theorem 9).** The main calendars let a client's gaps alternate (for example 2, 1, 2, 1).
  If every client must keep a constant gap, with the gaps dividing one another (the form of Bosman et al.'s
  output), the best possible worst-case factor lies between **1.6001 and 1.6014**. An explicit four-ladder
  mixture already gives 48/29 ≈ 1.655 < 2.
- **Structure (Theorems 2–5, 8).** The nested two-edge problem is solved exactly; divisibility and
  least-common-multiple criteria say exactly when the standard frequency lower bound is attained; and the
  cost of a longer global cycle is profiled exactly on the worst-case family.

**Priority.** The rounding tools and the constant 1/ln 2 are classical (Roundy 1989; Teo and Bertsimas 2001;
pinwheel scheduling), and they are credited in the paper. A Spring 2025 DTU MSc thesis by H. H. Hermansen,
*Approximation Algorithms for Replenishment Problems with Fixed Turnover Times*, is listed on a supervisor's
page, but its text could not be obtained. Historical priority is therefore **not certified**. See
`novelty/priority_addendum_2026-10-31.md`.

## Main files

- `paper/integer_calendar_replenishment.pdf`: the manuscript. `paper/integer_calendar_replenishment.md`
  is its source.
- `paper/*_notes.md`: supplementary derivations.
- `review/REVIEW_SUMMARY.md`: the internal review of this version, what it found and how each point was
  handled. It was AI-assisted, not external peer review.
- `VERIFICATION.md`: the ledger of claims and checks, with limits.
- `AI_INDEX.md`: a map of the package for automated readers.
- `src/replenishment.py`: the exact-arithmetic calendar implementation and lower-bound certificates.
- `src/constant_gap_chains.py`, `verification/verify_constant_gap_chains.py`: the Theorem 9 certificates
  and their exact standard-library verifier.
- `src/broom_exact.py`: certified optima showing how far the frequency bound can sit below the optimum.
- `data/`: synthetic benchmark inputs and results, and exact optimum certificates. `figures/`: reproducible
  figures. `novelty/`: the prior-art search records.

## Reproduce

Python 3.11 or later. The calendar code and all verifiers use only the standard library. NumPy and SciPy
(versions in `requirements.txt`) are needed to regenerate certificates, and Matplotlib only for the figures.

```bash
python -B verification/run_verification.py
```

This command verifies every shipped certificate as released, under normal and `python -O` execution. It then
regenerates every computation into `logs/replay/<run>/` (shipped `data/` is never overwritten), compares
optimum values and counts with the shipped data, and runs negative controls with corrupted certificates.
It writes `logs/verification_run.json`. The standalone checks are:

```bash
python -S verification/verify_exact_certificates.py      # 192 small-tree optima
python -S verification/verify_coverage_certificates.py   # 100 coverage optima
python -S verification/verify_constant_gap_chains.py     # Theorem 9 bounds (exact rationals)
python verification/negative_controls.py
python src/replenishment.py                               # the three-day example
```

## Evidence and scope

The theorems are proved analytically. The bounds in Theorem 9 and the broom remark rest on finite
certificates in exact rational arithmetic. All instances are synthetic; nothing estimates real-world savings.
No proof-assistant formalisation was made. All checks were written within one AI-assisted session, so
"independent" means separately written code, not independent people.

The model has no vehicle capacity, no daily working-time limit, no holding cost, no lead time and no
stochastic demand. It controls the long-run average, not the busiest day. The short-cycle lower bound does
not rule out better algorithms that use longer cycles.

## Sanity check

Take a path with edge lengths 1 and 2 and client turnovers 2 and 3. The three-day calendar costs 0, 2 and 6
on its three days, an average of exactly 8/3. The power-of-two calendar costs 3, and the frequency bound is
7/3. The exact two-edge theorem raises the lower bound to 8/3, which certifies that the calendar is optimal.
