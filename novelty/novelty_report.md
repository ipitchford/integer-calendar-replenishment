# Novelty-gate report: integer-calendar replenishment under hard maximum gaps

**Search date:** 31 October 2026 (Europe/London).  
**Researcher:** independent literature-checking agent, with findings reported to the theorem-development agent.  
**Corpus boundary:** two public web-search engines; Exa search and extraction; arXiv; publisher pages and openly accessible PDFs; university repositories and personal academic pages; targeted DTU thesis searches. This was a bounded search, not an exhaustive literature review.  
**Intended contribution unit:** a discrete-calendar theorem and an explicit algorithm, rather than a new logarithmic-rounding method or a newly discovered numerical constant.

## 1. Frozen claim

For a finite client set, positive integer turnover times \(\tau_i\), and a normalised, nonnegative, monotone submodular daily service-cost function \(f\), construct a feasible cyclic integer-day schedule with average cost at most \(1/\ln 2\) times the infimum over feasible schedules. The schedule has a compact arithmetic description; the intended construction chooses a rational breakpoint and has cycle length at most \(\max_i\tau_i\). The rooted-tree routing problem is a special case, with each used edge charged twice.

The candidate's proposed mechanism is

\[
p_i(\alpha)=\alpha 2^{\lfloor\log_2(\tau_i/\alpha)\rfloor},
\qquad 1\leq\alpha<2,
\]

followed by the common calendar map \(kp_i\mapsto\lceil kp_i\rceil\). All visits landing on the same integer day are combined. The shifted periods remain nested before and after this map. The theorem-development files contain the complete proof and the precise treatment of periods below one day, ties and cycle boundaries.

The problem statement excludes stockout penalties, vehicle capacities, route-duration constraints, stochastic demands, minimum spacing between visits, and guarantees on the largest daily route. It does not settle the computational complexity of finding the exact optimum on trees. General metric travelling-salesman tour costs are not assumed submodular.

Before adjudication, the permitted research claim is: **a candidate improvement of the tree approximation guarantee stated by Bosman et al. (2022), obtained by adapting classical inventory rounding to hard integer-day service windows.** Historical priority remains conditional on the recorded corpus boundary.

## 2. Normalisation and model translation

