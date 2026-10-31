# Structural formula audit and cross-disciplinary novelty rerun

**Search and audit date:** 31 October 2026.  
**Final manuscript:** *The price of short cycles in fixed-turnover replenishment: Integer calendars, sharp approximation and exact synchronisation bounds*, Theorems 1–8.  
**Scope:** The two-edge formula, lower-bound equality criteria, harmonic-ladder obstruction, short-cycle obstruction and cycle-budget profile in `paper/integer_calendar_replenishment.md`. This supplements `novelty_report.md`; it does not certify historical priority.

## 1. Decision and material discovery

The formula-level rerun found a **direct algorithmic collision**: the unsaturated harmonic-clock choice and its breakpoint optimisation are the harmonic-specialisation algorithm attributed to Han and Tyan (1997), reproduced as the Sr algorithm in Díaz-Ramírez et al. (2013). They must not be presented as a new rounding formula or a new standalone optimisation algorithm.

No equivalent statement of the integer-event projection theorem, the precise coverage equality criterion, the consecutive-turnover star obstruction, or its full cycle-budget profile was identified in the primary material inspected here. This is **bounded uncertainty**, because the original Han–Tyan paper and the specifically relevant Hermansen 2025 thesis were not fully accessible. A failed exact-string search is not evidence that a theorem was previously unknown.

The strongest remaining contribution unit is therefore the complete integer-calendar theorem and the sharp price of the global restriction `P <= tau_max`, with the structural equality and pairwise bounds as additional results. The standard harmonic sequence, logarithmic constant, greedy submodular lower bound and real-period sweep receive explicit credit.

## 2. Frozen claims and exclusions

### 2.1 Integer calendars

Inputs are positive integer maximum gaps `tau_i` and a normalised monotone submodular daily cost. Repeating schedules may have nonconstant individual gaps. For an optimised `alpha in [1,2)`, use

\[
p_i=\alpha 2^{\lfloor\log_2(\tau_i/\alpha)\rfloor},
\qquad D_i=\{\lceil kp_i\rceil:k\ge1\}.
\]

Repeated events on one day count as one service. The contribution sought is preservation of every integer rolling deadline and of nesting under event projection, followed by a `1/ln 2` cost bound and a global integer cycle no longer than `tau_max`. No claim is made for constant-gap integer policies, a vehicle capacity restriction, a peak-day objective, or arbitrary metric travelling-salesperson costs.

### 2.2 Nested two-edge formula

For maximum gaps `a <= b`, activation costs `u,v >= 0`, and nested descendant activation days, write `b=ma+r`. The claim is

\[
C_2=\min_{1\le d\le b}\frac{u\lceil d/a\rceil+v}{d}
=\min\left\{\frac ua+\frac v{ma},\frac{(m+1)u+v}{b}\right\}
\]

when `r>0`; if `r=0`, `C_2=u/a+v/b`. The strict excess for `r>0` is

\[
\min\left\{\frac{a-r}{ab}u,\frac r{mab}v\right\}.
\]

This is a closed-form special case of an already studied line problem. It does not resolve the complexity of the line or tree problem.

### 2.3 Equality and pooled costs

For tree edges with effective turnovers `q_e=min_{i in D(e)} tau_i`, the edge-frequency lower bound is attained exactly when positive-cost comparable edges have `q_ancestor | q_descendant`.

For weighted coverage features `A` of positive weight, let `q_A=min_{i in A} tau_i` and `ell_i=lcm{q_A:i in A}`; an empty lcm is one. The coverage-frequency lower bound is attained exactly when `ell_i <= tau_i` for every client. These are statements about uncapacitated rolling-window service; they are not feasibility criteria for pinwheel scheduling or processors with limited daily capacity.

The pooled pair lower bound allocates edge weights across incompatible comparable pairs and adds their two-edge excesses. Its mathematical claim is validity of any feasible allocation; a floating-point optimiser's suggested allocation is separately converted to a rational feasible certificate.

### 2.4 Two restriction barriers and the budget profile

For a unit-weight star with turnovers `M,...,2M-1`, `M>=2`, define

\[
L_M=H_{2M-1}-H_{M-1}.
\]

