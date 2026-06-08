from pathlib import Path
import re
from PIL import Image
from bs4 import BeautifulSoup
root=Path('/mnt/data/u2_1_notes')
html=(root/'u2_1_notes.html').read_text()
issues=[]
for pat in ['\\(','\\)','\\[','\\]']:
    if pat in html:
        issues.append(f'Found forbidden MathJax delimiter {pat}')
if re.search(r'\\f(?!rac)', html):
    issues.append('Found possible broken \\f command')
soup=BeautifulSoup(html,'html.parser')
for p in soup.find_all('p'):
    if p.find(['table','ol','ul','div','blockquote']):
        issues.append('Block element nested inside <p>')
example_count=len(re.findall(r'<h3>Example \d+</h3>', html))
yti_count=len(re.findall(r'<h3>You Try It \d+</h3>', html))
if example_count!=4: issues.append(f'Expected 4 examples, found {example_count}')
if yti_count!=4: issues.append(f'Expected 4 You Try Its, found {yti_count}')
if 'Supplemental Notes' in html: issues.append('Supplemental Notes section found')
if re.search(r'page-break-before|break-before', html):
    issues.append('Potential forced page break found')
imgs=re.findall(r'<img[^>]+src="([^"]+)"', html)
for src in imgs:
    if not (root/src).exists(): issues.append(f'Missing image: {src}')
referenced={Path(src).name for src in imgs}
for img in (root/'figures').glob('*.png'):
    if img.name not in referenced: issues.append(f'Unreferenced image: {img.name}')
    im=Image.open(img); w,h=im.size; ratio=max(w,h)/min(w,h)
    if 'constant_nonconstant' in img.name:
        if ratio>2.1: issues.append(f'Multi-panel graph too wide: {img.name} {w}x{h}')
    elif ratio>1.25:
        issues.append(f'Graph not near-square: {img.name} {w}x{h}')
print('examples:', example_count)
print('you_try_its:', yti_count)
print('images:', imgs)
print('issues:', issues if issues else 'none')
if issues:
    raise SystemExit(1)
