# Verification record (release 1.0.0-candidate)

**Every listed finite check and exact certificate reproduced. The general mathematical results have complete informal proofs; no proof-assistant verification was carried out.** Historical priority and operational effectiveness are separate questions that remain unresolved.

Date: 31 October 2026. `python -B verification/run_verification.py` exited successfully. It verified every shipped certificate as released (normal and `-O`), regenerated every computation into `logs/replay/<run>/`, found no mismatch in optimum values or counts, and confirmed that 13 corrupted certificates are rejected under both normal and `-O` execution (26 rejections) while the pristine copies are accepted. Commands, versions, timings and outputs are in `logs/verification_run.json` and the replay directory. No check relies on `assert`.

## Claims and evidence

| Manuscript claim | Analytical evidence | Computational evidence | Status and limit |
|---|---|---|---|
| Theorem 1: feasible integer calendar and 1/ln 2 bound | Greedy submodular lower bound; nested ceiling calendars; exact log-uniform integral; finite sweep; integer common period | Independent checker: 4,680 turnover tuples, 11,566 candidate calendars, 14,040 submodular cost tables | Informal proof, audited; finite checks passed |
| Theorem 2: exact two-edge optimum | Partition at lower-edge visits; minimise over gap endpoints | 532 numerical state-model optima; 3,120 exact all-gap comparisons | Proof complete; numerical checks supplementary |
| Theorem 3: frequency bound attained exactly under positive-edge divisibility | Arithmetic progressions at equality; explicit construction; positive two-edge gap | 750 random structural cases, 558 equality calendars; all 192 benchmark predictions agree | Zero-cost edges checked; complexity of general trees open |
| Theorem 4: pooled pair lower bound | Nonnegative split of each edge's cost across pair and singleton bounds | Rationally checked allocations; exact in 191/192 benchmark instances | Every returned allocation feasible; LP optimality not needed |
| Theorem 5: coverage equality | Intersection of progressions; per-client lcm criterion; explicit calendar | 100 exact finite-state optima: 58 equalities, 42 strict gaps | Explicit weighted coverages only |
| Theorem 6: harmonic-ladder barrier | Unit-cost consecutive-turnover stars; density bound from integer ratios | Finite star checks, dyadic family to M=4096 | Policy-class barrier, not approximation hardness |
| Theorem 7, eq. (29): price of a global cycle at most the largest turnover | Cyclic visit counts; common-M cycle; Theorem 1 | 110 exhaustive binary-cycle count cases; exact finite stars | Supremum, approached but not attained |
| Corollary 2: analysis of the algorithm tight on trees | epsilon-trunk added to the witness stars | Follows from the Theorem 7 counts | Analytical |
| Theorem 8: full cycle-budget profile on the witness family | Exact ceiling count, integral identity, monotone left-Riemann error | 3,464 finite-period and 3,464 budget cases | Specific star family only |
| Theorem 9(a): constant-gap chain mixtures, 12/7, 48/29 and below 1.60139 | Lemma 3 (chain calendars are feasible, constant-gap, prefix-structured); Lemma 4 (tail envelope) | `verify_constant_gap_chains.py`: exact rational maxima over all q below the largest top, plus all tail left limits; envelope confirmed on large integers | Exact finite certificate; weights proposed by LP, bounds recomputed exactly |
| Theorem 9(b): any pairwise-dividing constant-gap calendar costs at least 1.60010 x OPT on an explicit 17-leaf star | Reduction of harmonic period sets to divisor chains | All 15,374 divisor chains with elements at most 511 enumerated in exact arithmetic; count checked by an independent recursion | Exact finite certificate; covers harmonic (pairwise-dividing) periods only |
| Remark: OPT_T / L_T reaches 3780/3139 (about 1.204) on brooms | Theorem 1 gives the upper bound 1/ln 2 | 4 broom optima (M=2,3,4,5) with exact potential certificates, checked by `verify_exact_certificates.py --certificates data/broom_exact_certificates.json` | Lower bound on the supremum only |

## Exact optimum certificates

The benchmark uses 192 original tree instances, independently converted to finite age-state graphs. A numerical circulation solver locates a candidate cycle. For an alleged mean a/b, an integer potential h is checked on every transition u -> v:

