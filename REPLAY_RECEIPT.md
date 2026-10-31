# Replay receipt (31 October 2026)

Environment: see [ENVIRONMENT.txt](ENVIRONMENT.txt). Every run started from a fresh copy of the package and wrote only to temporary directories, or (for `run_verification.py`) only under `logs/`. No shipped file outside `logs/` changed.

| Step | Command | Result |
|---|---|---|
| Tree certificates, normal and `-O` | `python3 -B -I -S [-O] verification/verify_exact_certificates.py` | PASS: 192 optima, 48,979 integer transition inequalities, 1,873 attaining-cycle steps, 51 rational pair allocations; identical reports in both modes |
| Broom certificates | `... verify_exact_certificates.py --certificates data/broom_exact_certificates.json` | PASS: 4 optima (M = 2..5), 544,298 inequalities, 42 cycle steps |
| Coverage certificates | `python3 -B -I -S [-O] verification/verify_coverage_certificates.py` | PASS: 100 optima, 115,378 inequalities, 549 cycle steps, 348 cyclic gap checks |
| Constant-gap bounds (Theorem 9) | `python3 -B -I -S [-O] verification/verify_constant_gap_chains.py` | PASS: 12/7 and 48/29 exactly; certified upper bound 1.6013816744…; lower bound 1.6001012546… over 15,374 enumerated chains |
| Negative controls | `python3 -B -I [-O] verification/negative_controls.py` | 13 corruptions, 26 rejections confirmed, 4 pristine acceptances, in both modes |
| Full sequence | `uv run --no-project --with numpy==2.3.5 --with scipy==1.17.0 python3 -B verification/run_verification.py` | PASS: shipped certificates verified first; all generators rerun into `logs/replay/<run>/`; optimum values and counts identical to shipped data (some dual potentials differ, as expected); regenerated chain bounds within the stated bracket; brooms M = 2..4 regenerated identically (M = 5 takes about 30 minutes and is verified from the shipped certificate) |
| Manuscript | Pandoc 3 + LuaLaTeX (TinyTeX, TeX Live 2026) via `src/build_documents.py` | 26 pages; every page inspected; TeX-leak preflight passed |

The broom M = 5 certificate was generated once (about 30 minutes, 25,200 states and 529,785 transitions) and is checked by the standard-library verifier in every replay.