Unrestricted optimal cost is `L_M`. Minimum cost is exactly one under either of two output restrictions: one projected real harmonic ladder, or any global integer cycle `P <= 2M-1`. These are restrictions on output policies, not hardness results for the unrestricted problem. Independent leaf periods solve the witness stars exactly.

For a prescribed positive integer cycle,

\[
C_M(P)=\frac1P\sum_{q=M}^{2M-1}\lceil P/q\rceil.
\]

Writing `a=floor(h/2)`, `b=floor(h)`, the limit profile is

\[
g(h)=\frac1h\int_1^2\lceil h/x\rceil\,dx
=H_b-H_a+\frac{1+2a-b}{h}.
\]

It is a continuous nonincreasing function, with a uniform finite-size error at most `1/M` for the optimum over `P <= B` evaluated at `h=B/M`. This profile concerns the witness family only.

## 3. Exact fingerprints

### Two-edge values

| `(a,b,u,v)` | Singleton bound | Exact optimum | Excess |
|---|---:|---:|---:|
| `(2,3,1,1)` | `5/6` | `1` | `1/6` |
| `(2,5,1,1)` | `7/10` | `3/4` | `1/20` |
| `(3,5,1,1)` | `8/15` | `3/5` | `1/15` |
| `(3,7,1,1)` | `10/21` | `1/2` | `1/42` |
| `(2,3,2,4)` | `7/3` | `8/3` | `1/3` |

The only possible optimiser gap lengths are `ma` and `b`. This endpoint property is a stronger fingerprint than the appearance of a ceiling function alone.

### Coverage equality examples

With feature sets `{1,3}` and `{2,3}`, each of weight one, and client turnovers `(2,3,6)`, feature turnovers are `(2,3)` and client lcms are `(2,3,6)`. The bound `5/6` is attained. Replacing the last turnover by five preserves the feature turnovers but violates `ell_3 <= tau_3`, so the bound is not attained. Nested sets `{1,2}` and `{2}` at turnovers `(2,3)` give `ell=(2,6)` and the two-edge obstruction above.

### Star sequence and transformed sequence

| `M` | `L_M` | `1/L_M` |
|---:|---:|---:|
| 1 | `1` | `1` |
| 2 | `5/6` | `6/5` |
| 3 | `47/60` | `60/47` |
| 4 | `319/420` | `420/319` |
| 5 | `1879/2520` | `2520/1879` |
| 6 | `20417/27720` | `27720/20417` |
| 7 | `263111/360360` | `360360/263111` |
| 8 | `52279/72072` | `72072/52279` |
| 9 | `1768477/2450448` | `2450448/1768477` |
| 10 | `33464927/46558512` | `46558512/33464927` |

The sequence is classical. In particular,

\[
L_M=\sum_{k=1}^{2M-1}\frac{(-1)^{k-1}}k,
\qquad
-\log(1+x)\log(1-x)=\sum_{M\ge1}\frac{L_M}{M}x^{2M}.
\]