`h(u) - h(v) <= b * transition_cost - a`.

Summing around a cycle proves its mean cannot be smaller than a/b. A supplied cycle attains a/b exactly. Thus a successful certificate does not depend on the solver's floating-point claim of optimality.

The standalone standard-library verifier checked:

- 192 optimum certificates;
- 48,979 integer transition inequalities;
- 1,873 steps in attaining cycles;
- 51 nonzero rational pair allocations.

Every feasible periodic regime is reachable after an all-client visit and a transient of at most the largest turnover. Smaller initial ages preserve feasibility, and the original regime's ages are recovered after every client has been served. The state-space restriction therefore does not discard a better periodic schedule.

All 100 coverage cases also retain full exact certificates. Their separate standard-library verifier reconstructs the coverage graph without importing the generator or numerical libraries. It checks 115,378 integer transition inequalities, 549 attaining-cycle steps and 348 individual cyclic maximum gaps. It returns 58 lower-bound equalities and 42 strict gaps, agreeing with the analytical criterion. Running Python with `-S` succeeds, so site packages are unnecessary for this check.

## Comparative results

| Measure | Original dyadic | Single calendar | Independent depot branches |
|---|---:|---:|---:|
| Mean cost / exact optimum | 1.170888 | 1.037547 | 1.004514 |
| Median ratio | 1.106203 | 1 | 1 |
| Largest ratio | 1.5 | 1.25 | 1.14 |
| Exact optima attained | 61 | 122 | 179 |

These are synthetic examples with two to four clients and turnovers at most six, using a fixed seed and explicitly constructed cases. They are not representative field data. The independent-branch construction can have a global cycle longer than the largest turnover.

The pair relaxation's one gap is retained: parents (0,1,1,3), lengths (6,7,2,1), turnovers (4,5,5,3). Its elementary bound is 44/5, pooled bound 48/5, and exact optimum 10. The new calendar is optimal there. This disproves any unqualified claim that the pair relaxation is always exact.

## Independence and inspection boundary

The independent calendar checker was written from the theorem notes before its author inspected the production implementation. The finite-state benchmark uses the original age constraints and daily rooted tours, independently of the edge-frequency formulas. The coverage audit builds its own model but reuses cycle and potential routines from the tree benchmark; the coverage certificates also have a separate standard-library verifier. The constant-gap verifier shares no code with its generator. All code was written within one AI-assisted session. Five AI reviewer agents and a separate AI model carried out an internal review of the pre-release draft (see `review/REVIEW_SUMMARY.md`). This is not external peer review.

## Missing evidence and modelling assumptions

- The Spring 2025 Hermansen MSc thesis (DTU) is listed on a supervisor's page, but its text could not be obtained: there is no Crossref, arXiv or Semantic Scholar record, and the DTU catalogues were not accessible to automated search. Its contents are unknown.
- Han and Lin (1992) and Han, Lin and Hou (1996) on distance-constrained scheduling, Chan and Chin (1992, 1993), and Roundy (1989) were checked at the level of their metadata or abstracts, not their full texts. They are credited as precedent.
- The original Han–Tyan paper was not inspected. Its algorithm was inspected in a published reproduction (Díaz-Ramírez et al. 2013).
- There are no field observations or estimated savings. All instances are synthetic.
- Costs are normalised, monotone and submodular. Capacity, daily working-time limits and travel-time feasibility are outside the model.
- The theorems allow Steiner vertices. The benchmark places a client at every vertex other than the depot.

## Sanity checks

Path with lengths (1,2) and turnovers (2,3): the three-day calendar costs 0+2+6=8, an average of 8/3. This equals the two-edge optimum and exceeds the frequency bound 7/3 by 1/3.

Four-leaf unit-cost star with turnovers (4,5,6,7): the optimum is 319/420. Every cycle of at most seven days costs at least 1, and 420/319 is about 1.3166, below 1/ln 2.

Two constant-gap ladders (1,2,4,...) and (1,3,6,...) with probabilities 4/7 and 3/7: for turnover 2 the expected ratio is 4/7·1 + 3/7·2 = 10/7, and the worst case over all turnovers is 12/7.
