from pathlib import Path
import re, zipfile, os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

base=Path('/mnt/data/u1_3_notes')
figdir=base/'figures'
figdir.mkdir(exist_ok=True)

# ---------- GRAPH REGENERATION ----------
def setup_data_square(ax, xlim, ylim, title=None, xticks=None, yticks=None):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_box_aspect(1)  # square plotting panel, without forcing equal data-unit scale
    ax.axhline(0, color='black', lw=1.2)
    ax.axvline(0, color='black', lw=1.2)
    if xticks is None:
        xticks = range(int(np.ceil(xlim[0])), int(np.floor(xlim[1]))+1)
    if yticks is None:
        yticks = range(int(np.ceil(ylim[0])), int(np.floor(ylim[1]))+1, 2)
    ax.set_xticks(list(xticks)); ax.set_yticks(list(yticks))
    ax.grid(True, linewidth=0.5, alpha=0.35)
    ax.tick_params(labelsize=8)
    if title:
        ax.set_title(title, fontsize=12, pad=8, fontweight='bold')

# Fixed Example 3 graph: two square panels, labels offset away from points/ticks
xp=np.array([0,1,2,3,4])
yp1=np.array([2,5,8,11,14])
yp2=np.array([1,2,4,8,16])
fig, axs = plt.subplots(1,2,figsize=(8.4,4.4), constrained_layout=True)
for ax,title,yp,offsets in [
    (axs[0],'Table A pattern',yp1,[(0.10,0.45),(0.10,0.45),(0.10,0.45),(0.10,0.45),(0.10,0.45)]),
    (axs[1],'Table B pattern',yp2,[(0.10,0.45),(0.10,0.45),(0.10,0.45),(-0.85,0.55),(0.10,0.45)])
]:
    setup_data_square(ax, xlim=(-0.6,4.8), ylim=(-1,17), title=title, xticks=range(0,5), yticks=range(-1,18,3))
    ax.plot(xp, yp, marker='o', lw=2.8, markersize=6)
    for (xx,yy),(dx,dy) in zip(zip(xp,yp), offsets):
        ax.text(xx+dx, yy+dy, f'({xx},{yy})', fontsize=8)
fig.savefig(figdir/'u1_3_table_patterns_sq_v2.png', dpi=180, bbox_inches='tight')
plt.close(fig)

# New future task graph set: four square panels, deliberately unlabeled family names
fig, axs = plt.subplots(2,2,figsize=(7.4,7.4), constrained_layout=True)
# A straight increasing
ax=axs[0,0]; setup_data_square(ax, (-0.5,6.5), (-1,13), 'Graph A', xticks=range(0,7), yticks=range(0,14,3))
x=np.linspace(0,6,200); ax.plot(x, 1.6*x+1.2, lw=2.8); ax.text(0.35,11.4,'same steady rise?', fontsize=8)
# B curved faster and faster
ax=axs[0,1]; setup_data_square(ax, (-0.5,6.5), (-1,13), 'Graph B', xticks=range(0,7), yticks=range(0,14,3))
x=np.linspace(0,6,200); ax.plot(x, 0.28*(x**2)+1, lw=2.8); ax.text(2.0,10.6,'gets steeper?', fontsize=8)
# C repeating
ax=axs[1,0]; setup_data_square(ax, (-0.5,6.5), (-4,4), 'Graph C', xticks=range(0,7), yticks=range(-4,5,2))
x=np.linspace(0,6,400); ax.plot(x, 2.4*np.sin(2*np.pi*(x-0.4)/3), lw=2.8); ax.text(2.2,3.0,'repeats?', fontsize=8)
# D decreasing and leveling
ax=axs[1,1]; setup_data_square(ax, (-0.5,6.5), (-1,13), 'Graph D', xticks=range(0,7), yticks=range(0,14,3))
x=np.linspace(0,6,300); ax.plot(x, 10*np.exp(-0.55*x)+1.2, lw=2.8); ax.text(2.6,4.8,'levels out?', fontsize=8)
fig.savefig(figdir/'u1_3_future_shapes_v2.png', dpi=180, bbox_inches='tight')
plt.close(fig)

