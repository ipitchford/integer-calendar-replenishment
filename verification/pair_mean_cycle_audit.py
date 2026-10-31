from collections import deque
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog


def require(condition, message):
    """Explicit check that stays active under python -O (-O strips bare checks)."""
    if not condition:
        raise SystemExit(f"CHECK FAILED: {message}")

def independent_mean_cycle(a,b,x,y):
    states=[(0,0)]; index={(0,0):0}; q=deque(states); arcs=[]
    while q:
        s=q.popleft(); u=index[s]
        for visit in range(3):
            t=(0 if visit>=1 else s[0]+1, 0 if visit>=2 else s[1]+1)
            if t[0]>=a or t[1]>=b: continue
            if t not in index:
                index[t]=len(states); states.append(t); q.append(t)
            arcs.append((u,index[t], (x if visit>=1 else 0)+(y if visit>=2 else 0)))
    A=np.zeros((len(states)+1,len(arcs)))
    for k,(u,v,c) in enumerate(arcs):
        A[u,k]+=1;A[v,k]-=1;A[-1,k]=1
    rhs=np.zeros(len(states)+1);rhs[-1]=1
    res=linprog([z[2] for z in arcs],A_eq=A,b_eq=rhs,bounds=(0,None),method='highs')
    require(res.success, 'res.success')
    return res.fun

def formula(a,b,x,y):
    m=b//a
    return min(Fraction(x,a)+Fraction(y,m*a),Fraction((m+1)*x+y,b)) if b%a else Fraction(x,a)+Fraction(y,b)

count=0; worst=0
for a in range(1,9):
    for b in range(a,14):
        for x,y in [(1,1),(2,1),(1,2),(3,7),(11,2),(0,1),(1,0)]:
            f=float(formula(a,b,x,y)); v=independent_mean_cycle(a,b,x,y)
            err=abs(f-v);worst=max(worst,err);count+=1
            require(err<1e-8, (a,b,x,y,f,v))
print({'tested':count,'max_abs_error':worst})
