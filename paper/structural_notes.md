# Structural results for tree replenishment

These are independently derived theorem notes, not a priority claim. Date: 31 October 2026. The original two-edge optimisation is a special case of Bosman et al.'s pseudopolynomial line problem; the closed form and pooled lower bound need a separate literature audit before any novelty assertion.

## Definitions

Let a rooted tree have nonnegative edge costs. Delete edges whose descendant subtrees contain no clients. For each remaining edge e, let q_e be the minimum integer turnover time of a client below e. Write w_e=2c_e, so that activating an edge on one day costs w_e. A daily tour is a closed walk from the root; deleting repeated excursions cannot hurt feasibility, so its minimum cost is the sum of w_e over activated edges. The activation-day set of a descendant edge is contained in that of any ancestor edge. Every q_e consecutive days must include an activation of e.

The elementary lower bound is

L = sum_e w_e/q_e.

All results below hold for arbitrary feasible schedules when average cost is interpreted by a limiting inferior or superior; in particular they hold for globally repeating schedules. Positive lower-bound gaps do not require an assumption that the optimum is attained.

## Theorem 1: Exact equality criterion for the elementary bound

The following are equivalent:

1. There exists a feasible repeating schedule with average cost L.
2. The infimum average cost over feasible schedules equals L.
3. For every pair of positive-cost edges e,f such that e is an ancestor of f, q_e divides q_f.

### Sufficiency

For a client v, find its deepest positive-cost ancestor edge e(v). If there is none, serve v daily; its root path has zero cost. Otherwise serve v on every integer multiple of q_e(v). Since q_e(v) is the minimum turnover in a subtree containing v, q_e(v)≤tau_v and the schedule is feasible.

Fix a positive-cost edge e. Every scheduled client below e is assigned to a positive-cost edge f at or below e. Divisibility ensures q_e divides q_f, so every traversal of e occurs on a multiple of q_e. Conversely, choose a client v below e with tau_v=q_e. Its assigned edge f is at or below e; monotonicity of subtree minima and q_f≤tau_v imply q_f=q_e. Hence e is traversed on every multiple of q_e, and precisely on those days. Its average contribution is w_e/q_e.

The whole schedule repeats after the least common multiple of the finitely many q_e. Thus its average is exactly L.

### Necessity for finite repeating schedules

A positive-cost edge must attain its individual lower-bound activation frequency 1/q_e. On a cycle, its positive integer activation gaps are all at most q_e. Their average equals q_e only when every gap equals q_e. Its activation days therefore form a full arithmetic progression of period q_e. For comparable positive-cost edges the descendant progression is contained in the ancestor progression, which forces q_e to divide q_f.

### Necessity even for an unattained infimum

If positive-cost comparable edges have nondividing turnover times, Theorem 2 supplies a strictly positive additive gap above their individual lower bounds. Adding all other edge lower bounds gives OPT≥L+delta>L. Thus an asymptotic sequence of increasingly long cycles cannot evade the criterion.

## Theorem 2: Exact two-edge relaxation and incompatibility penalty

Consider two nested activation sets with maximum gaps a and b, where 1≤a≤b are integers. Let the nonnegative activation costs of the ancestor and descendant be u and v. Put m=floor(b/a) and r=b−ma.

If r=0, their optimum average cost equals u/a+v/b.

If 0<r<a, their optimum average cost is

C2(a,b;u,v) = min { u/a + v/(ma), ((m+1)u+v)/b }

= u/a + v/b + min { A u, B v },

where

A=(a−r)/(ab),   B=r/(mab).

Both alternatives are achieved by finite repeating feasible schedules.

### Lower-bound proof

Partition a cyclic schedule into intervals between consecutive descendant activations. A gap has integer length d∈{1,...,b}. Since ancestor activations have gaps at most a and both interval endpoints activate the ancestor, the interval contains at least ceil(d/a) ancestor activations when counting its right endpoint and excluding its left endpoint. Its charge is therefore at least u ceil(d/a)+v.

The overall average is at least a duration-weighted average of quantities

