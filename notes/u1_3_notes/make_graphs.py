import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

out=Path('/mnt/data/u1_3_notes/figures')
out.mkdir(parents=True, exist_ok=True)

def setup(ax, xlim=(-6,6), ylim=(-6,6), title=None):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect('equal', adjustable='box')
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.set_xticks(range(int(xlim[0]), int(xlim[1])+1, 2))
    ax.set_yticks(range(int(ylim[0]), int(ylim[1])+1, 2))
    ax.grid(True, linewidth=0.5, alpha=0.35)
    ax.tick_params(labelsize=8)
    if title:
        ax.set_title(title, fontsize=10, pad=8, fontweight='bold')

# family set 2x2
fig, axs = plt.subplots(2,2,figsize=(7,7))
x=np.linspace(-5,5,400)
setup(axs[0,0], title='Graph A')
axs[0,0].plot(x, 0.75*x+1.5, lw=2.4)
axs[0,0].text(2.0,4.2,'straight line',fontsize=8)
setup(axs[0,1], title='Graph B')
axs[0,1].plot(x, 0.35*(x-1)**2-3, lw=2.4)
axs[0,1].text(-4.8,3.8,'U-shape',fontsize=8)
setup(axs[1,0], title='Graph C')
axs[1,0].plot(x, np.abs(x+1)-2, lw=2.4)
axs[1,0].text(1.1,3.6,'V-shape',fontsize=8)
setup(axs[1,1], title='Graph D')
axs[1,1].plot(x, 2*(1.55**x)-3, lw=2.4)
axs[1,1].text(-4.6,-2.2,'curves upward',fontsize=8)
fig.tight_layout(pad=2.0)
fig.savefig(out/'u1_3_family_set.png', dpi=180, bbox_inches='tight')
plt.close(fig)

# future graph set similar but unlabeled family names
fig, axs = plt.subplots(2,2,figsize=(7,7))
labels=['Store A','Store B','Store C','Store D']
for ax,label in zip(axs.flat,labels): setup(ax,title=label)
axs[0,0].plot(x, x+1, lw=2.4)
axs[0,1].plot(x, 0.4*x**2-2, lw=2.4)
axs[1,0].plot(x, 1.3*np.abs(x-1)-3, lw=2.4)
axs[1,1].plot(x, 1.8*(1.45**x)-3, lw=2.4)
fig.tight_layout(pad=2.0)
fig.savefig(out/'u1_3_future_graphs.png', dpi=180, bbox_inches='tight')
plt.close(fig)

# single absolute value for example 1 maybe
fig, ax=plt.subplots(figsize=(4.8,4.8))
setup(ax)
ax.plot(x, np.abs(x-2)-3, lw=2.5)
ax.text(2.3,-2.6,'turning point',fontsize=8)
fig.savefig(out/'u1_3_abs_graph.png',dpi=180,bbox_inches='tight')
plt.close(fig)

# table graph comparison linear vs exponential for example 3
fig, axs=plt.subplots(1,2,figsize=(7.4,3.8))
xp=np.array([0,1,2,3,4])
yp1=np.array([2,5,8,11,14])
yp2=np.array([1,2,4,8,16])
for ax,title,yp in zip(axs,['Table A pattern','Table B pattern'],[yp1,yp2]):
    setup(ax,xlim=(-1,5),ylim=(-1,17),title=title)
    ax.plot(xp,yp,marker='o',lw=2.2)
    for xx,yy in zip(xp,yp): ax.text(xx+0.12, yy+0.35, f'({xx},{yy})', fontsize=7)
fig.tight_layout(pad=1.8)
fig.savefig(out/'u1_3_table_patterns.png',dpi=180,bbox_inches='tight')
plt.close(fig)

# nonexample/error comparison: quadratic vs linear context sketch
fig, ax=plt.subplots(figsize=(4.8,4.8))
setup(ax,xlim=(-1,7),ylim=(-1,13))
xx=np.linspace(0,6,200)
ax.plot(xx, 0.3*xx**2+1, lw=2.4, label='curving pattern')
ax.plot(xx, 1.5*xx+1, lw=1.8, linestyle='--', label='straight-line guess')
ax.legend(fontsize=8, loc='upper left')
fig.savefig(out/'u1_3_curve_vs_line.png',dpi=180,bbox_inches='tight')
plt.close(fig)
