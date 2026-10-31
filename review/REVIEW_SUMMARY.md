# Internal review summary (rating-free public record)

**What this is.** Before release, the paper had an internal, AI-assisted review. Five simulated reviewers
(editor, methodology, domain, cross-disciplinary perspective and devil's advocate, following the
academic-paper-reviewer protocol) worked independently, a separate AI model gave an adversarial correctness
review, and the lead editor ran a clean replay of every script. A re-review and two proof audits of the new
material followed. This was not external peer review. The original reports are kept privately; their
substantive findings and the responses are recorded here.

## Correctness

No reviewer or audit found an error in any theorem of the pre-release draft. Points of rigour that were
raised and fixed:

- Theorem 2 proof: the average is *at least* a duration-weighted average (extra activations of the upper
  edge only add cost).
- Lemma 2: the gap across the cycle boundary is now stated explicitly.
- Equation (14): the minimum over the phase is attained, not merely an infimum.
- Theorem 6: the case a < M uses the bound M/max(1, a); M ≥ 2 makes a/2 ≥ 1.
- Theorem 7: the class is all P-periodic schedules with P ≤ τ_max, including schedules whose minimal period
  is a divisor of P.
- Theorem 8: the inequality ⌈h⌉ − ⌈h/2⌉ ≤ h, used in the 1/M error bound, is now proved.
- Equation (29): the supremum is approached but not attained.

The new results (Lemmas 3–4, Theorem 9, Corollary 2, the broom remark) were audited separately by a proof
auditor and an outside-model auditor. Both recomputed every certified number independently (including
E[q/c(q)] for every integer q up to 10^6 and a separate enumeration of all 15,374 divisor chains). Neither
found a correctness issue. Two minor points were fixed: a lower bound had been rounded up in one sentence,
and the broom description now mentions the redundant hub client.

## Framing and significance

- *The headline was placed on a restriction the paper had imposed on itself.* The title and abstract now lead
  with the improvement of Bosman et al.'s factor two. Theorem 7 is presented as tightness.
- *The constant-gap output class of Bosman et al. was left unexplored, although reviewers' brute force
  suggested it is strong.* New Section 7 (Theorem 9) addresses it. Mixtures of integer divisor ladders give
  constant-gap algorithms with factor 12/7, 48/29 and ≤ 1.60139. No calendar whose constant gaps divide one
  another can beat 1.60010 in the worst case. Constant gaps that do not divide one another remain open.
- *Sharpness applied only to the output class.* New Corollary 2 shows that the analysis of the full algorithm,
  branch refinement included, is tight on trees.
- *The frequency lower bound was never examined.* A new remark gives exactly certified broom instances, where
  OPT/L_T reaches 3780/3139 ≈ 1.204. Any analysis against L_T alone therefore cannot prove a factor below 1.204.
- *The three-day example's comparison was weak.* The text now says that a constant-gap policy with
  non-dividing periods 2 and 3 also attains the optimum.

## Literature and priority

- Added, with records copied from Crossref, DataCite, arXiv or the repository: Roundy (1985, 1989) as the
  origin of the 1/ln 2 rounding constant; Chan and Chin (1992, 1993), Holte et al. (1989), Liu and Layland
  (1973), Kawamura (2024) and Fujiwara et al. (2026) on pinwheel and real-time scheduling, with the octave
  witness family credited as classical; multilevel aggregation and joint replenishment with deadlines
  (Becchetti et al. 2009; Bienkowski et al. 2015, 2020; Nonner and Souza 2009), with the explanation that those
  routes give weaker factors and are pseudo-polynomial; Cheung et al. (2016) and Nagarajan and Shi (2016); the
  problem's history (LATIN 2018, Bosman's 2019 thesis, Bosman and Olver 2020); periodic maintenance and
  inventory-routing context (Anily et al. 1998; Bar-Noy et al. 2002; Coelho et al. 2014; van Ee 2021;
  Gąsieniec et al. 2024). Han and Lin's distance-constrained scheduling papers are cited as possible precedent
  for the integer-slot realisation; their full texts could not be inspected.
- Bosman's 2019 thesis was read (Chapter 3): it has the same factor two and open question, and no 1/ln 2.
- The 2025 Hermansen MSc thesis could not be obtained by any permitted route (see
  `novelty/priority_addendum_2026-10-31.md`). Its contents are unknown, and this is disclosed in the abstract,
  in Section 1.3 and in Section 9. Priority is not claimed.

## Practical reading and readability

- New plain-language opening, results table, roadmap, terminology paragraph and calendar figure.
- New paragraphs separate three kinds of regularity (short global cycle, constant gaps per client, weekly
  alignment). They also explain peak days (nested calendars put every client on one day; branch offsets can
  spread the load) and say when the model fits.
- The "27.87% reduction" sentence, which compared two worst-case bounds, was removed.

## Reproducibility

- The tree-certificate verifier relied on `assert` and accepted corrupted certificates under `python -O`. Every
  check now raises an explicit error, and 13 semantic corruptions are rejected in both modes.
- The verification driver had regenerated certificates rather than checking the shipped ones. It now verifies
  the shipped files first, regenerates into a separate replay directory, compares optimum values and counts,
  and writes a single run record.
- The benchmark script failed under `python -I`; fixed.

## Not done (stated as open in the paper)

Hardness on trees; the min–max (peak-day) objective; general constant-gap policies; algorithms that use longer
cycles; a large realistic benchmark.
