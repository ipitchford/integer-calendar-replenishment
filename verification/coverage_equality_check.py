"""Bounded exact audit of the weighted-coverage equality criterion.

A separately constructed age-state optimisation supplies exact cycle/potential
certificates. The criterion itself is checked against those optima. This is a
synthetic mathematical check, not an empirical logistics benchmark.
Every case retains its full certificate for the separate standard-library
verifier in verify_coverage_certificates.py.
"""
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import math
import random
import sys

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from benchmark_small_trees import support_cycle, certify_potential


def require(condition, message):
    """Explicit check that stays active under python -O (-O strips bare checks)."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")


def feature_cost(mask,features,weights):
    return sum(w for feature,w in zip(features,weights) if mask&feature)


def exact_optimum(turnovers,features,weights):
    n=len(turnovers);initial=(0,)*n
    states=[initial];ids={initial:0};queue=deque([initial]);arcs=[]
    actions=[(mask,feature_cost(mask,features,weights)) for mask in range(1<<n)]
    while queue:
        state=queue.popleft();u=ids[state]
        for mask,cost in actions:
            target=tuple(0 if mask&(1<<i) else state[i]+1 for i in range(n))
            if any(target[i]>=turnovers[i] for i in range(n)):continue
            if target not in ids:
                ids[target]=len(states);states.append(target);queue.append(target)
            arcs.append((u,ids[target],cost,mask))
    V,E=len(states),len(arcs);rows=[];cols=[];values=[]
    for k,(u,v,c,m) in enumerate(arcs):
        rows.extend((u,v,V));cols.extend((k,k,k));values.extend((1.,-1.,1.))
    matrix=coo_matrix((values,(rows,cols)),shape=(V+1,E)).tocsc()
    rhs=np.zeros(V+1);rhs[-1]=1
    result=linprog([a[2] for a in arcs],A_eq=matrix,b_eq=rhs,bounds=(0,None),method='highs')
    require(result.success, result.message)
    cycle=support_cycle(arcs,result.x,V)
    mu=F(sum(arcs[k][2] for k in cycle),len(cycle))
    require(abs(float(mu)-float(result.fun))<1e-7, 'abs(float(mu)-float(result.fun))<1e-7')
    potential,method=certify_potential(arcs,mu,result.eqlin.marginals[:-1],V)
    require(all(potential[u]-potential[v]<=c*mu.denominator-mu.numerator for u,v,c,_ in arcs), 'all(potential[u]-potential[v]<=c*mu.denominator-mu.numerator for u,v,c,_ in arcs)')
    return mu,{'optimum':str(mu),'states':V,'arcs':E,
               'cycle_actions':[arcs[k][3] for k in cycle],
               'cycle_state_ids':[arcs[k][0] for k in cycle],
               'potential':potential,'potential_denominator':mu.denominator,'method':method}


def criterion(turnovers,features,weights):
    n=len(turnovers);h=[1]*n;L=F(0)
    for feature,w in zip(features,weights):
        if not w:continue
        q=min(turnovers[i] for i in range(n) if feature&(1<<i))
        L+=F(w,q)
        for i in range(n):
            if feature&(1<<i):h[i]=math.lcm(h[i],q)
    return all(a<=b for a,b in zip(h,turnovers)),h,L


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out',type=Path,default=ROOT/'data',help='output directory (default: bundle data/)')
    args=parser.parse_args(argv)
    rng=random.Random(20261101)
    cases=[('overlap_six',(2,3,6),(0b101,0b110),(1,1)),
           ('overlap_five',(2,3,5),(0b101,0b110),(1,1)),
           ('uncovered_client',(2,3,5),(0b001,0b010),(2,3)),
           ('zero_features',(2,3,5),(0b101,0b110),(0,0))]
    for n in (3,4):
        for k in range(48):
            turnovers=tuple(rng.randint(2 if k%2==0 else 1,6) for _ in range(n))
            count=rng.randint(2,min(6,(1<<n)-1))
            features=tuple(sorted(rng.sample(range(1,1<<n),count)))
            weights=tuple(rng.randint(0,5) for _ in features)
            cases.append((f'random_{n}_{k:02}',turnovers,features,weights))
    records=[]
    for ident,turnovers,features,weights in cases:
        predicted,h,L=criterion(turnovers,features,weights)
        opt,cert=exact_optimum(turnovers,features,weights)
        require(opt>=L, 'opt>=L')
        require(predicted==(opt==L), (ident,turnovers,features,weights,h,L,opt))
        cycle=None
        if predicted:
            cycle=math.lcm(*h)
            costs=[]
            for day in range(1,cycle+1):
                mask=sum(1<<i for i,p in enumerate(h) if day%p==0)
                costs.append(feature_cost(mask,features,weights))
            require(F(sum(costs),cycle)==L, 'F(sum(costs),cycle)==L')
            require(all(p<=tau for p,tau in zip(h,turnovers)), 'all(p<=tau for p,tau in zip(h,turnovers))')
        record={'id':ident,'turnovers':turnovers,'feature_masks':features,'weights':weights,
                'client_lcms':h,'predicted_equality':predicted,'lower_bound':str(L),
                'exact_optimum':str(opt),'constructed_cycle':cycle,
                'states':cert['states'],'arcs':cert['arcs'],'certificate':cert}
        records.append(record)
    summary={'purpose':'Bounded synthetic proof check of explicit weighted-coverage equality criterion.',
             'seed':20261101,'cases':len(records),'exact_optima_certified':len(records),
             'complete_certificates_stored':len(records),
             'correct_predictions':len(records),'equality_cases':sum(r['predicted_equality'] for r in records),
             'strict_gap_cases':sum(not r['predicted_equality'] for r in records),
             'maximum_states':max(r['states'] for r in records),
             'maximum_arcs':max(r['arcs'] for r in records),
             'overlap_six_optimum':records[0]['exact_optimum'],
             'overlap_five_optimum':records[1]['exact_optimum']}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'coverage_equality_checks.json').write_text(json.dumps({'summary':summary,'records':records},indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
