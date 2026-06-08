import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
out = Path('/mnt/data/u2_1_notes/figures')
out.mkdir(parents=True, exist_ok=True)

def setup(ax, xlim=(-1,8), ylim=(-1,10), xlabel='Input', ylabel='Output'):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_box_aspect(1)
    ax.set_xlabel(xlabel, labelpad=8)
    ax.set_ylabel(ylabel, labelpad=8)
    ax.set_xticks(np.arange(np.ceil(xlim[0]), np.floor(xlim[1])+1, 1))
    ax.set_yticks(np.arange(np.ceil(ylim[0]), np.floor(ylim[1])+1, 1))
    ax.grid(True, linewidth=0.5, alpha=0.45)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    for spine in ax.spines.values():
        spine.set_linewidth(1)
    ax.tick_params(labelsize=8)

def save(fig, name):
    fig.tight_layout(pad=0.8)
    fig.savefig(out/name, dpi=180, bbox_inches='tight')
    plt.close(fig)

# Future task: three linear distance-time lines on same square coordinate grid, clean and moderate.
fig, ax = plt.subplots(figsize=(5.2,5.2))
setup(ax, (0,8), (0,16), xlabel='Time (minutes)', ylabel='Distance (blocks)')
x = np.array([0,8])
ax.plot(x, 2*x, linewidth=2, label='Route A')
ax.plot(x, 1.25*x+3, linewidth=2, label='Route B')
ax.plot(x, 0.75*x+7, linewidth=2, label='Route C')
ax.scatter([0,4,8],[0,8,16], s=24)
ax.scatter([0,4,8],[3,8,13], s=24)
ax.scatter([0,4,8],[7,10,13], s=24)
ax.legend(loc='upper left', fontsize=8, framealpha=0.95)
ax.set_title('Three walking routes', fontsize=11, pad=8)
save(fig, 'u2_1_future_routes_sq_v1.png')

# Example 1: Slope triangle on line.
fig, ax = plt.subplots(figsize=(5,5))
setup(ax, (0,7), (0,9), xlabel='x', ylabel='y')
x = np.array([0,7])
ax.plot(x, 1.5*x+0.5, linewidth=2)
ax.scatter([1,5],[2,8], s=40, zorder=5)
# triangle from (1,2) to (5,2) to (5,8)
ax.plot([1,5],[2,2], linewidth=2, linestyle='--')
ax.plot([5,5],[2,8], linewidth=2, linestyle='--')
ax.text(3,1.45,'run = 4', ha='center', va='top', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
ax.text(5.2,5,'rise = 6', ha='left', va='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
ax.annotate('(1, 2)', (1,2), xytext=(8,8), textcoords='offset points', fontsize=8, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
ax.annotate('(5, 8)', (5,8), xytext=(8,-14), textcoords='offset points', fontsize=8, bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
save(fig, 'u2_1_slope_triangle_sq_v1.png')

# Example 2/YouTry graph: Table-to-graph constant slope.
fig, ax = plt.subplots(figsize=(5,5))
setup(ax, (0,6), (0,14), xlabel='Hours', ylabel='Dollars earned')
pts_x = np.array([0,1,2,3,4])
pts_y = 2*pts_x+4
ax.plot(pts_x, pts_y, linewidth=2)
ax.scatter(pts_x, pts_y, s=35, zorder=5)
for x0,y0 in zip(pts_x,pts_y):
    ax.annotate(f'({x0}, {y0})', (x0,y0), xytext=(6,4), textcoords='offset points', fontsize=7, bbox=dict(facecolor='white', edgecolor='none', alpha=0.75))
ax.set_title('Earnings over time', fontsize=11, pad=8)
save(fig, 'u2_1_earnings_graph_sq_v1.png')

# Example 4: Two small square panels: constant vs not constant rate from table-like points.
fig, axes = plt.subplots(1,2, figsize=(8,4))
for ax in axes:
    setup(ax, (0,5), (0,12), xlabel='Time', ylabel='Distance')
axes[0].plot([0,1,2,3,4],[2,4,6,8,10], linewidth=2)
axes[0].scatter([0,1,2,3,4],[2,4,6,8,10], s=28)
axes[0].set_title('Graph A', fontsize=10)
axes[1].plot([0,1,2,3,4],[2,3,5,8,12], linewidth=2)
axes[1].scatter([0,1,2,3,4],[2,3,5,8,12], s=28)
axes[1].set_title('Graph B', fontsize=10)
save(fig, 'u2_1_constant_nonconstant_sq_v1.png')