The numerator search matched [OEIS A049281](https://oeis.org/A049281), which records the second formula and the same first ten numerators. This is a sequence identity, not a scheduling-theorem identity. No novelty is assigned to the harmonic-number sequence, its generating function or its limit.

The profile plateaux are `g=1` on `[1,2]`, `5/6` on `[3,4]`, and `47/60` on `[5,6]`: these are the same alternating-harmonic partial sums.

## 4. Verified collision: real-time harmonic specialisation

The indexed author-hosted text of Díaz-Ramírez et al. (2013), Algorithm 2, reproduces the Sr algorithm and attributes it to Han and Tyan. It folds the original periods into a factor-two interval, sorts their distinct folded values, evaluates a utilisation recurrence, chooses the best folded base, and returns

\[
T'_i=r^*2^{\lfloor\log_2(T_i/r^*)\rfloor}.
\]

Mohaqeqi et al. (2018), Section 1, independently identifies Sr and DCT as previous harmonic-period transformation algorithms. Its Section 2 allows real-valued periods and defines harmonicity by integer ratios. Its own optimisation objectives and processor-utilisation constraints differ from replenishment.

The verified translation is:

| Real-time term | Replenishment term |
|---|---|
| original task period `T_i` | integer turnover `tau_i` |
| task execution cost `C_i` | greedy supporting weight `a_i` |
| transformed period `T'_i <= T_i` | internal clock `p_i <= tau_i` |
| utilisation `sum_i C_i/T'_i` | unsaturated average clock cost `sum_i a_i/p_i` |
| folded base `r*`, modulo powers of two | phase `alpha in [1,2)` |
| harmonic chain | common dyadic ladder |

For `tau_i>=2`, the objectives are identical after this translation. Terms with turnover one are daily constants after coalescence. Removing those constants does not create a new real-period optimisation problem. The candidate breakpoints are equivalent after rescaling by powers of two. Therefore the standalone formula and breakpoint algorithm have a collision; their independent derivation here does not establish priority.

The inspected Sr reproduction does not establish a theorem about coalesced integer-day events, arbitrary monotone submodular set costs, or a sharp global-cycle restriction. That is a boundary of this inspection, not a claim that those topics are absent from all earlier work.

**Access limitation:** the original 1997 full text was not retrieved. Algorithm 2 was inspected in the search index of the author-hosted 2013 PDF; direct opening of that PDF failed, and the alternate publisher/SciELO routes were blocked or timed out. The searchable algorithm itself is sufficiently explicit to establish the formula identity, but this is not a claim to have read the original Han–Tyan proof.

## 5. Relation to the originating logistics paper

Bosman et al. (2022), Section 1, defines rolling-window feasibility and repeating schedules, then introduces a constant-gap restriction for compact representation. Lemma 2 gives the edge-frequency bound. Theorem 4 proves factor two by integer power-of-two rounding. Section 3.2 supplies a pseudopolynomial dynamic programme on a line, constructing repeating blocks up to the farthest client's turnover. The conclusion asks whether factor two on trees can improve.

The present calendar theorem uses the rolling-window feasible set. Its individual service gaps need not be constant. It improves the inspected guarantee under that interpretation and does not answer a problem explicitly restricted to constant-gap integer policies. The two-edge closed form sits inside the already solvable line case. The reported structural result is its explicit obstruction and cost-allocation use, not the first exact algorithm for a two-node line.

## 6. Corpus, aliases and query log

The public web searches used two search engines, with the stronger engine used to verify the mathematical sources and formula matches. Primary publisher pages and author-hosted papers were preferred. Secondary records were used for metadata or to locate originals. No author was contacted, no private repository was searched, and no subscription bibliographic database was exhaustively queried.

Cross-disciplinary aliases covered recurring replenishment, nested renewal events, periodic maintenance, pinwheel/windows scheduling, harmonic task-period assignment, rate-monotonic utilisation, hyperperiod compression, short global cycles, submodular coverage, congruence intersections, divisibility and least common multiples. The renewal-reward interpretation of the two-edge quotient and the finite-state minimum-mean-cycle interpretation were checked algebraically; no claim that those standard tools are novel is made. Representation-theoretic and physical aliases were considered but did not produce a plausible object beyond classical harmonic-number sequences.

### A. Two-edge, divisibility and coverage searches

```text
"replenishment" "ceil" "b/a" "turnover"
"replenishment" "divisibility" "lower bound" turnover
"replenishment" "least common multiple" "coverage"
"joint replenishment" "maximum" "two" "interval" exact
"periodic maintenance" "nested" "ceil"
"replenishment" "lcm" "optimal" "submodular"
"replenishment" "ceil(d"
"replenishment" "ceiling" "two" "turnover"
"maintenance" "nested" "maximum intervals" cost
"periodic" "scheduling" "least common multiple" "lower bound" submodular
"submodular" "replenishment" "attain" "lower bound"
"coverage" "maximum gap" "least common multiple"
"replenishment" "divides" "lower bound" "tree"
```

No inspected source supplied the two endpoint formula, the coverage lcm equality criterion, or the specific pooled pair allocation. Related maintenance and periodic-task papers often impose processor or server capacity, or exact periods; those restrictions prevent a direct identification.

### B. Harmonic algorithms and barriers

```text
"harmonic" "periods" "1/ln" replenishment
"harmonic" "ln 2" "star" replenishment
"power-of-two" "harmonic numbers"
"Nearly optimal perfectly-periodic schedules" pdf
"harmonic schedules" "1.442"
"periodic" "harmonic" "ln 2" approximation schedules
"harmonic" "period transformation" "ln" utilisation
"harmonic" "periods" "1.4427"
"harmonic" "periods" "ln(2)" approximation
Han Tyan 1997 harmonic task transformation utilization bound paper
"harmonic task" "utilization" "optimal" transformation
"harmonic" "period" "transformation" "1/ln"
"A better polynomial-time schedulability test" pdf Han Tyan 1997
"Han" "Tyan" "Sr" harmonic "bound"
"Enhanced fixed-priority real-time scheduling on multi-core platforms by exploiting task period relationship"
"A better polynomial-time schedulability test" "pdf" "tyan"
"harmonic" "Sr" "Tyan" "log"
"Comprehensive Comparison of Schedulability Tests" "pdf"
"641267" pdf
"schedulability" "Sr" "Han" "1997" filetype:pdf
site:delta.cs.cinvestav.mx/~pmalvarez/ComparisonRM-Tests_arnoldo_jmcart.pdf "r" "Algorithm 2"
"harmonic period" "ln" "bound" minimum utilization
"harmonic" "Tyan" "tight"
"harmonic" "periods" "2n" "lower bound"
```

This family yielded the verified Sr collision. The familiar `ln 2` real-time utilisation threshold also makes the numerical constant non-distinctive. No claim of a new constant or of first harmonic rounding is permitted. Neither that constant alone nor an abstract on perfectly periodic broadcast schedules establishes equivalence of the exact policy-restriction barrier.

### C. Sequence and short-cycle rerun after simplification

```text
"1, 5, 47, 319, 1879, 20417"
"6/5" "60/47" "420/319"
"H_{2n-1}" "H_{n-1}" scheduling harmonic
site:oeis.org/A049281 "FORMULA"
"scheduling" "harmonic" "H_{2" "period"
"replenishment" "short" "cycle" "ln"
"sum" "ceil(P" "periodic" "scheduling"
"harmonic" "cycle" "ceil" "1.442"
"period" "harmonic" "H_{2n"
"short cycle" "maximum gap" scheduling
"hyperperiod" "1/ln"
"period harmonization" "worst" "ln"
"hyperperiod" "period" "harmonization" "approximation"
"maximum gap" "cyclic" "approximation" scheduling
"harmonic" "period" "harmonic numbers" scheduling
"replenishment" "ceil" "cycle length"
```

The sequence query matched the classical generating function. The short-cycle queries returned related hyperperiod and scheduling work but no inspected statement equivalent to the exact supremum `OPT_short/OPT = 1/ln 2`, or to the specific function `g(h)`. Query recall is limited, especially for mathematical expressions whose formatting is lost in indexing.

**Final freeze boundary:** Theorem 7 is the exact price of restricting the global cycle to at most the largest turnover, across the stated tree and submodular classes. Theorem 8 is the finite-budget and asymptotic horizon profile for the consecutive-turnover star family. Both were included in this rerun after the witness simplification. No separate universal theorem for larger horizon budgets is claimed. The primary material inspected under the hyperperiod aliases did not establish a collision, but the search did not exhaust all real-time period-assignment papers or inspect every cited antecedent. This is the final recorded search boundary for the eight-theorem manuscript; no priority clearance beyond it is implied.

## 7. Outcome by contribution unit

| Unit | Adjudication | Consequence |
|---|---|---|
| Logarithmic random shift, greedy submodular weights | Established precedent | Credit the inventory sources in the main novelty report. |
| Real-period clock formula and breakpoint minimisation | **COLLISION** | Credit Han–Tyan via the inspected Sr reproduction; no standalone novelty claim. |
| Complete integer-event projection and hard-gap theorem | **BOUNDED UNCERTAINTY** | A proved candidate application/bridge; no certified historical first. |
| Two-edge closed form | **BOUNDED UNCERTAINTY** | Present as a structural exact formula inside an already solvable line case. |
| Tree divisibility and coverage lcm equality | **BOUNDED UNCERTAINTY** | State the theorem and proof; acknowledge classical congruence reasoning. |
| Pooled pair programme | **BOUNDED UNCERTAINTY** | Claim a valid lower-bound construction, not a new general LP principle. |
| Harmonic number sequence and generating function | **COLLISION** | Classical identity; do not treat its rediscovery as research novelty. |
| Entire harmonic-family barrier | **BOUNDED UNCERTAINTY** | Exact restriction theorem with transparent witness; no problem-hardness claim. |
| Sharp global short-cycle ratio and budget profile | **BOUNDED UNCERTAINTY** | Strongest candidate structural theorem; further hyperperiod literature check needed. |
| Proof and verification bundle | Independently produced artefact | Does not establish the first proof or historical priority. |

Permitted wording: “We prove the following theorem for integer rolling-window calendars”; “this improves the factor-two guarantee in the inspected 2022 paper under the stated cyclic interpretation”; “an equivalent structural theorem was not found in the bounded search recorded here.”

Forbidden wording: “the first harmonic rounding algorithm”; “a new logarithmic constant”; “the first exact algorithm on two-edge paths”; “the literature's currently open problem is conclusively resolved”; “no earlier result exists.”

The next load-bearing historical checks are the original Han–Tyan paper and Hermansen's 2025 thesis, followed by specialist scrutiny of short-cycle and hyperperiod approximation literature. These checks affect priority and positioning; the supplied elementary proofs can be evaluated independently.

## 8. Inspected references and access record

### Primary mathematical sources used in this rerun

Bosman, T., van Ee, M., Jiao, Y., Marchetti-Spaccamela, A., Ravi, R., & Stougie, L. (2022). Approximation algorithms for replenishment problems with fixed turnover times. *Algorithmica, 84*, 2597–2621. <https://doi.org/10.1007/s00453-022-00974-4>. Full publisher text inspected, including Sections 1, 3.2 and 5, Lemma 2 and Theorem 4. <https://link.springer.com/article/10.1007/s00453-022-00974-4>

Díaz-Ramírez, A., Mejía-Alvarez, P., & Leyva-del-Foyo, L. E. (2013). Comprehensive comparison of schedulability tests for uniprocessor rate-monotonic scheduling. *Journal of Applied Research and Technology, 11*(3), 408–436. <https://doi.org/10.1016/S1665-6423(13)71551-7>. Algorithm 2 and adjoining explanation inspected through indexed author PDF text: <https://delta.cs.cinvestav.mx/~pmalvarez/ComparisonRM-Tests_arnoldo_jmcart.pdf>. Direct document retrieval unsuccessful; this paper reproduces and attributes the prior algorithm rather than originating it.

Mohaqeqi, M., Nasri, M., Xu, Y., Cervin, A., & Årzén, K.-E. (2018). Optimal harmonic period assignment: Complexity results and approximation algorithms. *Real-Time Systems, 54*, 830–860. <https://doi.org/10.1007/s11241-018-9304-0>. Full publisher text inspected for the model, prior Sr/DCT discussion and distinct optimisation objectives. <https://link.springer.com/article/10.1007/s11241-018-9304-0>

### Identification and access-boundary records

Han, C.-C., & Tyan, H.-Y. (1997). A better polynomial-time schedulability test for real-time fixed-priority scheduling algorithms. In *Proceedings of the 18th IEEE Real-Time Systems Symposium* (pp. 36–45). <https://doi.org/10.1109/REAL.1997.641267>. Metadata and later mathematical reproduction inspected; original full text not inspected. Metadata: <https://dblp.uni-trier.de/rec/conf/rtss/HanT97.html>.

OEIS Foundation Inc. (n.d.). *A049281: Numerators of coefficients in power series for -log(1+x)*log(1-x).* Retrieved October 31, 2026, from <https://oeis.org/A049281>. Used for sequence identity, not as evidence for a scheduling theorem.

Bille, P. (n.d.). *Students and supervision*. Technical University of Denmark. <https://people.compute.dtu.dk/~phbi/people.html>. The session's main novelty audit found the entry for Hans Henrik Hermansen's Spring 2025 MSc thesis with the same title as Bosman et al.; the thesis itself remains uninspected.

Additional leads were screened at abstract or indexed-excerpt level, including Xu, Cervin and Årzén (2016), “Harmonic scheduling and control co-design,” <https://doi.org/10.1109/RTCSA.2016.44>, and Fan et al. (2015), “Enhanced fixed-priority real-time scheduling on multi-core platforms by exploiting task period relationship,” <https://doi.org/10.1016/j.jss.2014.09.010>. They provide search aliases, not decisive negative evidence about the new structural claims. The main novelty report separately records the inventory and contemporary joint-replenishment sources.
