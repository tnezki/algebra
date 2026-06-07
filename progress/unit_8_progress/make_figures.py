import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
out = Path('/mnt/data/unit_8_progress/figures')
out.mkdir(parents=True, exist_ok=True)

def setup_axes(ax, xlim=(-10,10), ylim=(-10,10), xlabel='x', ylabel='y'):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect('equal', adjustable='box')
    ax.spines['left'].set_position('zero'); ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none'); ax.spines['top'].set_color('none')
    majorx=np.arange(np.ceil(xlim[0]/5)*5, xlim[1]+1, 5)
    majory=np.arange(np.ceil(ylim[0]/5)*5, ylim[1]+1, 5)
    minorx=np.arange(np.ceil(xlim[0]), xlim[1]+1, 1)
    minory=np.arange(np.ceil(ylim[0]), ylim[1]+1, 1)
    ax.set_xticks(majorx); ax.set_yticks(majory)
    ax.set_xticks(minorx, minor=True); ax.set_yticks(minory, minor=True)
    ax.grid(which='minor', linewidth=0.35, alpha=0.35)
    ax.grid(which='major', linewidth=0.8, alpha=0.7)
    ax.tick_params(labelsize=8)
    ax.set_xlabel(xlabel, loc='right', fontsize=9)
    ax.set_ylabel(ylabel, loc='top', fontsize=9, rotation=0)

def save(fig, name):
    fig.savefig(out/name, dpi=160, bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)

# 1 mixed family graphs - separated into a clear 2x2 grid
# Each family gets its own small coordinate plane so labels and shapes are readable.
fig,axs=plt.subplots(2,2,figsize=(5.2,5.2),constrained_layout=True)
families=[
    ('A', lambda t: t+1, 'linear', (-5,5), (-5,6), '-'),
    ('B', lambda t: t**2-3, 'quadratic', (-5,5), (-5,10), '--'),
    ('C', lambda t: 2**t-2, 'exponential', (-5,5), (-5,10), ':'),
    ('D', lambda t: np.abs(t)-1, 'absolute value', (-5,5), (-5,6), '-.'),
]
for ax,(label,func,name,xlim,ylim,style) in zip(axs.flat,families):
    setup_axes(ax, xlim, ylim)
    xx=np.linspace(xlim[0],xlim[1],400)
    yy=func(xx)
    ax.plot(xx, yy, linewidth=1.9, linestyle=style, color='black')
    ax.text(0.04,0.92,label,transform=ax.transAxes,fontsize=13,fontweight='bold',
            bbox=dict(boxstyle='square,pad=0.15',facecolor='white',edgecolor='none'))
    # Keep panel titles out of the prompt logic; labels A-D are what students match.
save(fig,'unit8_family_sort.png')

# 2 transformation quadratic
x=np.linspace(-6,6,400)
fig,ax=plt.subplots(figsize=(4,4))
setup_axes(ax, (-6,6), (-4,10))
ax.plot(x, x**2, linewidth=1.6, linestyle='--')
ax.plot(x, (x-2)**2+1, linewidth=1.9)
ax.text(-2.8,7.5,'parent',fontsize=9)
ax.text(2.5,2.0,'transformed',fontsize=9)
save(fig,'unit8_quadratic_transform.png')

# 3 absolute value
x=np.linspace(-8,8,400)
fig,ax=plt.subplots(figsize=(4,4))
setup_axes(ax, (-8,8), (-2,10))
y=2*np.abs(x-1)+2
ax.plot(x,y,linewidth=1.8)
ax.plot([1],[2],'ko')
ax.text(1.2,2.2,'vertex',fontsize=9)
save(fig,'unit8_absolute_value.png')

# 4 scatter quadratic trend
rng=np.random.default_rng(4)
x=np.linspace(-5,5,17)
y=0.45*x**2+1+rng.normal(0,0.8,len(x))
fig,ax=plt.subplots(figsize=(4,4))
setup_axes(ax, (-6,6), (-2,16))
ax.scatter(x,y,s=22,color='black')
xx=np.linspace(-5.5,5.5,200)
ax.plot(xx,0.45*xx**2+1,linewidth=1.4,linestyle='--')
save(fig,'unit8_quadratic_scatter.png')

# 5 residual pattern
x=np.arange(1,11); res=np.array([-3,-1,1,2,3,2,1,-1,-2,-3])
fig,ax=plt.subplots(figsize=(4,4))
ax.axhline(0,color='black',linewidth=1)
ax.set_xlim(0,11); ax.set_ylim(-5,5); ax.set_aspect('auto')
ax.set_xticks([0,5,10]); ax.set_yticks([-5,0,5])
ax.set_xticks(np.arange(0,12,1), minor=True); ax.set_yticks(np.arange(-5,6,1), minor=True)
ax.grid(which='minor', linewidth=0.35, alpha=0.35); ax.grid(which='major', linewidth=0.8, alpha=0.7)
ax.scatter(x,res,s=24,color='black')
ax.set_xlabel('x', fontsize=9); ax.set_ylabel('residual', fontsize=9)
save(fig,'unit8_residual_pattern.png')

# 6 mixed comparison linear vs exp
x=np.linspace(0,8,300)
fig,ax=plt.subplots(figsize=(4,4))
setup_axes(ax, (0,10), (0,30), xlabel='time', ylabel='value')
ax.plot(x, 2*x+5, linewidth=1.8)
ax.plot(x, 3*(1.35**x), linewidth=1.8, linestyle='--')
ax.text(6.5,19,'A',fontsize=10,fontweight='bold')
ax.text(6.5,26,'B',fontsize=10,fontweight='bold')
save(fig,'unit8_linear_exp_compare.png')

# 7 model choice scatter exponential
# Use a square plot box instead of equal data-unit aspect, since the units differ.
x=np.arange(0,8); y=2*(1.55**x)+rng.normal(0,1.2,len(x))
fig,ax=plt.subplots(figsize=(4,4))
ax.set_xlim(0,8); ax.set_ylim(0,55)
ax.set_box_aspect(1)
ax.spines['left'].set_position(('data',0)); ax.spines['bottom'].set_position(('data',0))
ax.spines['right'].set_color('none'); ax.spines['top'].set_color('none')
ax.set_xticks(np.arange(0,9,1)); ax.set_yticks(np.arange(0,56,5))
ax.set_xticks(np.arange(0,8.5,0.5), minor=True); ax.set_yticks(np.arange(0,56,1), minor=True)
ax.grid(which='minor', linewidth=0.35, alpha=0.30)
ax.grid(which='major', linewidth=0.8, alpha=0.65)
ax.tick_params(labelsize=8)
ax.set_xlabel('week', loc='right', fontsize=9)
ax.set_ylabel('amount', loc='top', fontsize=9, rotation=0)
ax.scatter(x,y,s=28,color='black')
xx=np.linspace(0,7.5,200); ax.plot(xx,2*(1.55**xx),linestyle='--',linewidth=1.5,color='black')
save(fig,'unit8_exponential_scatter.png')

# 8 capstone mixed graph simple
x=np.linspace(-4,6,400)
fig,ax=plt.subplots(figsize=(4,4))
setup_axes(ax, (-5,8), (-5,12))
ax.plot(x, -0.5*(x-2)**2+8, linewidth=1.8)
ax.plot(x, 1.5*x+1, linewidth=1.8, linestyle='--')
ax.text(2.2,8.3,'P',fontsize=10,fontweight='bold')
ax.text(5,8.8,'L',fontsize=10,fontweight='bold')
save(fig,'unit8_projectile_compare.png')
