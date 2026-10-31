"""Regenerate publication figures from the saved verification data."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/replenishment-matplotlib')
from fractions import Fraction as F
import csv
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, ScalarFormatter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
PLUM, RUST, OLIVE, INK = '#70466F', '#B46136', '#768044', '#30323B'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
    'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':INK,
    'text.color':INK,'xtick.color':INK,'ytick.color':INK,'axes.edgecolor':'#8A8A8A',
    'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white',
    'axes.titleweight':'bold','grid.color':'#DEDEDE','grid.linewidth':0.65})

rows = list(csv.DictReader((ROOT/'data/small_tree_benchmark.csv').open()))
fig, ax = plt.subplots(figsize=(7.2,4.2))
for field,label,color in [
    ('original_to_optimum','Power-of-two calendar (Bosman et al.)',RUST),
    ('calendar_to_optimum','Single-phase calendar (Theorem 1)',PLUM),
    ('branch_calendar_to_optimum','Separate depot branches',OLIVE)]:
    values = np.sort([float(r[field]) for r in rows])
    ax.step(np.r_[0.985,values,1.52], np.r_[0,np.arange(1,len(values)+1)/len(values),1],
            where='post',label=label,color=color,lw=2.25)
ax.axvline(1/math.log(2),color=INK,ls=':',lw=1.2)
ax.text(1/math.log(2)-0.006,0.16,'Universal guarantee\n1 / ln 2',rotation=90,
        ha='right',va='bottom',fontsize=9,color=INK)
ax.set_xlim(0.985,1.52);ax.set_ylim(0,1.025)
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.set_xlabel('Calendar cost / exact optimum')
ax.set_ylabel('Share of the 192 instances at or below this ratio')
ax.set_title('Exactly certified small-tree comparison',loc='left',pad=14)
ax.grid(axis='y',alpha=.8)
ax.legend(loc='lower right',frameon=False,fontsize=9)
fig.text(.11,.015,'Synthetic cases: 2–4 clients; turnover times 1–6 days. Descriptive, not a population estimate.',
         fontsize=8,color='#5D5D5D')
fig.tight_layout(rect=(0,.05,1,1))
fig.savefig(OUT/'benchmark_ecdf.pdf',bbox_inches='tight')
fig.savefig(OUT/'benchmark_ecdf.png',dpi=200,bbox_inches='tight')
plt.close(fig)

Ms = [2**k for k in range(0,13)]
ratios = [1/sum(1/q for q in range(M,2*M)) for M in Ms]
fig, ax = plt.subplots(figsize=(7.2,3.8))
ax.plot(Ms,ratios,color=PLUM,lw=2.2,marker='o',ms=4)
limit = 1/math.log(2)
ax.axhline(limit,color=RUST,ls='--',lw=1.6)
ax.text(1.2,limit+.014,'Sharp class limit: 1 / ln 2 = 1.442695…',color=RUST,fontsize=9)
ax.set_xscale('log',base=2);ax.set_xticks([1,4,16,64,256,1024,4096]);ax.xaxis.set_major_formatter(ScalarFormatter())
ax.set_ylim(.97,1.50);ax.set_xlim(.9,5000)
ax.set_xlabel('Number of star leaves, M')
ax.set_ylabel('Best restricted calendar / exact optimum')
ax.set_title('The sharp price of a short global cycle',loc='left',pad=12)
ax.grid(axis='y',alpha=.8)
fig.text(.11,.015,'Unit activation weights; turnover times M, M+1, …, 2M−1. Independent clocks solve each star exactly.',
         fontsize=8,color='#5D5D5D')
fig.tight_layout(rect=(0,.05,1,1))
fig.savefig(OUT/'harmonic_class_limit.pdf',bbox_inches='tight')
fig.savefig(OUT/'harmonic_class_limit.png',dpi=200,bbox_inches='tight')
plt.close(fig)

def g(h):
    a, b = math.floor(h/2), math.floor(h)
    return sum(1/j for j in range(a+1,b+1))+(1+2*a-b)/h

hs=np.linspace(1,12,1101)
fig,ax=plt.subplots(figsize=(7.2,3.8))
ax.plot(hs,[g(h)/math.log(2) for h in hs],color=PLUM,lw=2.3)
for h,y,label in [(1.5,1/math.log(2),'1.4427'),(3.5,5/(6*math.log(2)),'1.2022'),
                  (5.5,47/(60*math.log(2)),'1.1301')]:
    ax.annotate(label,(h,y),xytext=(0,11),textcoords='offset points',ha='center',color=PLUM,fontsize=9)
ax.axhline(1,color=OLIVE,ls='--',lw=1.3)
ax.text(8.8,1.015,'Unrestricted optimum',color=OLIVE,fontsize=9)
ax.set_xlim(1,12);ax.set_ylim(.985,1.50)
ax.set_xticks(range(1,13))
ax.set_xlabel('Allowed global cycle / M, in the large-M limit')
ax.set_ylabel('Constrained cost / unrestricted optimum')
ax.set_title('Longer calendars reduce the unavoidable cost on these stars',loc='left',pad=12)
ax.grid(axis='y',alpha=.8)
fig.text(.11,.015,'The largest turnover is approximately 2M. This is an exact asymptotic witness-family profile.',
         fontsize=8,color='#5D5D5D')
fig.tight_layout(rect=(0,.05,1,1))
fig.savefig(OUT/'cycle_budget_profile.pdf',bbox_inches='tight')
fig.savefig(OUT/'cycle_budget_profile.png',dpi=200,bbox_inches='tight')
plt.close(fig)
print(json.dumps({'figures':['benchmark_ecdf','harmonic_class_limit','cycle_budget_profile'],
                  'instances':len(rows),'limit':limit,'maximum_M':max(Ms)}))

# Calendar picture for the three-day example (Section 4.1).
from matplotlib.patches import Rectangle
def calendar_rows(periods, days):
    return [[1 if (t // p if p >= 1 else t) > ((t - 1) // p if p >= 1 else t - 1) else 0
             for t in range(1, days + 1)] for p in periods]
def frac_rows(periods, days):
    out = []
    for p in periods:
        p = F(p)
        out.append([1 if math.floor(t / p) > math.floor((t - 1) / p) else 0 for t in range(1, days + 1)])
    return out
days = 12
panels = [('Power-of-two calendar: both clients every 2 days (cost 3 per day)', frac_rows([2, 2], days)),
          ('Integer calendar at phase 3/2: clocks 3/2 and 3 (cost 8/3 per day)', frac_rows([F(3, 2), 3], days))]
fig, axes = plt.subplots(2, 1, figsize=(7.2, 3.2))
for ax, (title, rows_) in zip(axes, panels):
    for r, row in enumerate(rows_):
        for t, v in enumerate(row):
            ax.add_patch(Rectangle((t, 1 - r), 0.9, 0.8, color=PLUM if v else '#EEEAEE', lw=0))
    ax.set_xlim(0, days); ax.set_ylim(-0.1, 2)
    ax.set_yticks([0.4, 1.4]); ax.set_yticklabels(['Far client (τ = 3)', 'Near client (τ = 2)'], fontsize=8.5)
    ax.set_xticks([t + 0.45 for t in range(days)]); ax.set_xticklabels([str(t + 1) for t in range(days)], fontsize=8)
    ax.tick_params(length=0)
    for side in ('left', 'bottom'):
        ax.spines[side].set_visible(False)
    ax.set_title(title, loc='left', fontsize=9.5, pad=4)
axes[1].set_xlabel('Day')
fig.tight_layout()
fig.savefig(OUT / 'calendar_example.pdf', bbox_inches='tight')
fig.savefig(OUT / 'calendar_example.png', dpi=200, bbox_inches='tight')
plt.close(fig)
