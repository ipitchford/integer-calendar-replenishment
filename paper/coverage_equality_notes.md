# Equality in the frequency lower bound for explicit weighted coverage costs

This note establishes a precise extension of the tree divisibility criterion. It makes no historical-priority claim.

## Model

Let N be a finite set of clients with integer turnover times tau_i≥1. Let A be an explicitly given finite family of nonempty subsets of N, with weights w_A≥0. The daily service cost is

f(S)=sum_A w_A 1{S intersects A}.

A feature A is active whenever at least one client in A is served. Discard zero-weight features when applying the criterion. For every positive-weight feature let

q_A=min_{i in A} tau_i,

and define

L=sum_A w_A/q_A.

The contribution of each feature enters the sorted greedy lower bound at its first client. Thus L is also the greedy submodular bound in the main manuscript.

For each client i define

h_i=lcm{q_A : w_A>0 and i in A},

where the least common multiple of an empty family is one.

## Theorem

The following statements are equivalent:

1. OPT=L, where OPT is the infimum average cost over feasible repeating schedules.
2. A feasible repeating schedule of cost exactly L exists.
3. h_i≤tau_i for every client i.

When these conditions hold, serving client i on every multiple of h_i is an exact optimum. The condition is decidable in polynomial time in the explicit coverage-family input size and bit length. The resulting constant-gap schedule has a compact descriptor even if its overall cycle is large.

### Preliminary fact: a finite optimum exists

For any fixed finite cost function and integer turnover vector, the minimum average is attained by a repeating schedule. After each day record each client's age, meaning the number of days since its last service. Feasible states have 0≤age_i<tau_i. A service set resets its clients' ages to zero and increments the other ages; retain only valid transitions and give each transition the cost of its service set.

This is a finite directed graph with a nonempty cycle (serve everybody every day). Every repeating feasible schedule gives a closed state walk after its finite initial transient. A closed walk's mean cost is a duration-weighted average of its constituent directed cycles. Conversely, each directed cycle defines a repeating feasible schedule, including across its boundary. The minimum cycle mean is therefore OPT and is attained. Starting with all clients freshly supplied does not obstruct such a cycle: its action sequence remains feasible from the all-zero age state, and after every client has first been served the recorded ages agree with the cycle's ages.

The same minimum bounds the limiting inferior average of any infinite feasible schedule: decompose its finite prefixes into cycles and a remaining simple path of bounded length. Thus allowing a nonperiodic schedule cannot evade a strict lower-bound gap.

### Proof of necessity

For a positive-weight feature A, a client attaining q_A must be served at least once in every q_A consecutive days. Consequently A's activation gaps are at most q_A and its activation density is at least 1/q_A. These feature bounds sum to L.

If a repeating schedule has total cost L, every positive-weight feature attains its own density bound. All its integer activation gaps must then equal q_A: their average cannot equal q_A while any is strictly shorter. Its active days form a full arithmetic progression of period q_A.

Every service day of client i belongs to every feature progression containing i. Their intersection must be nonempty and is itself an arithmetic progression of period h_i. A subsequence of such a progression cannot have all gaps at most tau_i unless h_i≤tau_i. This proves (2) implies (3). The finite-optimum fact proves that (1) implies (2).

### Proof of sufficiency

Assume h_i≤tau_i for every i and serve client i on all positive multiples of h_i. This meets each rolling deadline. For a positive-weight feature A, q_A divides every h_i with i in A, so A is active only on multiples of q_A.

Choose i_A in A with tau_i_A=q_A. Its h_i_A is a multiple of q_A and satisfies h_i_A≤tau_i_A=q_A, so h_i_A=q_A. Hence A is active on every multiple of q_A, as well as only on those days. Its density is exactly 1/q_A. Summing gives cost L.

The schedule repeats after lcm_i h_i. Computing all h_i uses integer gcd/lcm arithmetic; the bit length of any intermediate least common multiple is bounded by the sum of input bit lengths. During the decision test, values can also be capped once they exceed tau_i. The compact schedule stores one integer h_i per client. This proves (3) implies (2), and (2) implies (1) follows from the lower bound.

## Relation to the tree criterion

For tree routing, feature sets are descendant-client sets and their weights are twice the edge lengths. These sets are laminar. If every positive-cost ancestor edge's turnover divides every positive-cost descendant edge's turnover, the relevant periods for each client form a divisibility chain, and their least common multiple is the largest, which is no greater than that client's turnover.

Conversely, suppose positive-cost ancestor and descendant edges have periods a,b with a not dividing b. A client attaining the descendant minimum has turnover b and belongs to both features. Its h_i is at least lcm(a,b)>b, so the coverage condition fails. The general criterion therefore recovers exactly the tree divisibility criterion.

## An overlapping-feature example

Take three clients with turnover vector (2,3,6), two unit-weight features A={1,3} and B={2,3}, and feature periods q_A=2,q_B=3. The client periods are h=(2,3,6), so serving on these exact periods attains L=1/2+1/3=5/6.

Changing only the third turnover from six to five leaves the feature lower bound unchanged but violates h_3≤tau_3. Thus the lower bound is strictly unattainable. The independent finite-state calculation in the accompanying check gives optimum one for this second instance.

## Scope

This criterion requires an explicit weighted coverage representation. A general monotone submodular value oracle need not supply such a representation, and the theorem does not claim that all monotone submodular functions are coverage functions. The result is an exact recognisable subclass and a useful structural extension of the tree result.
