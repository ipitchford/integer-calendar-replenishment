"""Fixed-seed synthetic benchmark with an independent exact optimum certificate.

The production calendar and lower bound are compared with an age-state model.
SciPy finds an optimum circulation; a rational cycle and integer potential then
certify that optimum exactly. The finite-state model uses original turnover
constraints, not the production edge-turnover reduction or analytical formulas.

Run from any directory (also under python -I or -O):
    python /absolute/path/src/benchmark_small_trees.py [--out DIR]
Outputs are placed in the sibling data directory unless --out is given.
"""
from __future__ import annotations
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

# python -I does not put the script directory on sys.path; add it explicitly.
sys.path.insert(0,str(Path(__file__).resolve().parent))
from replenishment import TreeInstance, paired_lower_bound

ROOT=Path(__file__).resolve().parents[1]


def require(condition, message):
    """Explicit check that stays active under python -O (-O strips bare checks)."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")


def age_graph(parents, lengths, turnovers):
    """Independent model: all rooted-subtree daily actions and bounded ages."""
    n=len(parents)
    actions={}
    for mask in range(1<<n):
        visited=set()
        for client in range(n):
            if mask & (1<<client):
                node=client+1
                while node:
                    visited.add(node-1)
                    node=parents[node-1]
        mask2=sum(1<<i for i in visited)
        actions[mask2]=sum(2*lengths[i] for i in visited)
    actions=sorted(actions.items())
    initial=(0,)*n
    states=[initial]; ids={initial:0}; queue=deque([initial]); arcs=[]
    while queue:
        state=queue.popleft(); source=ids[state]
        for mask,cost in actions:
            target=tuple(0 if mask&(1<<i) else state[i]+1 for i in range(n))
            if any(target[i]>=turnovers[i] for i in range(n)):
                continue
            if target not in ids:
                ids[target]=len(states);states.append(target);queue.append(target)
            arcs.append((source,ids[target],int(cost),mask))
    return states,arcs


def support_cycle(arcs,flow,state_count):
    """Extract a directed cycle from a positive circulation support."""
    threshold=max(1e-10,float(np.max(flow))*1e-8)
    adj=[[] for _ in range(state_count)]
    for i,((u,v,c,m),x) in enumerate(zip(arcs,flow)):
        if x>threshold:adj[u].append(i)
    # Following any support edge must eventually repeat a vertex, because
    # flow conservation ensures that each reached vertex has an outgoing edge.
    for start in range(state_count):
        if not adj[start]:continue
        positions={};vertices=[];edges=[];u=start
        while u not in positions and adj[u]:
            positions[u]=len(vertices);vertices.append(u)
            k=adj[u][0];edges.append(k);u=arcs[k][1]
        if u in positions:
            return edges[positions[u]:]
    raise AssertionError('No positive-support cycle found')


def certify_potential(arcs,mu,dual_potential,state_count):
    """Integer difference constraints certify no cycle mean below mu."""
    numerator,denominator=mu.numerator,mu.denominator
    potential=[int(math.floor(float(v)*denominator+1e-7)) for v in dual_potential]
    def valid(p):
        return all(p[u]-p[v]<=c*denominator-numerator for u,v,c,_ in arcs)
    if valid(potential):return potential,'reconstructed LP potential'
    # Exact all-source shortest paths in the reversed graph. Each integer
    # inequality is p[u] <= p[v] + c*denominator-numerator.
    reverse=[[] for _ in range(state_count)]
    for u,v,c,_ in arcs:reverse[v].append((u,c*denominator-numerator))
    potential=[0]*state_count;queue=deque(range(state_count));queued=[True]*state_count
    relaxations=0
    while queue:
        v=queue.popleft();queued[v]=False
        for u,w in reverse[v]:
            if potential[u]>potential[v]+w:
                potential[u]=potential[v]+w;relaxations+=1
                if relaxations>state_count*max(1,len(arcs)):
                    raise AssertionError('Failed exact optimum certification')
                if not queued[u]:queue.append(u);queued[u]=True
    require(valid(potential), 'valid(potential)')
    return potential,'integer difference constraints'


def exact_optimum(parents,lengths,turnovers):
    states,arcs=age_graph(parents,lengths,turnovers)
    V,E=len(states),len(arcs)
    rows=[];cols=[];vals=[]
    for k,(u,v,c,mask) in enumerate(arcs):
        rows.extend((u,v,V));cols.extend((k,k,k));vals.extend((1.,-1.,1.))
    matrix=coo_matrix((vals,(rows,cols)),shape=(V+1,E)).tocsc()
    rhs=np.zeros(V+1);rhs[-1]=1
    result=linprog([a[2] for a in arcs],A_eq=matrix,b_eq=rhs,
                   bounds=(0,None),method='highs')
    if not result.success:raise AssertionError(result.message)
    cycle=support_cycle(arcs,result.x,V)
    mu=F(sum(arcs[k][2] for k in cycle),len(cycle))
    if abs(float(mu)-float(result.fun))>1e-7:
        raise AssertionError(('LP cycle mismatch',mu,result.fun))
    potential,method=certify_potential(arcs,mu,result.eqlin.marginals[:-1],V)
    # Direct exact checks of the witness and optimality inequalities.
    for j,k in enumerate(cycle):
        require(arcs[k][1]==arcs[cycle[(j+1)%len(cycle)]][0], 'arcs[k][1]==arcs[cycle[(j+1)%len(cycle)]][0]')
    slack=[c*mu.denominator-mu.numerator-(potential[u]-potential[v])
           for u,v,c,_ in arcs]
    require(min(slack)>=0, 'min(slack)>=0')
    certificate={
        'optimum':str(mu),'cycle_actions':[arcs[k][3] for k in cycle],
        'cycle_state_ids':[arcs[k][0] for k in cycle],
        'potential':potential,'potential_denominator':mu.denominator,
        'states':V,'arcs':E,'certificate_method':method,
        'minimum_integer_dual_slack':min(slack),
        'max_lp_cycle_discrepancy':abs(float(mu)-float(result.fun)),
    }
    return mu,certificate


def instances():
    rng=random.Random(20261031)
    cases=[]
    for n in (2,3,4):
        for family in ('star','path','random'):
            for k in range(20):
                if family=='star':parents=(0,)*n
                elif family=='path':parents=tuple(range(n))
                else:parents=tuple(rng.randrange(i+1) for i in range(n))
                turnovers=tuple(rng.randint(2 if k%2==0 else 1,6) for _ in range(n))
                lengths=tuple(rng.randint(1,9) for _ in range(n))
                if k==19:lengths=(0,)+lengths[1:]
                cases.append((f'{n}_{family}_{k:02}',family,parents,lengths,turnovers))
    special=[
        ((0,1),(1,1),(2,3)),((0,1),(1,4),(2,3)),
        ((0,1),(4,1),(2,3)),((0,1),(1,1),(3,5)),
        ((0,1,2),(1,1,1),(2,3,5)),((0,1,2),(1,4,7),(2,3,5)),
        ((0,1,2),(7,4,1),(2,3,5)),((0,1,1),(1,5,5),(2,3,5)),
        ((0,1,1,3),(2,3,5,7),(2,3,4,5)),
        ((0,0,0,0),(3,4,5,6),(3,4,5,6)),
        ((0,1,2,3),(0,3,0,7),(2,3,4,5)),
        ((0,1,1,3),(1,1,1,1),(1,2,3,6)),
    ]
    for k,(parents,lengths,turnovers) in enumerate(special):
        cases.append((f'special_{k:02}','special',parents,lengths,turnovers))
    return cases


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out',type=Path,default=ROOT/'data',help='output directory (default: bundle data/)')
    args=parser.parse_args(argv)
    started=time.perf_counter();rows=[];certificates=[]
    for ident,family,parents,lengths,turnovers in instances():
        tree=TreeInstance(parents,tuple(F(x) for x in lengths),turnovers)
        cal=tree.calendar();pair=paired_lower_bound(tree);branch=tree.branch_calendar()
        optimum,cert=exact_optimum(parents,lengths,turnovers)
        q=tree.edge_turnovers()
        original=sum((F(2*lengths[i],1<<(q[i].bit_length()-1))
                      for i in range(len(q))),F(0))
        equality=tree.lower_bound_attainable()
        require(cal.lower_bound<=pair['bound']<=optimum<=cal.cost<=original, "cal.lower_bound<=pair['bound']<=optimum<=cal.cost<=original")
        require(optimum<=branch.cost<=cal.cost, 'optimum<=branch.cost<=cal.cost')
        require(equality==(optimum==cal.lower_bound), 'equality==(optimum==cal.lower_bound)')
        require(float(cal.cost/optimum)<=1/math.log(2)+1e-12, 'float(cal.cost/optimum)<=1/math.log(2)+1e-12')
        # Independently execute one cycle of the production calendar, including
        # incidental visits to ancestors, to check its claimed average cost.
        direct_cost=F(0)
        for day in range(1,cal.cycle+1):
            direct_cost+=tree.cost(cal.active(day))
        require(direct_cost/cal.cycle==cal.cost, 'direct_cost/cal.cycle==cal.cost')
        require(sum((tree.cost(branch.active(t)) for t in range(1,branch.cycle+1)),F(0))/branch.cycle==branch.cost, 'sum((tree.cost(branch.active(t)) for t in range(1,branch.cycle+1)),F(0))/branch.cycle==branch.cost')
        row={'id':ident,'family':family,'n':len(q),
             'parents':json.dumps(parents),'lengths':json.dumps(lengths),
             'turnovers':json.dumps(turnovers),'edge_turnovers':json.dumps(q),
             'optimum_exact':str(optimum),'calendar_exact':str(cal.cost),
             'branch_calendar_exact':str(branch.cost),
             'original_dyadic_exact':str(original),'elementary_bound_exact':str(cal.lower_bound),
             'paired_bound_exact':str(pair['bound']),'alpha':str(cal.alpha),
             'cycle':cal.cycle,'lower_bound_equality':equality,
             'calendar_to_optimum':float(cal.cost/optimum),
             'branch_calendar_to_optimum':float(branch.cost/optimum),
             'original_to_optimum':float(original/optimum),
             'paired_to_optimum':float(pair['bound']/optimum),
             'elementary_to_optimum':float(cal.lower_bound/optimum),
             'states':cert['states'],'arcs':cert['arcs']}
        rows.append(row)
        certificates.append({'id':ident,'parents':list(parents),'lengths':list(lengths),
                             'turnovers':list(turnovers),'exact_optimum_certificate':cert,
                             'paired_lower_bound_witness':pair['witness']})
    elapsed=time.perf_counter()-started
    cal_ratios=[r['calendar_to_optimum'] for r in rows]
    old_ratios=[r['original_to_optimum'] for r in rows]
    branch_ratios=[r['branch_calendar_to_optimum'] for r in rows]
    worst=max(rows,key=lambda r:r['calendar_to_optimum'])
    summary={
        'purpose':'Fixed-seed synthetic correctness and comparative benchmark; not a representative logistics dataset.',
        'seed':20261031,'instances':len(rows),'exact_optima_certified':len(rows),
        'random_instances':180,'constructed_instances':12,
        'minimum_n':min(r['n'] for r in rows),'maximum_n':max(r['n'] for r in rows),
        'maximum_turnover':6,'maximum_states':max(r['states'] for r in rows),
        'maximum_arcs':max(r['arcs'] for r in rows),
        'calendar_ratio_mean':statistics.mean(cal_ratios),
        'calendar_ratio_median':statistics.median(cal_ratios),
        'calendar_ratio_max':max(cal_ratios),
        'branch_calendar_ratio_mean':statistics.mean(branch_ratios),
        'branch_calendar_ratio_median':statistics.median(branch_ratios),
        'branch_calendar_ratio_max':max(branch_ratios),
        'branch_calendar_exact_optima':sum(F(r['branch_calendar_exact'])==F(r['optimum_exact']) for r in rows),
        'original_ratio_mean':statistics.mean(old_ratios),
        'original_ratio_median':statistics.median(old_ratios),
        'original_ratio_max':max(old_ratios),
        'strict_calendar_improvements':sum(F(r['calendar_exact'])<F(r['original_dyadic_exact']) for r in rows),
        'calendar_exact_optima':sum(F(r['calendar_exact'])==F(r['optimum_exact']) for r in rows),
        'original_exact_optima':sum(F(r['original_dyadic_exact'])==F(r['optimum_exact']) for r in rows),
        'elementary_bound_exact_optima':sum(r['lower_bound_equality'] for r in rows),
        'paired_bound_exact_optima':sum(F(r['paired_bound_exact'])==F(r['optimum_exact']) for r in rows),
        'strict_pair_bound_improvements':sum(F(r['paired_bound_exact'])>F(r['elementary_bound_exact']) for r in rows),
        'all_lower_bound_equality_predictions_correct':True,
        'all_calendar_cycles_checked_exactly':True,
        'worst_calendar_instance':worst,
        'elapsed_seconds':elapsed,
    }
    data=args.out;data.mkdir(parents=True,exist_ok=True)
    with (data/'small_tree_benchmark.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (data/'small_tree_benchmark.json').write_text(json.dumps(summary,indent=2)+'\n')
    (data/'small_tree_exact_certificates.json').write_text(json.dumps(certificates,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