[u ceil(d/a)+v]/d.

For a fixed value of ceil(d/a), this expression is nonincreasing in d. Its minimum is consequently achieved at d=ka for 1≤k≤m or at d=b. At d=ka it is u/a+v/(ka), nonincreasing in k. Only d=ma and d=b need be retained, giving the formula. For nonperiodic schedules, discard initial/final partial intervals. Their lengths are bounded by b and their bounded costs vanish after division by the horizon.

### Achieving schedules

For d=ma, activate the ancestor every a days and the descendant every ma days.

For d=b, activate the descendant every b days; within each b-day block, activate the ancestor after gaps a,a,...,a,r, where there are m copies of a followed by r. This creates m+1 ancestor activations per b days. When r=0 use only m gaps of a.

The formula remains valid if u or v equals zero. Strict incompatibility requires u,v>0 and r>0.

### Sanity example

For a=2, b=3 and u=v=1, the elementary bound is 1/2+1/3=5/6. Both endpoint constructions cost 1 per day, so C2=1 and the penalty is 1/6. The first schedule activates both daily-equivalent sites every second day; the second activates the ancestor on alternating gaps 2,1 and the descendant every third day. The average gap arithmetic directly rules out cost 5/6.

## Corollary 3: Pooled pairwise lower bound

Let P be the set of ordered pairs (e,f) of positive-cost edges such that e is an ancestor of f and q_e does not divide q_f. For p=(e,f), set a=q_e, b=q_f and define A_p,B_p by Theorem 2.

Compute Z by the rational linear programme

maximise sum_{p in P} z_p

subject to, for every positive-cost edge e,

sum_{p=(e,f)} z_p/A_p + sum_{p=(g,e)} z_p/B_p ≤ w_e,

and z_p≥0.

Then

OPT ≥ L+Z.

The LP has at most |E|(|E|−1)/2 variables and |E| constraints. All its coefficients are positive rationals with polynomial encoding length. It is therefore polynomially solvable in the standard rational bit model.

### Proof

For each pair p=(e,f), allocate u_p=z_p/A_p of edge e's activation cost and v_p=z_p/B_p of edge f's activation cost to this pair. The constraints leave each edge with a nonnegative residual weight. Apply Theorem 2 to every allocated pair and apply the singleton bound to each residual weight. Every original edge weight is counted exactly once. All baseline contributions sum to L. Each pair adds min(A_p u_p,B_p v_p)=z_p. Summing gives L+sum_p z_p, and optimising proves the result.

No scheduling independence or disjointness of the pairs is assumed: these are additive cost allocations applied to the same schedule. Disjoint-pair summation is a valid simpler special case, but the LP can be strictly stronger.

## Independent computational audit

`verification/pair_mean_cycle_audit.py` constructs a finite age-state transition graph independently of the formula. A state records the days since the last ancestor and descendant activations. Actions are neither, ancestor only, or both. It solves a stationary-flow linear programme whose optimum equals the minimum cycle mean.

The audit tested 532 cases: a=1,...,8; b=a,...,13; and cost pairs (1,1),(2,1),(1,2),(3,7),(11,2),(0,1),(1,0). All analytic values matched to floating-point precision. Maximum absolute discrepancy was 1.7763568394002505e−15. This is a numerical cross-check of an exact proof, not a replacement for the proof.

## Theorem 4: Barrier for a common harmonic calendar

The constant 1/ln(2) is asymptotically optimal for the following policy class: assign real service periods p_i≤tau_i such that, for every pair, the larger period divided by the smaller is a positive integer; project each arithmetic event calendar onto integer days by consistently flooring or ceiling. The projection phases may even differ by client. The proof uses only activation frequencies, so phase choices do not affect it. The class includes arbitrary integer-ratio harmonic grids, not only dyadic grids.

This is a limitation of a policy class. It is not an inapproximability theorem for tree replenishment. The witness instances are stars, whose unrestricted optimum is elementary.

### Exact finite integer witnesses

