# Assurance boundary

## What was done

1. **Written proofs** of every theorem in [paper/integer_calendar_replenishment.pdf](paper/integer_calendar_replenishment.pdf) (source: the `.md` file).
2. **Exact certificates.** Small-tree, broom and coverage optima carry attaining cycles and integer potentials. The Theorem 9 bounds are recomputed in exact rational arithmetic, including all 15,374 divisor chains with elements up to 511. The verifiers use only the Python standard library and raise errors instead of using `assert`, so they also run under `python -O`.
3. **Internal AI-assisted review.** Five simulated reviewers, an outside-model adversarial correctness review, a clean replay, a re-review and two separate proof audits of the new results. Each audit recomputed the certified numbers with its own code. No correctness error was found in any theorem. The findings and responses are in [review/REVIEW_SUMMARY.md](review/REVIEW_SUMMARY.md).
4. **Replay.** `verification/run_verification.py` verifies the shipped certificates, regenerates everything into a separate directory and compares the results, and runs 13 semantic negative controls under normal and `-O` execution. A clean replay from the frozen archive is recorded in [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md). CI repeats the exact checks on Linux.
5. **Citations.** Every DOI was resolved and matched to its registry record ([CITATION_AUDIT.md](CITATION_AUDIT.md)).

## What was not done

- No human specialist review or journal peer review. No independent reproduction by an unaffiliated party. No proof-assistant formalisation.
- **Priority is not claimed.** The 2025 Hermansen MSc thesis could not be obtained. Several precedents (Han–Lin distance-constrained scheduling, Chan–Chin, Roundy 1989) were checked through their metadata or abstracts only ([novelty/](novelty/)).
- All instances are synthetic. Nothing estimates operational savings.

Agreement between AI reviewers is not independent evidence. All review here was internal AI-assisted checking.
