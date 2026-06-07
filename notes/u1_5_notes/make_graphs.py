import matplotlib.pyplot as plt
from pathlib import Path
out=Path('/mnt/data/u1_5_notes/figures')
out.mkdir(parents=True, exist_ok=True)

def setup(ax, xlim, ylim, title, xlabel, ylabel, xticks=None, yticks=None):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.set_xlabel(xlabel, fontsize=11); ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, alpha=0.35)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    if xticks is not None: ax.set_xticks(xticks)
    if yticks is not None: ax.set_yticks(yticks)
    ax.set_box_aspect(1)

# Future: break-even plans square
fig, ax = plt.subplots(figsize=(5.4,5.4), dpi=160)
months = [0,1,2,3,4,5,6,7,8]
plan_a = [30+10*m for m in months]
plan_b = [60+5*m for m in months]
setup(ax, (-0.5,8.5), (0,125), 'Two Membership Plans', 'Months', 'Total cost ($)', xticks=range(0,9), yticks=range(0,126,25))
ax.plot(months, plan_a, marker='o', linewidth=2.4, label='Plan A')
ax.plot(months, plan_b, marker='s', linewidth=2.4, label='Plan B')
ax.legend(loc='upper left', frameon=True, fontsize=9)
ax.text(1.2, 50, 'starts lower\nchanges faster', fontsize=9)
ax.text(4.7, 82, 'starts higher\nchanges slower', fontsize=9)
fig.tight_layout()
fig.savefig(out/'u1_5_future_two_plans_sq_v1.png')
plt.close(fig)

# Example graph: ticket cost
fig, ax = plt.subplots(figsize=(5.2,5.2), dpi=160)
t = [0,1,2,3,4,5,6]
C = [8+6*i for i in t]
setup(ax, (-0.5,6.5), (0,50), 'Ticket Cost Model', 'Tickets', 'Cost ($)', xticks=range(0,7), yticks=range(0,51,10))
ax.plot(t, C, marker='o', linewidth=2.6)
for x,y in zip(t,C):
    if x in [0,3,6]:
        ax.annotate(f'({x},{y})', (x,y), textcoords='offset points', xytext=(7,6), fontsize=9)
fig.tight_layout()
fig.savefig(out/'u1_5_ticket_cost_sq_v1.png')
plt.close(fig)
