# Priority addendum for release 1.0.0-candidate (31 October 2026)

This addendum records the prior-art checks made during the internal review of the pre-release draft. It supplements
`novelty_report.md` and `structural_prior_art.md` and does not replace them.

## The 2025 DTU thesis (Hermansen)

- A supervisor's page (people.compute.dtu.dk/~phbi/people.html, fetched 31 Oct 2026) lists "Approximation
  Algorithms for Replenishment Problems with Fixed Turnover Times, Spring 2025. Hans Henrik Hermansen,
  Technical University of Denmark, DTU Compute MSc Thesis. Joint with Inge Li Gørtz." There is no link to a
  text. The co-supervisor's page does not link one either.
- A Crossref bibliographic query on the title returns only Bosman et al. (2018, 2022). The arXiv API returns
  only arXiv:1712.05218. Web searches for the author name together with the topic found nothing.
- DTU Findit and DTU Orbit present a bot-verification wall to automated access. It was not bypassed.
- Outcome: the thesis could not be read, and its contents are unknown. It remains a disclosed priority
  uncertainty. The most direct way to settle it would be a request to the supervisors or a library request.

## Other sources checked in this round

| Source | What was found | Bearing |
|---|---|---|
| Bosman (2019) PhD thesis, VU Amsterdam (open full text, ir.cwi.nl/pub/29320), Chapter 3 | Same factor 2 on trees (power-of-two rounding, periodic outputs) and the same open question; no logarithmic shift, no 1/ln 2 | No pre-emption; now cited |
| Bosman and Olver (IPCO 2020) | O(log log) for general metrics via inventory routing | No tree constant; now cited |
| Semantic Scholar forward citations of Bosman et al. 2022 (9 citing works: pinwheel variants, polyamorous scheduling, bamboo trimming, perpetual maintenance, inventory allocation, complexity of inventory routing) | None improves the factor 2 or studies the min-avg cost objective | No pre-emption |
| Multilevel aggregation and joint replenishment with deadlines (Becchetti et al. 2009; Bienkowski et al. 2015, 2020; Nonner and Souza 2009) | Factor 2 on trees and 1.574 on depth-2 trees over finite horizons, pseudo-polynomial in the compact encoding (abstracts or reviewer reading) | Weaker than 1/ln 2; now cited |
| Roundy (1985, 1989); Chan and Chin (1992, 1993); Liu and Layland (1973); Holte et al. (1989); Kawamura (2024) | Classical origin of the 1/ln 2 constant (lot sizing) and of the octave witness family (pinwheel single-integer reduction, rate-monotonic bound) | Credited as precedent for Theorems 1 and 6 |
| Fujiwara, Miyagi and Ouchi (2026), "Pinwheel scheduling with real periods" (abstract) | Real-period pinwheel (attributed to Kawamura): a task of real period a is served at least l times in every ceil(l a) consecutive days | Close precedent for rounding real clocks to integer days; credited |
| Han and Lin (1992); Han, Lin and Hou (1996), distance-constrained scheduling | Base-times-power-of-two specialisation with integer slots and maximum distances (metadata; full texts paywalled) | Possible precedent for the integer-slot realisation; disclosed as not inspected |

## Constant-gap results (new in this release)

Searches for a sub-2 or a lower-bound result for constant-gap (periodic) outputs in this model found nothing
beyond Bosman et al.'s factor 2. Randomising over integer harmonic ladders is a natural idea with pinwheel
analogues (Chan and Chin's double-integer reduction), but no source found states the 1.600–1.601 bracket or
the 12/7 and 48/29 mixtures for the cost objective. This is a bounded negative search, not proof of novelty.
