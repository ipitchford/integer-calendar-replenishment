# A sharp approximation–cycle-length tradeoff

The proof below is elementary and independent of harmonic-calendar restrictions. It supplies a stronger interpretation of the main approximation ratio. No historical-priority claim is made.

## The witness family and exact cost at a prescribed cycle length

For M≥2, consider a star with one leaf of turnover q for each q=M,...,2M−1. Every leaf has unit activation weight (edge length 1/2). Since leaf costs add independently, the unrestricted optimum is

S_M=sum_{q=M}^{2M−1}1/q.

For any prescribed positive integer cycle length P, the exact optimum among P-periodic schedules is

C_M(P)=(1/P) sum_{q=M}^{2M−1} ceil(P/q).                     (A1)

To prove the lower bound, a leaf of turnover q needs at least ceil(P/q) visits: its positive cyclic gaps sum to P and are at most q. To attain the bound, give that leaf k=ceil(P/q) visits whose gaps are floor(P/k) and ceil(P/k). Such integer gaps can be selected to sum to P, and ceil(P/k)≤q. Leaves can be scheduled independently because their activation costs add. This establishes (A1).

For a cycle budget B, define C_M^*(B)=min_{1≤P≤B} C_M(P).

## Exact short-cycle barrier

If P<M, every leaf needs a visit, so C_M(P)≥M/P>1. If M≤P≤2M−1, exactly P−M turnover values are below P. Those leaves need two visits, and all the remaining leaves need one. Therefore C_M(P)=1 throughout this integer range. Thus

C_M^*(2M−1)=1,       S_M→ln(2).

The optimal ratio under the output restriction P≤tau_max therefore tends to 1/ln(2), even if schedules may be arbitrary rather than harmonic. This is an output-cycle restriction, not computational inapproximability of the unrestricted problem.

## The complete asymptotic cycle-budget profile

Define, for t>0,

g(t)=(1/t) integral_1^2 ceil(t/x) dx.                       (A2)

Let H_j=sum_{k=1}^j 1/k, H_0=0. Put a=floor(t/2), b=floor(t). Counting the integer thresholds crossed by t/x gives

integral_1^2 ceil(t/x) dx
 = 1 + sum_{k≥1} [min(2,t/k)−1]_+
 = 1+2a−b + t(H_b−H_a).

Consequently

g(t)=H_b−H_a+(1+2a−b)/t.                                  (A3)

An exact, continuous piecewise description is

g(t)=H_{2k}−H_k+1/t,     2k≤t≤2k+1,

g(t)=H_{2k+1}−H_k,       2k+1≤t≤2k+2,

for integers k≥0, excluding t=0. The expressions agree at every endpoint. Thus g is continuous and nonincreasing: it decreases on each even-to-odd interval and is constant on the following odd-to-even interval. In particular,

- g(t)=1 on [1,2];
- g(t)=5/6 on [3,4];
- g(t)=47/60 on [5,6];
- g(t)=319/420 on [7,8].

The last fraction equals H_7−H_3=1/4+1/5+1/6+1/7.

### Uniform finite-size error

For t=P/M, the summand in (A1) is a left Riemann sum for (A2):

C_M(P)=(1/t)(1/M) sum_{q=M}^{2M−1} ceil(t/(q/M)).

The function x→ceil(t/x) is nonincreasing on [1,2]. Its left-sum error is between zero and [ceil(t)−ceil(t/2)]/M. For t<1 this numerator is zero. For t≥1 it is at most t. Hence, for every positive integer P,

0≤C_M(P)−g(P/M)≤1/M.                                      (A4)

Because g is nonincreasing, (A4) yields the useful finite bound

g(B/M) ≤ C_M^*(B) ≤ g(B/M)+1/M.                            (A5)

The upper bound evaluates the feasible choice P=B; no assertion that B is the exact finite optimum is needed.

For every fixed h>0, take B=floor(hM). Continuity of g and (A5) imply

lim_{M→infinity} C_M^*(floor(hM)) = g(h),

lim_{M→infinity} C_M^*(floor(hM))/S_M = g(h)/ln(2).          (A6)

Thus the period-budget profile is asymptotically sharp, with both the lower bound and matching finite calendars explicit. A budget expressed as a multiple beta of tau_max≈2M corresponds to h=2beta.

### Illustrative limits

| Cycle budget relative to tau_max | h | Limiting cost / unrestricted optimum |
|---|---:|---:|
| 1 | 2 | 1/ln(2) |
| 3/2 | 3 | 5/[6ln(2)] |
| 2 | 4 | 5/[6ln(2)] |
| 5/2 | 5 | 47/[60ln(2)] |
| 3 | 6 | 47/[60ln(2)] |
| 4 | 8 | 319/[420ln(2)] |

These are exact asymptotic limits for the displayed star family. They are not approximation guarantees for all trees. The appearance of 5/[6ln(2)] in the horizon profile is an arithmetic consequence of this witness and does not establish an algorithm with that general guarantee.

## Verification plan

`verification/short_cycle_budget_check.py` independently enumerates all nonempty binary cyclic visit patterns for small P and q, checks their maximum cyclic gaps, and verifies the minimum visit count ceil(P/q). It then checks (A3)–(A5), including integer endpoints, in exact rational arithmetic over a bounded set of finite stars. Data are saved under `data/short_cycle_budget_checks.json` and `data/period_budget_limit.csv`.
