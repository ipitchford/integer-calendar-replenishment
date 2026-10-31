# Agent navigation

## Identity

- Release slug: `integer-calendar-replenishment`. Version `1.0.0-candidate`, tag `v1.0.0-candidate`. DOI 10.5281/zenodo.23845965; concept DOI 10.5281/zenodo.23845964.
- Repository: https://github.com/ipitchford/integer-calendar-replenishment. Release page: https://evidencepress.org/releases/integer-calendar-replenishment/
- Scholarly creator: Anonymous. Status: unrefereed candidate ([STATUS.md](STATUS.md)).
- Manuscript: [PDF](paper/integer_calendar_replenishment.pdf), with [Markdown source](paper/integer_calendar_replenishment.md) and [LaTeX](paper/integer_calendar_replenishment.tex). Supplementary notes: [paper/structural_notes.md](paper/structural_notes.md), [paper/coverage_equality_notes.md](paper/coverage_equality_notes.md), [paper/period_budget_notes.md](paper/period_budget_notes.md).
- Machine-readable claims: [CLAIMS.json](CLAIMS.json). Human overview: [README.md](README.md).
- Assurance limits: [ASSURANCE.md](ASSURANCE.md). Review record: [review/REVIEW_SUMMARY.md](review/REVIEW_SUMMARY.md). Claim ledger: [VERIFICATION.md](VERIFICATION.md).
- Prior art: [novelty/](novelty/) (novelty report, structural prior art, priority addendum), [RESEARCH_GATES.json](RESEARCH_GATES.json), [SOURCES.md](SOURCES.md), [CITATION_AUDIT.md](CITATION_AUDIT.md). Provenance: [PROVENANCE.md](PROVENANCE.md).
- Citation: [CITATION.cff](CITATION.cff), [.zenodo.json](.zenodo.json). Licences: [LICENSES.md](LICENSES.md).

## Scientific map

Object: feasible schedules serving each client i at least once in every τ_i consecutive days, with a monotone submodular daily cost f (tree routing: f_T). Comparator: OPT over all repeating schedules. Frequency bound L_f = Σ a_i/τ_i with greedy weights a_i.

- Section 3: Lemma 1 (L_f ≤ OPT); Lemma 2 (rounded clocks ⌈k p_i⌉ are feasible and nested); eqs. (11)–(14), the logarithmic phase average and exact breakpoint sweep; Theorem 1, cost ≤ OPT/ln 2 with cycle ≤ τ_max.
- Section 4: Corollary 1 (trees, improving the factor 2 of Bosman et al.); the three-day example; independent depot branches.
- Section 5: Theorem 2 (exact two-edge optimum); Theorem 3 (divisibility criterion); Theorem 4 (pooled lower bound); the broom remark (OPT/L_T ≥ 1.204); Theorem 5 (coverage lcm criterion).
- Section 6: Theorem 6 (single-ladder barrier); Theorem 7 and eq. (29) (exact short-cycle price 1/ln 2); Corollary 2 (tightness on trees); Theorem 8 (cycle-budget profile).
- Section 7: Lemma 3 (chain calendars); Lemma 4 (tail envelope); Theorem 9 (constant-gap harmonic calendars, 1.60010 ≤ ρ_H ≤ 1.60139).
- Section 8: computations. Section 9: practical reading, limits and open problems.

## Evidence and replay

- Full sequence: `python -B verification/run_verification.py` (record: [logs/verification_run.json](logs/verification_run.json)).
- Standard-library verifiers, assert-free and valid under `-O`: [verification/verify_exact_certificates.py](verification/verify_exact_certificates.py) (192 trees; brooms via `--certificates data/broom_exact_certificates.json`); [verification/verify_coverage_certificates.py](verification/verify_coverage_certificates.py) (100 coverage cases); [verification/verify_constant_gap_chains.py](verification/verify_constant_gap_chains.py) (Theorem 9).
- Generators (NumPy/SciPy propose; results are checked exactly): [src/benchmark_small_trees.py](src/benchmark_small_trees.py), [src/constant_gap_chains.py](src/constant_gap_chains.py), [src/broom_exact.py](src/broom_exact.py), [verification/coverage_equality_check.py](verification/coverage_equality_check.py). Calendar implementation: [src/replenishment.py](src/replenishment.py). Independent checks: [src/independent_calendar_check.py](src/independent_calendar_check.py), [verification/structural_audit_checks.py](verification/structural_audit_checks.py), [verification/short_cycle_budget_check.py](verification/short_cycle_budget_check.py), [verification/pair_mean_cycle_audit.py](verification/pair_mean_cycle_audit.py).
- Negative controls: [verification/negative_controls.py](verification/negative_controls.py) (13 corruptions). CI: [.github/workflows/replay.yml](.github/workflows/replay.yml). Records: [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ENVIRONMENT.txt](ENVIRONMENT.txt). Integrity: [SHA256SUMS](SHA256SUMS).

## Trust boundary

Review was internal and AI-assisted. There was no peer review, no independent reproduction and no formal verification. Priority is not claimed: a 2025 DTU MSc thesis with a closely matching title could not be obtained. The rounding tools, the phase sweep and the constant 1/ln 2 are classical. All instances are synthetic.