| Source or formulation | Normalised object | Verified relation or distinction |
|---|---|---|
| Bosman et al. turnover time | Maximum gap \(\tau_i\) between integer-day services | Every consecutive window of \(\tau_i\) days must contain service. This matches the candidate feasibility condition. |
| Bosman et al. rooted-tree tour cost | \(f(S)=2\sum_{e:S\cap D(e)\ne\varnothing}c_e\) | The factor two accounts for a closed walk from and back to the depot. |
| Their edge turnover weight | \(q_e=\min_{i\in D(e)}\tau_i\) | Their lower bound is \(2\sum_e c_e/q_e\). This lower bound is prior art. |
| Their repeating schedule versus their more restrictive periodic output | Cyclic schedule versus constant inter-service interval for each client | The candidate is cyclic, but its individual client gaps can alternate. It does not preserve the narrower stationary/constant-gap output class. |
| Teo–Bertsimas resource constraints | \(\sum_j a_{ij}/T_j\le A_i\) | Feasibility is preserved by increasing periods. Their Algorithm C explicitly uses \(T_j^o\ge T_j^*\). This is the opposite rounding direction from a hard maximum-gap cap. |
| Federgruen–Zheng submodular setup costs | Submodular \(f\) and its chain/base-polyhedron representation | Submodular joint replenishment and its cost decomposition are classical; neither is a novelty claim. |
| Federgruen–Zheng (1993) individual capacity bounds | Upper and lower bounds on continuous replenishment intervals | This work explicitly includes storage-imposed upper bounds. It optimises a fixed-base power-of-two policy class, with bounds rounded to that grid; it does not establish the candidate integer-calendar theorem. |
| Han–Tyan's \(S_r\) specialisation, reproduced by Díaz-Ramírez et al. (2013) | \(T'_i=r2^{\lfloor\log_2(T_i/r)\rfloor}\), minimising \(\sum_i C_i/T'_i\) over one logarithmic period | The real-period map, its finite breakpoint set and the \(O(n\log n)\) sweep collide after rescaling the phase and taking \(C_i=a_i\). Daily saturation for \(\tau_i=1\) is handled separately in the candidate. |
| Mechanical words | \(\lfloor t/p\rfloor-\lfloor(t-1)/p\rfloor\), with positive values coalesced | This is the calendar membership indicator when \(p\ge1\), and a positive-event test for general \(p>0\). The floor/ceiling identity is not new. |
| Segev's 2026 constrained joint replenishment | Upward-closed feasible period sets | Its published guarantees concern a different feasible region and cost trade-off. They do not by themselves establish a discrete hard-gap schedule. |

## 3. Formula fingerprints

The decisive fingerprint is the reciprocal-period expectation, not the application title:

\[
\mathbb E_{\alpha}\frac1{p_i(\alpha)}
=\frac1{\tau_i\ln2},\qquad
d\Pr(\alpha)=\frac{d\alpha}{\alpha\ln2}.
\]

The shared logarithmic shift, the density \(1/(\alpha\ln2)\), dyadic period nesting, and the factor \(1/\ln2\) all collide with established inventory-rounding mathematics. The potentially new component is their use with a common integer-calendar map, hard maximum inter-visit gaps, and a finite exact breakpoint selection procedure.

Small exact schedule fingerprints, fixed in `target.yaml`, are:

| Turnover vector | Modular frequency lower bound | Best cost within the proposed shared dyadic calendar family, for unit service costs |
|---|---:|---:|
| \((1)\) | \(1\) | \(1\) |
| \((2,3)\) | \(5/6\) | \(1\) |
| \((4,5,6,7)\) | \(319/420\) | \(1\) |

The associated dyadic-block family has lower bound \(\sum_{q=M}^{2M-1}1/q\); its limit is \(\ln2\). Harmonic-sum asymptotics are classical. A lower-bound family for the *restricted calendar algorithm* must not be described as an inapproximability result for the underlying optimisation problem.

There is no new finite matrix, spectrum or generating function whose identity needs adjudication here. OEIS would not distinguish the proposed theorem from known harmonic numbers; the relevant identity search is at the scheduling, submodular-optimisation and inventory-rounding levels.

## 4. Cross-domain aliases searched

| Area | Aliases and their role |
|---|---|
| Inventory and logistics | Fixed turnover replenishment; joint replenishment; submodular ordering costs; power-of-two policies; storage/period caps; resource-constrained lot sizing. |
| Scheduling | Harmonic periods; recurrent tasks; periodic maintenance; pinwheel scheduling; bounded inter-visit gaps; cyclic versus stationary schedules. |
| Probability and optimisation | Shared random logarithmic shift; randomised rounding; Lovász extension; submodular convex closure; chain decomposition. |
| Combinatorics and discrete geometry | Beatty sequences; mechanical words; floor/ceiling discretisation; commensurable clocks. |
| Mathematical physics | Synchronised clocks and commensurable periods were considered only as translations. No distinct physics theorem matching the optimisation guarantee was identified. |

## 5. Search record

All queries below were executed on 31 October 2026. Similar queries were sometimes run in both search engines to check coverage. Results listed as negative mean only that no matching result was retrieved in that query family.

| Corpus | Exact query or query family | Main inspected result and consequence |
|---|---|---|
| Public web search, engine 1 | `"Replenishment Problems with Fixed Turnover Times" approximation 2024 2025` | Located the 2022 primary paper and recent adjacent inventory work. |
| Engines 1 and 2 | `"fixed turnover" "1.44"`; `"fixed turnover" "ln" approximation`; `"fixed turnover" "rounding"` | No retrieved direct statement of the candidate hard-gap ratio. This is negative evidence, not priority proof. |
| Engine 1 | `"replenishment" "randomized" "power-of-two"` | Located Teo–Bertsimas and Segev; identified the classical constant and method collision. |
| Engine 2 | `"fixed turnover times" "approximation" 2025 2026` | Located the DTU thesis listing. |
| Engines 1 and 2 | `"Hans Henrik Hermansen" replenishment`; `"Hermansen" "replenishment"`; `"fixed turnover times" "Bille"`; `"fixed turnover times" "Gørtz"` | Verified the Spring 2025 MSc thesis exists by a supervisor's institutional page. No full text obtained. |
| Engine 1 | `"fixed turnover" site:github.com`; `"Hermansen" "replenishment" site:github.com`; `"fixed turnover" thesis Hermansen filetype:pdf` | No thesis repository or PDF retrieved. |
| Exa | Natural-language query specifying Hermansen, Spring 2025, DTU, exact thesis title, and excluding the older paper | Returned the same supervision listing, not thesis text. |
| DTU Findit public catalogue | `title:("Replenishment Problems with Fixed Turnover Times")`; `author:("hermansen hans")`; `"fixed turnover"` | Each query returned a visitor-verification wall. No attempt was made to bypass it. |
| DTU Orbit | Public student-thesis listing and `?search=Replenishment` | No usable thesis record or text was returned. |
| Engine 1 | `Roundy 1989 Rounding Off to Powers of Two capacitated lot sizing pdf` | Located publisher metadata/abstract and a Cornell technical-report record. The 1989 full text was not inspected in this pass. |
| Engine 1 | `Federgruen Zheng 1992 joint replenishment generalized holding cost constraints pdf` | Opened the Columbia-hosted primary PDF. |
| Engine 1 | `"Optimal Power-of-Two Replenishment Strategies" pdf`; `"Federgruen" "Zheng" "1993" "upper" "bounds" replenishment` | Opened the 1993 Columbia-hosted primary PDF and inspected its storage caps and fixed-base restriction. |
| Engine 1 | `Teo Bertsimas 2001 multistage lot sizing randomized rounding maximum inventory capacity pdf` | Opened the MIT-hosted primary PDF; inspected the resource constraints and algorithm. |
| Engine 1 | `"Automated Teller Machine Replenishment Policies with Submodular Costs"`; `"ATM" "submodular" "replenishment"` | Opened publisher abstract for Zhang–Kulkarni. It is an MDP and index-policy study, rather than a hard-gap approximation result. |
| Engines 1 and 2 | Exact ATM title with `pdf`; DOI with `pdf`; author names with `dissertation` | Publisher PDF link returned the abstract. A related 2016 dissertation was identified but not retrieved in this pass. |
| Engine 1 | `"submodular" "turnover"`; `"submodular" "replenishment" "maximum" "interval"`; `"periodic" "submodular" "deadlines" replenishment`; `"replenishment" "1.4427" "discrete"` | Located finite-horizon joint replenishment and classical rounding, but no inspected theorem identical to the frozen claim. |
| Engine 1 | `replenishment "calendar" "rounding" "powers"`; `"submodular" "periodic" "1/ln"`; `"replenishment" "Beatty"`; `"replenishment" "mechanical words"` | No matching calendar theorem retrieved. Mechanical-word identities themselves are established mathematics. |
| Engines 1 and 2, reviewer update | `"10.1016/S1665-6423(13)71551-7"`; `Han Tyan Sr algorithm harmonic period assignment Diaz Ramirez 2013`; `"Comprehensive Comparison of Schedulability Tests" "pdf"` | Located the exact \(S_r\) specialisation and breakpoint algorithm. An author-hosted full text was retrieved using Exa after the ordinary publisher/PDF fetch failed. This supersedes the earlier tentative sweep-novelty assessment. |
| Engine 2 and primary full texts, reviewer update | `"joint replenishment" "maximum" "interval" "nested" two items`; `"periodic maintenance" "nested" "two" "cost" intervals`; `"replenishment" "divisibility" "turnover"` | No verified formula-level collision for the nested two-edge penalty or equality criterion was retrieved. This is a limited supplemental search, not a completed novelty certification for all later structural results. |

## 6. Inspected sources and exact implications

### A. Bosman et al. (2022): originating open question — full text inspected

Primary open text: <https://link.springer.com/article/10.1007/s00453-022-00974-4>.

Section 1 defines integer-day rolling-window feasibility and distinguishes repeating schedules from outputs with constant client-specific gaps. Section 3, Lemma 2 gives the edge lower bound; Theorem 4 obtains the factor two by rounding turnover times down to integral powers of two. Section 5 explicitly raises improvement of that tree guarantee. The candidate changes the output representation to a succinct cyclic calendar, so it must explain this distinction. The paper also notes an \(O(\log\log n)\) general-metric development by Bosman and Olver; the candidate must not describe \(O(\log n)\) as the latest general-metric guarantee.

### B. Teo and Bertsimas (2001): close formula-level collision — full text and formula image inspected

Primary author PDF: <https://www.mit.edu/~dbertsim/papers/OperationsManagement/Multistage%20Lot%20Sizing%20Problems%20via%20Randomized%20Rounding.pdf>.

Section 2 gives shared logarithmic randomisation; Section 2.3 handles submodular ordering costs. Section 3, equation (2), Algorithm C and Theorem 5 give the \(1.44\)-type bound under constraints \(\sum_j a_{ij}/T_j\le A_i\). Page 604 was also visually inspected to resolve extraction errors in inequality symbols. The algorithm increases periods relative to its relaxed solution. Thus the constant and rounding technique are already known. The inspected theorem does not itself give the candidate's maximum-gap integer-calendar feasibility claim. Its introduction also discusses special dyadic individual interval bounds; that is narrower than arbitrary integer caps plus calendar rounding.

### C. Federgruen and Zheng (1992): submodular joint replenishment — full text inspected

Primary author PDF: <https://business.columbia.edu/sites/default/files-efs/pubfiles/4029/federgruen_cost_structures.pdf>.

This paper already studies monotone submodular joint setup costs, power-of-two policies and lower bounds over general policies. Its model trades replenishment costs against inventory holding costs and uses constant replenishment intervals. The manuscript should credit this submodular setup-cost framework and the associated decomposition. No statement in the inspected material was verified as identical to the frozen discrete-calendar, arbitrary-hard-cap theorem. This is a model distinction, not evidence that all possible adaptations of the earlier method are new.

### D. Roundy (1989): classical factor — publisher abstract inspected; full text not inspected

Publisher page: <https://pubsonline.informs.org/doi/10.1287/mnsc.35.12.1433>.  
Earlier technical-report record: <https://ecommons.cornell.edu/entities/publication/f0bbfa05-e8ac-4eb4-b5d1-b2a74bfa691a>.

The publisher abstract reports feasibility-preserving rounding for capacitated multistage lot sizing and a maximum cost increase of about 44%, improving to about 6% with one capacity constraint. The exact formal relationship used in this report is verified through Teo–Bertsimas's explicit treatment of Roundy's model, not attributed to an uninspected proof. The report record is dated August 1986; it is not silently treated as the definitive 1989 text.

### D2. Federgruen and Zheng (1993): upper-period caps — full primary PDF inspected

Primary author PDF: <https://business.columbia.edu/sites/default/files-efs/pubfiles/4039/federgruen_replenishment_strategies.pdf>.

Page 711 explicitly derives an upper interval bound \(T\le Q/d\) from dedicated storage capacity. Section 1.2, pp. 714–715, formulates individual bounds after restricting to fixed-base power-of-two policies. It rounds arbitrary bounds down to that fixed dyadic grid without changing the *restricted* feasible region. The paper computes an optimal policy in this class. Thus it is incorrect to suggest that earlier inventory work never considered upper period bounds. The distinct candidate claim concerns integer-day calendars with potentially alternating individual gaps and a guarantee against all feasible hard-gap schedules; that theorem was not found in the inspected sections.

### E. Segev (2026): newer nearby bounds — full arXiv HTML inspected

Primary preprint: <https://arxiv.org/html/2603.18720v1>; metadata: <https://arxiv.org/abs/2603.18720>.

The 19 March 2026 version improves resource-constrained continuous joint replenishment using fractional-base grids, random shifts and interleaving. Its strongest stated ratio is \(5/(6\ln2)\). Section 5 explicitly frames feasibility through expansive rounding and upward-closed constraints. This prevents treating its stronger numerical ratio as an automatic improvement for arbitrary hard maximum gaps. It also prevents presenting \(1/\ln2\) as a new universal inventory-rounding frontier. Transfer of its interleaving ideas to the present model would require a separate proof.

### F. Zhang and Kulkarni (2018): application precedent — publisher abstract inspected only

Primary page: <https://pubsonline.informs.org/doi/10.1287/msom.2017.0656>.

The abstract identifies a Markov decision process for ATM replenishment with submodular costs and stockout costs, and an index-policy heuristic evaluated against optimal policies on smaller instances. It establishes direct application precedent for submodular replenishment costs. The requested PDF route returned the abstract, so this report does not claim to have excluded an embedded special-case theorem from the full paper. The candidate should not claim to introduce submodular ATM replenishment.

### G. Hermansen (2025): specific unresolved priority risk — institutional listing inspected only

Primary supervision listing: <https://people.compute.dtu.dk/~phbi/people.html>.

The page lists Hans Henrik Hermansen's Spring 2025 MSc thesis, *Approximation Algorithms for Replenishment Problems with Fixed Turnover Times*, jointly supervised with Inge Li Gørtz. The listing supplies no thesis PDF. Search engines and Exa did not retrieve its contents; DTU catalogue queries encountered visitor verification. Its title is too close to ignore. Nothing about its results may be inferred from its title. An author or supervisor enquiry, or access to the thesis, is the most direct remaining priority check. No enquiry was sent.

### H. Han–Tyan specialisation through Díaz-Ramírez et al. (2013) — decisive sweep collision

Author-hosted full text inspected on 31 October 2026: <https://delta.cs.cinvestav.mx/~pmalvarez/ComparisonRM-Tests_arnoldo_jmcart.pdf>. Published article DOI: <https://doi.org/10.1016/S1665-6423(13)71551-7>.

Section IV.I and Algorithm 2 reproduce the \(S_r\) algorithm credited to Han and Tyan (1997). It uses exactly \(T'_i=r2^{\lfloor\log_2(T_i/r)\rfloor}\), chooses the best real phase from at most \(n\) turnover-derived breakpoints, and evaluates the weighted reciprocal-period objective in \(O(n\log n)\). Its normalisation \(T_1/2<r\le T_1\) is equivalent to choosing a representative octave. Taking execution weights \(C_i=a_i\) identifies the candidate sweep for clients with turnover at least two. Thus the sweep is a reproduction/adaptation, not a distinct algorithmic novelty. The original 1997 paper was identified bibliographically but its full proof was not inspected in this pass; attribution is explicitly via the inspected reproduction.

### I. Later harmonic-period assignment — adjacent primary full texts inspected

Mohaqeqi et al. (2018), <https://link.springer.com/article/10.1007/s11241-018-9304-0>, formulate real harmonic-period assignments with period ranges and different utilisation/weighted-period objectives. Their introduction explicitly identifies \(S_r\) and DCT as below-cap assignments.

Bhat and Rajkumar (2023), <https://arxiv.org/html/2302.03724v1>, formulate integer harmonic-period assignment below application-specified upper bounds and include the total-system-utilisation objective \(\sum_i C_i/T'_i\). Sections II, IV and VI were inspected. These sources establish further prior art for harmonic assignment under upper caps. The inspected sections do not supply the candidate's submodular integer-event calendar theorem. No broader assertion that integer periods or below-cap harmonic assignments are new is supportable.

## 7. Verified collisions and candidate bridge

1. **Collision: shared log-uniform dyadic rounding.** Renaming Teo–Bertsimas's shift variable to \(\alpha\) leaves the same density \(1/(\alpha\ln2)\). Scaling their symmetric rounding by a constant recovers one-sided rounding. The elementary expectation calculation is a reproduction/adaptation of known machinery.
2. **Collision: submodular joint setup costs and chain decompositions.** These occur in the 1992 and 2001 primary works. Using the Lovász extension does not independently establish originality.
3. **Collision: the tree frequency lower bound.** The expression in the target is Bosman et al.'s Lemma 2 after notation changes.
4. **Candidate bridge: continuous harmonic clocks to hard integer-day windows.** Applying the same ceiling map to every harmonic clock preserves inclusions of service-day sets. Integer caps permit \(\lceil p_i\rceil\le\tau_i\). This relation supports the candidate discrete-calendar theorem; an earlier identical theorem was not found in the bounded search.
5. **Collision: finite breakpoint selection and its asymptotic arithmetic cost.** The \(S_r\) algorithm reproduced in Díaz-Ramírez et al. (2013) already provides the same real-period optimisation and \(O(n\log n)\) breakpoint sweep. The candidate supplies an exact-arithmetic implementation and uses integer turnover inputs to prove that its projected day calendar has cycle \(P\le\tau_{\max}\). The sweep must not be counted as an independent novelty. The short-cycle proof is an application property whose originality must be assessed together with the calendar theorem and later cycle-restriction bounds.

## 8. Missingness and uncertainty audit

- The exact-title 2025 MSc thesis was not inspected. This is a concrete, load-bearing priority uncertainty.
- Zhang–Kulkarni was inspected at abstract level, not full text. Roundy's definitive 1989 full text was not inspected in this pass.
- The search covered English-language titles, formulas and common aliases. It did not systematically search non-English theses, institutional catalogues worldwide or unpublished seminar notes.
- No subscription citation database, complete forward-citation graph, author enquiry or conference-submission database was used.
- Negative search results cannot establish that a question remained open on 31 October 2026.
- The mathematical theorem can remain correct even if priority collides. In that event, the contribution must be reclassified as reproduction, explicit discretisation or an implementation/refinement, depending on the earlier source.
- None of the older resource-constraint results has been proved equivalent to the whole candidate model. Conversely, a difference in constraint orientation alone is not a proof of substantial originality.
- Upper period caps themselves are also prior art, as explicitly verified in Federgruen–Zheng (1993). The relevant distinction combines caps, the comparison policy class, and the common integer-calendar mapping; it is not simply the presence of a cap.

## 9. Outcomes by contribution unit

| Contribution unit | Gate outcome | Confidence | Permitted wording | Wording to avoid |
|---|---|---|---|---|
| Factor \(1/\ln2\) and log-uniform dyadic-rounding identity | **COLLISION** | High | Classical rounding identity, used here in a discrete-calendar construction. | New constant; first logarithmic-shift method. |
| Submodular replenishment cost model and chain lower-bound machinery | **COLLISION** | High | Established submodular inventory framework. | Introduction of submodular replenishment or a new Lovász principle. |
| Downward real harmonic assignment and \(O(n\log n)\) phase sweep | **COLLISION** | High | Adaptation of the Han–Tyan \(S_r\) specialisation, as verified in Díaz-Ramírez et al. (2013). | New breakpoint search; first efficient below-cap harmonic assignment. |
| Integer-day hard-gap approximation theorem on trees | **BOUNDED UNCERTAINTY** | Moderate | Improves the factor-two guarantee in the inspected 2022 paper; no equivalent theorem found in the recorded search. | First solution; priority established; definitively open in October 2026. |
| Full monotone-submodular hard-gap theorem | **BRIDGE / BOUNDED UNCERTAINTY** | Moderate | An explicit transfer of classical rounding to the stated calendar model, with a complete proof. | Entirely new submodular optimisation technique. |
| Complete proof of calendar feasibility, exact average and short cycle | **CLEAR TO PROVE within this boundary** | Moderate | Self-contained proof and algorithm; prior-art uncertainty remains. | First complete proof without inspecting the 2025 thesis. |
| Exact implementation and reproducible checks | **CLEAR within this boundary** | High as a provenance claim, conditional on verification | Independently written implementation and verification artefacts. | Independent human validation or a certificate of novelty. |
| Two-edge penalty, divisibility/coverage equality criteria, pooled bounds and cycle-restriction results added later | **BOUNDED UNCERTAINTY; supplemental audit required** | Moderate to low on priority | Self-contained structural results with proof and checks; no collision found in the limited targeted search. | Exhaustively new theorems; priority inferred from this calendar-focused audit. |

**Overall gate decision: BOUNDED UNCERTAINTY.** Proceed with proof and computational verification while keeping historical-priority claims conditional. The classical components must be prominently credited. The uninspected 2025 thesis must appear in the manuscript's novelty boundary and review, not only in this supplement.

## 10. Rerun triggers and decisive next checks

Rerun the gate if the proof simplifies to an existing constrained-lot-sizing theorem, if the full Hermansen thesis becomes available, if a resource-constrained theorem is found allowing arbitrary upper period caps and calendar discretisation, or if the contribution changes to interleaved clocks, non-submodular costs or an exact-complexity claim. Before journal submission, obtain the 2025 thesis or a precise account of its main results and inspect the closest full texts still missing.

## References consulted

### Direct problem and unresolved thesis boundary

Bosman, T., van Ee, M., Jiao, Y., Marchetti-Spaccamela, A., Ravi, R., & Stougie, L. (2022). Approximation algorithms for replenishment problems with fixed turnover times. *Algorithmica, 84*, 2597–2621. <https://doi.org/10.1007/s00453-022-00974-4>

Bille, P. (n.d.). *MSc., BSc, and B.Eng. theses* [Supervision listing; includes Hermansen, Spring 2025]. Technical University of Denmark. Retrieved 31 October 2026, from <https://people.compute.dtu.dk/~phbi/people.html>

### Classical and recent inventory rounding

Federgruen, A., & Zheng, Y.-S. (1992). The joint replenishment problem with general joint cost structures. *Operations Research, 40*(2), 384–403. <https://doi.org/10.1287/opre.40.2.384>

Federgruen, A., & Zheng, Y.-S. (1993). Optimal power-of-two replenishment strategies in capacitated general production/distribution networks. *Management Science, 39*(6), 710–727. <https://doi.org/10.1287/mnsc.39.6.710>

Roundy, R. (1989). Rounding off to powers of two in continuous relaxations of capacitated lot sizing problems. *Management Science, 35*(12), 1433–1442. <https://doi.org/10.1287/mnsc.35.12.1433> [Publisher abstract inspected.]

Segev, D. (2026). *Resource-constrained joint replenishment via power-of-\(m^{1/k}\) policies* (Version 1). arXiv. <https://arxiv.org/abs/2603.18720>

Teo, C.-P., & Bertsimas, D. (2001). Multistage lot sizing problems via randomized rounding. *Operations Research, 49*(4), 599–608. <https://doi.org/10.1287/opre.49.4.599.11222>

### Logistics application precedent

Zhang, Y., & Kulkarni, V. (2018). Automated teller machine replenishment policies with submodular costs. *Manufacturing & Service Operations Management, 20*(3), 517–530. <https://doi.org/10.1287/msom.2017.0656> [Publisher abstract inspected.]

### Harmonic scheduling sources added during the full review

Díaz-Ramírez, A., Mejía-Alvarez, P., & Leyva-del-Foyo, L. E. (2013). Comprehensive comparison of schedulability tests for uniprocessor rate-monotonic scheduling. *Journal of Applied Research and Technology, 11*(3), 408–436. <https://doi.org/10.1016/S1665-6423(13)71551-7> Author-hosted full text: <https://delta.cs.cinvestav.mx/~pmalvarez/ComparisonRM-Tests_arnoldo_jmcart.pdf>.

Mohaqeqi, M., Nasri, M., Xu, Y., Cervin, A., & Årzén, K.-E. (2018). Optimal harmonic period assignment: Complexity results and approximation algorithms. *Real-Time Systems, 54*, 830–860. <https://doi.org/10.1007/s11241-018-9304-0>.

Bhat, A., & Rajkumar, R. (2023). *Assigning optimal integer harmonic periods to hard real-time tasks* [Preprint]. arXiv. <https://arxiv.org/abs/2302.03724>.

## Sanity checks on the literature inference

The same number in two papers is not by itself a theorem collision; here the shared rounding distribution is also identical, so the method/constant collision is real. The feasibility constraints, however, differ in direction. That distinction preserves a candidate application theorem without certifying its priority. A cyclic schedule with alternating gaps must also never be described as a constant-gap stationary policy.
