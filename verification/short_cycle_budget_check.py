"""Exact bounded checks for the output-cycle barrier and horizon profile."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import csv
import json
import math

ROOT=Path(__file__).resolve().parents[1]


def require(condition, message):
    """Explicit check that stays active under python -O (-O strips bare checks)."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")

def ceil_div(a,b):return (a+b-1)//b

def H(n):return sum((F(1,k) for k in range(1,n+1)),F(0))

def g(t):
    t=F(t);a=t.numerator//(2*t.denominator);b=t.numerator//t.denominator
    return H(b)-H(a)+F(1+2*a-b,1)/t

def C(M,P):return F(sum(ceil_div(P,q) for q in range(M,2*M)),P)

def minimum_count_by_enumeration(P,q):
    best=P+1
    for mask in range(1,1<<P):
        count=mask.bit_count()
        if count>=best:continue
        days=[i for i in range(P) if mask&(1<<i)]
        gaps=[days[i+1]-days[i] for i in range(len(days)-1)]+[days[0]+P-days[-1]]
        if max(gaps)<=q:best=count
    return best

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out',type=Path,default=ROOT/'data',help='output directory (default: bundle data/)')
    args=parser.parse_args(argv)
    enumeration_cases=0
    for P in range(1,11):
        for q in range(2,13):
            require(minimum_count_by_enumeration(P,q)==ceil_div(P,q), 'minimum_count_by_enumeration(P,q)==ceil_div(P,q)')
            enumeration_cases+=1
    period_cases=0;budget_cases=0;selected=[]
    Ms=list(range(2,21))+[32,64,128]
    for M in Ms:
        values=[];last_g=None;best=None
        for P in range(1,8*M+1):
            value=C(M,P);limit=g(F(P,M))
            require(F(0)<=value-limit<=F(1,M), 'F(0)<=value-limit<=F(1,M)')
            if last_g is not None:require(limit<=last_g, 'limit<=last_g')
            last_g=limit;values.append(value)
            best=value if best is None else min(best,value)
            require(limit<=best<=limit+F(1,M), 'limit<=best<=limit+F(1,M)')
            if P<=2*M-1:require(value>=1, 'value>=1')
            if M<=P<=2*M-1:require(value==1, 'value==1')
            period_cases+=1;budget_cases+=1
        require(min(values[:2*M-1])==1, 'min(values[:2*M-1])==1')
        S=sum((F(1,q) for q in range(M,2*M)),F(0))
        if M in (2,8,32,128):
            for h in (1,2,3,4,5,6,8):
                best=min(values[:h*M])
                selected.append({'M':M,'h':h,'budget':h*M,'best_cost':str(best),
                                 'unrestricted_optimum':str(S),'ratio':float(best/S),
                                 'limiting_cost':str(g(h)),'limiting_ratio':float(g(h))/math.log(2)})
    require(g(1)==g(2)==1, 'g(1)==g(2)==1')
    require(g(3)==g(4)==F(5,6), 'g(3)==g(4)==F(5,6)')
    require(g(5)==g(6)==F(47,60), 'g(5)==g(6)==F(47,60)')
    require(g(7)==g(8)==F(319,420), 'g(7)==g(8)==F(319,420)')
    # Verify the pointwise threshold-integral identity at all half-integers.
    for numerator in range(1,33):
        t=F(numerator,2)
        integral=F(1)+sum((max(F(0),min(F(2),t/k)-1) for k in range(1,math.ceil(t)+1)),F(0))
        require(integral/t==g(t), 'integral/t==g(t)')
    data=args.out;data.mkdir(parents=True,exist_ok=True)
    summary={'binary_cycle_enumeration_cases':enumeration_cases,
             'finite_period_cases':period_cases,'finite_budget_cases':budget_cases,
             'star_sizes':Ms,'all_exact_checks_passed':True,
             'scope':'Synthetic exact arithmetic; unrestricted star optimum known exactly.'}
    (data/'short_cycle_budget_checks.json').write_text(json.dumps({'summary':summary,'selected_limits':selected},indent=2)+'\n')
    with (data/'period_budget_limit.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['h','cycle_multiple_of_tau_max','limiting_cost_exact','limiting_ratio'])
        writer.writeheader()
        for numerator in range(1,65):
            h=F(numerator,4)
            writer.writerow({'h':float(h),'cycle_multiple_of_tau_max':float(h/2),
                             'limiting_cost_exact':str(g(h)),'limiting_ratio':float(g(h))/math.log(2)})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