Fix M≥2 and create a star with M leaves. Give the leaves turnover times

M, M+1, ..., 2M−1

and unit activation weights w_i=1 (edge lengths 1/2). Independent exact-turnover schedules give

OPT=L=sum_{q=M}^{2M−1} 1/q.

For any harmonic calendar, let a be the largest assigned real period. Its projected activation density is min(1,1/p), so its effective period is max(1,p).

If a<M, all M effective periods are at most M. The total average cost is therefore at least one.

If a≥M, then a≤2M−1. Exactly ceil(a)−M turnover times are strictly less than a. Each of their assigned periods is strictly below a; harmonicity forces it to be at most a/2. Since a≥2, its effective period is also at most a/2. All other effective periods are at most a. The total average cost is therefore at least

[M + ceil(a)−M]/a = ceil(a)/a ≥ 1.

Assigning all clients period M attains cost one. Thus the optimum within the entire common harmonic-calendar class equals exactly one, and its approximation ratio is

1 / [sum_{q=M}^{2M−1} 1/q] → 1/ln(2).

The elementary harmonic-sum convergence follows, for example, from upper and lower integral sums for 1/x on [M,2M]. Every numerator, turnover and cost in this witness family is rational or integer.

### Interpretation and scope

Allowing bases 3,4,... or an irregular ladder of integer period ratios cannot improve the universal constant while retaining one common harmonic ladder. Additional flexibility such as independently chosen calendars on separate branches can improve these examples. The obstruction therefore motivates exploring multiple calendars, rather than claiming the approximation problem itself is tight.

## Theorem 5: Sharpness for every calendar with a short global cycle

The preceding star family gives a stronger barrier that does not assume harmonic clocks, nested service sets, or any particular calendar representation.

For each M≥2, consider M unit-activation-weight star leaves with turnovers M,M+1,...,2M−1. Any globally repeating feasible calendar with integer cycle length P≤tau_max=2M−1 has average cost at least one.

Indeed, a leaf of turnover q must be served at least ceil(P/q) times per cycle: P is the sum of its cyclic gaps, each at most q. If P<M, every leaf needs at least one service and the total average is at least M/P>1. If M≤P≤2M−1, there are P−M turnover values q<P. Those leaves need at least two visits; the other M−(P−M) leaves need at least one. Therefore the average cost is at least

[2(P−M)+M−(P−M)]/P=1.

Serving all leaves every M days attains one with P=M. Thus the optimum over all calendars with P≤tau_max equals exactly one, whereas the unrestricted optimum is sum_{q=M}^{2M−1}1/q. Their ratio tends to 1/ln(2).

Consequently no algorithm required always to return a repeating calendar with global period at most tau_max can have a universal approximation guarantee smaller than 1/ln(2), even on stars, regardless of computational resources. This is a representation/output-period barrier, not computational hardness of unrestricted replenishment.

More generally, for this star and any prescribed integer P, its exact optimum among P-periodic calendars is

C_M(P)=(1/P) sum_{q=M}^{2M−1} ceil(P/q).

The lower bound was proved above. It is achievable by giving each independent leaf k=ceil(P/q) visits with cyclic gaps floor(P/k) or ceil(P/k). Those gaps are at most q. This expression makes the period restriction explicit; it is not needed for the main approximation proof.

## Focused branch-decomposition attempt

Root child subtrees have additive costs and independent feasibility constraints, so OPT is the sum of their optima. One may optimise separate phases in those subtrees, or apply the equality criterion to solve an attainable component exactly. Superimposing their calendars preserves feasibility and adds their average costs. Therefore this can only improve the cost relative to using one common phase, and it preserves the 1/ln(2) bound.

However, the resulting global cycle is the least common multiple of the component cycles and can exceed tau_max. The short-cycle theorem explains why that extra freedom is necessary to improve its witness family. Interior branch splitting does not retain additive costs because multiple branches share positively weighted paths to the depot. No rigorous uniform improvement below 1/ln(2) for unrestricted tree schedules was established in this focused attempt. No such improvement is claimed.