# ---------- HTML EDITS ----------
html_path=base/'u1_3_notes.html'
html=html_path.read_text()
old_future = re.search(r'    <!-- SECTION START: WHAT\'S TO COME -->.*?    <!-- SECTION START: INTRO -->', html, re.S)
new_future = '''    <!-- SECTION START: WHAT'S TO COME -->
    <section>
      <div class="problem section-title-task-group">
        <h2>What’s To Come</h2>
        <p>Later in this course, you will understand much more about the task below. For now, do not solve it. Instead, annotate it individually. Circle anything familiar, underline words or graph features that seem important, and write notes about what information you think will be needed.</p>
        <p>As you annotate, ask yourself: Are all relationships that increase basically the same? Which graph changes by about the same amount each time? Which graph changes faster and faster? Which graph repeats? Which graph decreases and levels out? What might make two relationships belong to the same function family?</p>
        <div class="annotation-box">
          <p><strong>Future Task</strong></p>
          <p>A student says, “Most real-world relationships are basically the same because the outputs just get bigger or smaller.” The four situations and four graph shapes below may or may not support that claim.</p>
          <div class="representation-grid">
            <div class="rep-card"><h4>Situation 1</h4><p>A water tank fills at a steady rate each minute.</p></div>
            <div class="rep-card"><h4>Situation 2</h4><p>A shared post reaches more people each hour because each group shares it with more groups.</p></div>
            <div class="rep-card"><h4>Situation 3</h4><p>Outdoor temperature rises and falls in a repeating daily pattern.</p></div>
            <div class="rep-card"><h4>Situation 4</h4><p>A phone battery drops quickly at first, then the percent changes more slowly.</p></div>
          </div>
          <div class="graph-block graph-xl"><img src="figures/u1_3_future_shapes_v2.png" alt="Four graph shapes showing steady change, faster change, repeating change, and leveling change"></div>
          <ol>
            <li>Annotate one graph that seems to change by about the same amount each step.</li>
            <li>Annotate one graph that seems to change faster and faster.</li>
            <li>Annotate one graph that seems to repeat a pattern.</li>
            <li>Write one question you would need to answer before matching every situation to a graph with confidence.</li>
          </ol>
        </div>
        <div class="workspace-discuss"></div>
      </div>
    </section>

    <!-- SECTION START: INTRO -->'''
if not old_future:
    raise SystemExit('Future section not found')
html = html[:old_future.start()] + new_future + html[old_future.end():]
html = html.replace('figures/u1_3_table_patterns.png', 'figures/u1_3_table_patterns_sq_v2.png')
html = html.replace('Look back at the future task. Highlight one part that makes more sense now than it did at the beginning. Circle one part that still feels unfamiliar. Write one sentence about what representation you would look at first.',
                    'Look back at the future task. Highlight one graph shape that makes more sense now than it did at the beginning. Circle one part that still feels unfamiliar. Write one sentence about what makes two relationships seem like they belong to the same function family.')
html_path.write_text(html)

# ---------- QA ----------
text=html_path.read_text()
issues=[]
for pat in ['\\(', '\\)', '\\[', '\\]', '\\f']:
    if pat in text:
        issues.append(f'MathJax danger pattern found: {pat}')
if len(re.findall(r'<h3>Example \d+</h3>', text)) != 4:
    issues.append('Expected exactly 4 examples')
if len(re.findall(r'<h3>You Try It \d+</h3>', text)) != 4:
    issues.append('Expected exactly 4 You Try Its')
if 'u1_3_table_patterns.png' in text or 'u1_3_future_graphs.png' in text:
    issues.append('Old graph filename still referenced')
for img in ['u1_3_table_patterns_sq_v2.png','u1_3_future_shapes_v2.png']:
    p=figdir/img
    if not p.exists():
        issues.append(f'Missing graph: {img}')
    else:
        im=Image.open(p)
        w,h=im.size
        # combined 1x2 and 2x2 images can be rectangular/square, but should not be tall/narrow
        if h/w > 1.25:
            issues.append(f'Image too tall: {img} {w}x{h}')

# zip package
zip_path=Path('/mnt/data/u1_3_notes_v2.zip')
if zip_path.exists():
    zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in base.rglob('*'):
        if p.is_file():
            z.write(p, p.relative_to(base.parent))
# test zip
with zipfile.ZipFile(zip_path,'r') as z:
    bad=z.testzip()
    if bad:
        issues.append(f'ZIP bad file: {bad}')

report=Path('/mnt/data/u1_3_notes_v2_QA.txt')
report.write_text('\n'.join(['QA REPORT - u1_3_notes_v2', 'Issues:'] + (issues if issues else ['None']) + [f'ZIP: {zip_path}', 'New future graph: u1_3_future_shapes_v2.png', 'New table graph: u1_3_table_patterns_sq_v2.png']))
if issues:
    print('\n'.join(issues))
else:
    print('QA passed')
print(zip_path)
