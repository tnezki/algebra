from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = os.path.dirname(__file__)
W, H = 1600, 1200
BLACK = (20,20,20)
DARK = (55,55,55)
MID = (120,120,120)
GRID = (205,205,205)
LIGHT = (232,232,232)
WHITE = (255,255,255)

FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_MATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def F(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def canvas(w=W,h=H):
    return Image.new('RGB',(w,h),WHITE), ImageDraw.Draw(Image.new('RGB',(1,1)))

def new(w=W,h=H):
    im = Image.new('RGB',(w,h),WHITE)
    return im, ImageDraw.Draw(im)

def save(im, name):
    path = os.path.join(OUT, name)
    im.save(path, 'PNG', optimize=True)
    print(name)

def arrow(draw, p1, p2, width=5, fill=BLACK, head=18):
    draw.line([p1,p2], fill=fill, width=width)
    x1,y1=p1; x2,y2=p2
    ang=math.atan2(y2-y1,x2-x1)
    for delta in (math.pi*0.82,-math.pi*0.82):
        draw.line([(x2,y2),(x2+head*math.cos(ang+delta),y2+head*math.sin(ang+delta))], fill=fill, width=width)

def axes(draw, box, x_ticks=10, y_ticks=10, labels=False, numbers=False, grid=True, first_quadrant=False):
    x0,y0,x1,y1=box
    if first_quadrant:
        ox, oy = x0, y1
    else:
        ox, oy = (x0+x1)//2, (y0+y1)//2
    sx=(x1-x0)/(x_ticks if first_quadrant else 2*x_ticks)
    sy=(y1-y0)/(y_ticks if first_quadrant else 2*y_ticks)
    if grid:
        if first_quadrant:
            for i in range(x_ticks+1):
                x=round(x0+i*sx)
                draw.line([(x,y0),(x,y1)], fill=GRID, width=2)
            for j in range(y_ticks+1):
                y=round(y1-j*sy)
                draw.line([(x0,y),(x1,y)], fill=GRID, width=2)
        else:
            for i in range(-x_ticks,x_ticks+1):
                x=round(ox+i*sx)
                draw.line([(x,y0),(x,y1)], fill=GRID, width=2)
            for j in range(-y_ticks,y_ticks+1):
                y=round(oy-j*sy)
                draw.line([(x0,y),(x1,y)], fill=GRID, width=2)
    if first_quadrant:
        arrow(draw,(x0,oy),(x1,oy),6,BLACK,22)
        arrow(draw,(ox,y1),(ox,y0),6,BLACK,22)
    else:
        arrow(draw,(x0,oy),(x1,oy),6,BLACK,22)
        arrow(draw,(x1,oy),(x0,oy),6,BLACK,22)
        arrow(draw,(ox,y1),(ox,y0),6,BLACK,22)
        arrow(draw,(ox,y0),(ox,y1),6,BLACK,22)
    tick=10
    if first_quadrant:
        for i in range(1,x_ticks+1):
            x=round(x0+i*sx); draw.line([(x,oy-tick),(x,oy+tick)], fill=BLACK,width=3)
            if numbers: draw.text((x-10,oy+14),str(i),font=F(22),fill=DARK)
        for j in range(1,y_ticks+1):
            y=round(y1-j*sy); draw.line([(ox-tick,y),(ox+tick,y)], fill=BLACK,width=3)
            if numbers: draw.text((ox-38,y-13),str(j),font=F(22),fill=DARK)
    else:
        for i in range(-x_ticks,x_ticks+1):
            if i==0: continue
            x=round(ox+i*sx); draw.line([(x,oy-tick),(x,oy+tick)], fill=BLACK,width=3)
            if numbers and (abs(i)%2==0 or x_ticks<=6): draw.text((x-14,oy+15),str(i),font=F(20),fill=DARK)
        for j in range(-y_ticks,y_ticks+1):
            if j==0: continue
            y=round(oy-j*sy); draw.line([(ox-tick,y),(ox+tick,y)], fill=BLACK,width=3)
            if numbers and (abs(j)%2==0 or y_ticks<=6): draw.text((ox+14,y-12),str(j),font=F(20),fill=DARK)
    if labels:
        draw.text((x1-30,oy+18),'x',font=F(28,True),fill=BLACK)
        draw.text((ox+15,y0+5),'y',font=F(28,True),fill=BLACK)
    return ox,oy,sx,sy

def title(draw, text, y=28, size=42):
    bb=draw.textbbox((0,0),text,font=F(size,True))
    draw.text(((W-(bb[2]-bb[0]))/2,y),text,font=F(size,True),fill=BLACK)

def label_center(draw, box, text, size=28, bold=False, fill=BLACK):
    x0,y0,x1,y1=box
    bb=draw.textbbox((0,0),text,font=F(size,bold))
    draw.text(((x0+x1-(bb[2]-bb[0]))/2,(y0+y1-(bb[3]-bb[1]))/2),text,font=F(size,bold),fill=fill)

# 1 coordinate plane labeled
im,d=new(); axes(d,(110,90,1490,1110),10,8,labels=True,numbers=True,grid=True); save(im,'coordinate_plane_labeled.png')
# 2 coordinate plane blank
im,d=new(); axes(d,(110,90,1490,1110),10,8,labels=False,numbers=False,grid=True); save(im,'coordinate_plane_blank.png')
# 3 four mini grids
im,d=new()
boxes=[(70,70,760,560),(840,70,1530,560),(70,640,760,1130),(840,640,1530,1130)]
for b in boxes: axes(d,b,5,4,labels=False,numbers=False,grid=True)
save(im,'four_quadrant_mini_grids.png')
# 4 first quadrant
im,d=new(); axes(d,(120,90,1480,1080),10,8,labels=True,numbers=True,grid=True,first_quadrant=True); save(im,'first_quadrant_grid.png')
# 5 polar grid
im,d=new(); cx,cy=800,600; R=500
for r in range(50,R+1,50): d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=GRID,width=2)
for deg in range(0,180,15):
    a=math.radians(deg); dx=R*math.cos(a); dy=R*math.sin(a)
    d.line([(cx-dx,cy+dy),(cx+dx,cy-dy)],fill=GRID,width=2)
d.ellipse((cx-R,cy-R,cx+R,cy+R),outline=BLACK,width=4)
d.line([(cx-R,cy),(cx+R,cy)],fill=DARK,width=3); d.line([(cx,cy-R),(cx,cy+R)],fill=DARK,width=3)
save(im,'polar_grid.png')
# 6 semilog grid
im,d=new(); x0,y0,x1,y1=110,100,1490,1090
# x linear 10 divisions
for i in range(11):
    x=x0+(x1-x0)*i/10; d.line([(x,y0),(x,y1)],fill=GRID,width=2)
# y logarithmic, three decades
for dec in range(3):
    y_top=y0+(y1-y0)*dec/3; y_bottom=y0+(y1-y0)*(dec+1)/3
    for n in range(1,10):
        frac=math.log10(n)
        y=y_bottom-frac*(y_bottom-y_top)
        d.line([(x0,y),(x1,y)],fill=GRID if n>1 else MID,width=2 if n>1 else 3)
# border
for seg in [((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]: d.line(seg,fill=BLACK,width=4)
d.text((125,35),'Semilog Grid (log y-axis)',font=F(30,True),fill=BLACK)
save(im,'semilog_grid.png')
# number line helper
def number_line(name, start=None, end=None, major=20, minor=1, blank=False):
    im,d=new(1800,420); y=180; x0,x1=100,1700
    arrow(d,(x0,y),(x1,y),6,BLACK,24); arrow(d,(x1,y),(x0,y),6,BLACK,24)
    if blank:
        for i in range(major+1):
            x=x0+(x1-x0)*i/major; d.line([(x,y-22),(x,y+22)],fill=BLACK,width=4)
    else:
        total=end-start
        count=int(total/minor)
        for i in range(count+1):
            val=start+i*minor; x=x0+(x1-x0)*i/count
            h=24 if ((val-start)%(minor*5)==0 or total<=50) else 15
            d.line([(x,y-h),(x,y+h)],fill=BLACK,width=4 if h==24 else 3)
            if total<=50 or (val%20==0):
                txt=str(int(val)); bb=d.textbbox((0,0),txt,font=F(24)); d.text((x-(bb[2]-bb[0])/2,y+38),txt,font=F(24),fill=BLACK)
    save(im,name)
number_line('number_line_blank_scale.png',blank=True,major=24)
number_line('number_line_neg20_to_20.png',-20,20,minor=1)
number_line('number_line_neg100_to_100.png',-100,100,minor=5)

# 10 parent function mini graphs
im,d=new(); title(d,'Parent Function Mini-Graphs',18,38)
funcs=[('y = x',lambda x:x),('y = x²',lambda x:x*x/2.5),('y = x³',lambda x:x**3/8),('y = |x|',lambda x:abs(x)),('y = √x',lambda x:math.sqrt(x) if x>=0 else None),('y = ∛x',lambda x:math.copysign(abs(x)**(1/3),x)),('y = 2ˣ',lambda x:2**x/3),('y = log₂x',lambda x:math.log(x,2) if x>0 else None),('y = 1/x',lambda x:1/x if abs(x)>.12 else None),('y = 1/x²',lambda x:1/x**2 if abs(x)>.18 else None),('y = sin x',lambda x:2*math.sin(x)),('y = cos x',lambda x:2*math.cos(x))]
cols,rows=4,3; gapx,gapy=22,24; top=90; left=50; bw=(W-left*2-gapx*(cols-1))/cols; bh=(H-top-40-gapy*(rows-1))/rows
for idx,(lab,fn) in enumerate(funcs):
    r=idx//cols;c=idx%cols; x0=left+c*(bw+gapx); y0=top+r*(bh+gapy); x1=x0+bw; y1=y0+bh
    d.rounded_rectangle((x0,y0,x1,y1),radius=16,outline=MID,width=2)
    bb=d.textbbox((0,0),lab,font=F(24,True)); d.text(((x0+x1-(bb[2]-bb[0]))/2,y0+8),lab,font=F(24,True),fill=BLACK)
    gx0,gy0,gx1,gy1=x0+22,y0+48,x1-18,y1-18
    ox,oy,sx,sy=axes(d,(gx0,gy0,gx1,gy1),4,3,grid=True)
    pts=[]; last=None
    for k in range(500):
        xv=-4+8*k/499
        try: yv=fn(xv)
        except: yv=None
        if yv is None or not math.isfinite(yv) or abs(yv)>6:
            if len(pts)>1: d.line(pts,fill=BLACK,width=4)
            pts=[]; continue
        px=ox+xv*sx; py=oy-yv*sy
        if gy0<=py<=gy1: pts.append((px,py))
        else:
            if len(pts)>1: d.line(pts,fill=BLACK,width=4)
            pts=[]
    if len(pts)>1: d.line(pts,fill=BLACK,width=4)
save(im,'parent_function_mini_graphs.png')

# transformation reference
im,d=new(); title(d,'Function Transformations',28,42)
rows=[('f(x) + k','shift up k'),('f(x) - k','shift down k'),('f(x - h)','shift right h'),('f(x + h)','shift left h'),('-f(x)','reflect across x-axis'),('f(-x)','reflect across y-axis'),('a·f(x)','vertical stretch/compress by |a|'),('f(bx)','horizontal scale by factor 1/|b|')]
x0,y0=120,120; col1=580; rowh=112
for i,(expr,desc) in enumerate(rows):
    y=y0+i*rowh
    d.rounded_rectangle((x0,y,1480,y+86),radius=12,outline=GRID,width=2)
    d.text((x0+30,y+18),expr,font=F(34,True),fill=BLACK)
    d.text((x0+col1,y+23),desc,font=F(30),fill=DARK)
save(im,'transformation_reference.png')

# piecewise axes
im,d=new(); title(d,'Blank Piecewise-Function Axes',18,34)
for i in range(3): axes(d,(120,90+i*365,1480,400+i*365),8,3,labels=(i==0),numbers=False,grid=True)
save(im,'piecewise_function_axes.png')
# interval notation template
im,d=new(); title(d,'Interval-Notation Number Lines',26,38)
for r in range(4):
    y=220+r*230; x0,x1=170,1430
    arrow(d,(x0,y),(x1,y),5,BLACK,20); arrow(d,(x1,y),(x0,y),5,BLACK,20)
    for i in range(13):
        x=x0+(x1-x0)*i/12; d.line([(x,y-18),(x,y+18)],fill=BLACK,width=3)
    if r==0:
        d.ellipse((440-12,y-12,440+12,y+12),outline=BLACK,width=4)
        d.ellipse((1160-12,y-12,1160+12,y+12),fill=BLACK)
        d.text((390,y+42),'open',font=F(22),fill=DARK); d.text((1090,y+42),'closed',font=F(22),fill=DARK)
save(im,'interval_notation_number_lines.png')
# sign chart
im,d=new(); title(d,'Sign Chart Template',34,42)
x0,x1=160,1440; y=250
arrow(d,(x0,y),(x1,y),5,BLACK,18); arrow(d,(x1,y),(x0,y),5,BLACK,18)
for x in [440,800,1160]: d.line([(x,y-36),(x,y+420)],fill=BLACK,width=4)
for yy,label in [(360,'Factor 1'),(480,'Factor 2'),(600,'Factor 3'),(760,'Product / Function')]:
    d.text((80,yy-18),label,font=F(28,True if yy==760 else False),fill=BLACK)
    d.line([(160,yy),(1440,yy)],fill=GRID,width=2)
save(im,'sign_chart_template.png')
# polynomial end behavior
im,d=new(); title(d,'Polynomial End Behavior',24,40)
beh=[('even, + leading','up / up',-1,1),('even, − leading','down / down',1,-1),('odd, + leading','down / up',-1,-1),('odd, − leading','up / down',1,1)]
boxes=[(100,120,750,560),(850,120,1500,560),(100,650,750,1090),(850,650,1500,1090)]
for b,(lab,desc,a,bend) in zip(boxes,beh):
    x0,y0,x1,y1=b; d.rounded_rectangle(b,radius=16,outline=MID,width=2); d.text((x0+22,y0+16),lab,font=F(28,True),fill=BLACK)
    gx0,gy0,gx1,gy1=x0+35,y0+70,x1-35,y1-35; ox,oy,sx,sy=axes(d,(gx0,gy0,gx1,gy1),4,3,grid=True)
    # simple curve representative
    pts=[]
    for k in range(300):
        x=-3.5+7*k/299
        if 'even' in lab: y=(x**2/4)*(1 if '+' in lab else -1)
        else: y=(x**3/12)*(1 if '+' in lab else -1)
        px=ox+x*sx; py=oy-y*sy
        if gy0<=py<=gy1: pts.append((px,py))
    d.line(pts,fill=BLACK,width=5)
save(im,'polynomial_end_behavior.png')
# rational asymptote template
im,d=new(); title(d,'Rational Function / Asymptote Template',24,38)
ox,oy,sx,sy=axes(d,(120,100,1480,1100),10,8,labels=True,numbers=False,grid=True)
for x in [ox-4*sx, ox+5*sx]: d.line([(x,100),(x,1100)],fill=MID,width=4)
for y in [oy-3*sy,oy+4*sy]: d.line([(120,y),(1480,y)],fill=MID,width=4)
d.text((130,1040),'Use dashed guides for vertical/horizontal asymptotes.',font=F(24),fill=DARK)
save(im,'rational_asymptote_template.png')
# unit circle labeled
im,d=new(); title(d,'Unit Circle Reference',18,38); cx,cy=800,620; R=450
d.ellipse((cx-R,cy-R,cx+R,cy+R),outline=BLACK,width=5); d.line([(cx-R-30,cy),(cx+R+30,cy)],fill=MID,width=3); d.line([(cx,cy-R-30),(cx,cy+R+30)],fill=MID,width=3)
angles=[0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330]
for deg in angles:
    a=math.radians(deg); x=cx+R*math.cos(a); y=cy-R*math.sin(a); d.line([(cx,cy),(x,y)],fill=GRID,width=2)
    txt={0:'0',30:'π/6',45:'π/4',60:'π/3',90:'π/2',120:'2π/3',135:'3π/4',150:'5π/6',180:'π',210:'7π/6',225:'5π/4',240:'4π/3',270:'3π/2',300:'5π/3',315:'7π/4',330:'11π/6'}[deg]
    tx=cx+(R+55)*math.cos(a); ty=cy-(R+55)*math.sin(a); bb=d.textbbox((0,0),txt,font=F(24)); d.text((tx-(bb[2]-bb[0])/2,ty-(bb[3]-bb[1])/2),txt,font=F(24),fill=BLACK)
save(im,'unit_circle_labeled.png')
# degrees + radians circle
im,d=new(); title(d,'Degrees and Radians',18,38); cx,cy=800,620; R=450; d.ellipse((cx-R,cy-R,cx+R,cy+R),outline=BLACK,width=5)
for deg in range(0,360,30):
    a=math.radians(deg); x=cx+R*math.cos(a); y=cy-R*math.sin(a); d.line([(cx,cy),(x,y)],fill=GRID,width=2)
    rad_map={0:'0',30:'π/6',60:'π/3',90:'π/2',120:'2π/3',150:'5π/6',180:'π',210:'7π/6',240:'4π/3',270:'3π/2',300:'5π/3',330:'11π/6'}
    tx=cx+(R+52)*math.cos(a); ty=cy-(R+52)*math.sin(a)
    txt=f'{deg}°\n{rad_map[deg]}'
    lines=txt.split('\n')
    for j,line in enumerate(lines):
        bb=d.textbbox((0,0),line,font=F(22,True if j==0 else False)); d.text((tx-(bb[2]-bb[0])/2,ty-22+j*26),line,font=F(22,True if j==0 else False),fill=BLACK)
save(im,'unit_circle_degrees_radians.png')
# trig wave axes
im,d=new(); title(d,'Trig Wave Axes',18,36)
for r in range(2):
    x0,y0,x1,y1=120,120+r*520,1480,560+r*520; ox=(x0+x1)//2; oy=(y0+y1)//2
    for i in range(17): x=x0+(x1-x0)*i/16; d.line([(x,y0),(x,y1)],fill=GRID,width=2)
    for j in range(9): y=y0+(y1-y0)*j/8; d.line([(x0,y),(x1,y)],fill=GRID,width=2)
    arrow(d,(x0,oy),(x1,oy),5,BLACK,18); arrow(d,(x1,oy),(x0,oy),5,BLACK,18); arrow(d,(ox,y1),(ox,y0),5,BLACK,18); arrow(d,(ox,y0),(ox,y1),5,BLACK,18)
    labs=['−2π','−3π/2','−π','−π/2','0','π/2','π','3π/2','2π']
    for i,lab in enumerate(labs):
        x=x0+(x1-x0)*i/8; d.line([(x,oy-12),(x,oy+12)],fill=BLACK,width=3); bb=d.textbbox((0,0),lab,font=F(21)); d.text((x-(bb[2]-bb[0])/2,oy+20),lab,font=F(21),fill=DARK)
save(im,'trig_wave_axes.png')
# derivative tangent diagram
im,d=new(); title(d,'Derivative / Tangent-Line Diagram',20,38); ox,oy,sx,sy=axes(d,(120,100,1480,1100),8,6,labels=True,grid=True)
pts=[]
for k in range(500):
    x=-7+14*k/499; y=0.08*(x+3)*(x-1)*(x-4)+1
    px=ox+x*sx; py=oy-y*sy
    if 100<=py<=1100: pts.append((px,py))
d.line(pts,fill=BLACK,width=5)
xp=2; yp=0.08*(xp+3)*(xp-1)*(xp-4)+1; slope=0.08*((xp-1)*(xp-4)+(xp+3)*(xp-4)+(xp+3)*(xp-1))
for x in [-7,7]:
    y=yp+slope*(x-xp); px=ox+x*sx; py=oy-y*sy
    if x==-7: p1=(px,py)
    else: p2=(px,py)
d.line([p1,p2],fill=DARK,width=4); px=ox+xp*sx; py=oy-yp*sy; d.ellipse((px-10,py-10,px+10,py+10),fill=BLACK); d.text((px+18,py-40),'point of tangency',font=F(24),fill=DARK)
save(im,'derivative_tangent_diagram.png')
# riemann sum grid
im,d=new(); title(d,'Riemann Sum Grid',20,38); ox,oy,sx,sy=axes(d,(120,100,1480,1100),8,6,labels=True,grid=True)
# sample curve
pts=[]
for k in range(400):
    x=-6+12*k/399; y=0.06*(x+5)*(x+1)*(x-4)+2
    px=ox+x*sx; py=oy-y*sy
    if 100<=py<=1100: pts.append((px,py))
d.line(pts,fill=BLACK,width=5)
# faint vertical partition guides
for xv in [-4,-2,0,2,4]:
    x=ox+xv*sx; d.line([(x,oy),(x,oy-5*sy)],fill=MID,width=3)
save(im,'riemann_sum_grid.png')

# Geometry/trig
im,d=new(); title(d,'Common Triangle Templates',24,40)
triangles=[((180,350),(520,350),(350,130),'acute'),((930,350),(1390,350),(930,100),'right'),((180,930),(600,930),(520,650),'obtuse'),((950,930),(1400,930),(1175,560),'isosceles')]
for a,b,c,lab in triangles:
    d.line([a,b,c,a],fill=BLACK,width=5); bb=d.textbbox((0,0),lab,font=F(28,True)); d.text(((a[0]+b[0]+c[0])/3-(bb[2]-bb[0])/2,max(a[1],b[1],c[1])+35),lab,font=F(28,True),fill=DARK)
save(im,'common_triangle_templates.png')
im,d=new(); title(d,'Special Right Triangles',28,42)
# 45-45-90
A=(180,520);B=(650,520);C=(180,120);d.line([A,B,C,A],fill=BLACK,width=6); d.rectangle((180,480,220,520),outline=BLACK,width=4); d.text((315,545),'45°–45°–90°',font=F(32,True),fill=BLACK); d.text((130,300),'x',font=F(30),fill=BLACK); d.text((390,530),'x',font=F(30),fill=BLACK); d.text((390,280),'x√2',font=F(30),fill=BLACK)
# 30-60-90
A=(900,950);B=(1470,950);C=(900,170);d.line([A,B,C,A],fill=BLACK,width=6); d.rectangle((900,910,940,950),outline=BLACK,width=4); d.text((1080,990),'30°–60°–90°',font=F(32,True),fill=BLACK); d.text((835,550),'x√3',font=F(30),fill=BLACK); d.text((1150,950),'x',font=F(30),fill=BLACK); d.text((1160,520),'2x',font=F(30),fill=BLACK)
save(im,'special_right_triangles.png')
# protractor
im,d=new(); title(d,'Blank Protractor',28,40); cx,cy=800,940; R=620
d.arc((cx-R,cy-R,cx+R,cy+R),180,360,fill=BLACK,width=6); d.line([(cx-R,cy),(cx+R,cy)],fill=BLACK,width=6)
for deg in range(0,181,5):
    a=math.radians(180+deg); outer=(cx+R*math.cos(a),cy+R*math.sin(a)); ln=42 if deg%10==0 else 24; inner=(cx+(R-ln)*math.cos(a),cy+(R-ln)*math.sin(a)); d.line([inner,outer],fill=BLACK,width=4 if deg%10==0 else 2)
    if deg%20==0:
        tx=cx+(R-80)*math.cos(a); ty=cy+(R-80)*math.sin(a); txt=str(deg); bb=d.textbbox((0,0),txt,font=F(24)); d.text((tx-(bb[2]-bb[0])/2,ty-(bb[3]-bb[1])/2),txt,font=F(24),fill=DARK)
save(im,'blank_protractor.png')
# angle circle
im,d=new(); title(d,'Angle Circle Template',24,40); cx,cy=800,620; R=450; d.ellipse((cx-R,cy-R,cx+R,cy+R),outline=BLACK,width=5)
for deg in range(0,360,15):
    a=math.radians(deg); x=cx+R*math.cos(a); y=cy-R*math.sin(a); ln=35 if deg%30==0 else 18; d.line([(cx+(R-ln)*math.cos(a),cy-(R-ln)*math.sin(a)),(x,y)],fill=BLACK,width=3)
d.line([(cx-R,cy),(cx+R,cy)],fill=GRID,width=3); d.line([(cx,cy-R),(cx,cy+R)],fill=GRID,width=3)
save(im,'angle_circle_template.png')
# parallel transversal
im,d=new(); title(d,'Parallel Lines with Transversal',24,40)
d.line([(180,350),(1420,300)],fill=BLACK,width=7); d.line([(180,850),(1420,800)],fill=BLACK,width=7); d.line([(520,100),(1050,1100)],fill=BLACK,width=7)
# small angle arcs approximated circles/labels boxes
for x,y,n in [(655,330,'1'),(730,335,'2'),(660,395,'3'),(735,400,'4'),(900,820,'5'),(975,820,'6'),(905,880,'7'),(980,885,'8')]: d.text((x,y),n,font=F(30,True),fill=BLACK)
save(im,'parallel_lines_transversal.png')
# similar triangles
im,d=new(); title(d,'Similar-Triangle Template',24,40)
A=(180,850);B=(650,850);C=(180,280);d.line([A,B,C,A],fill=BLACK,width=6); A2=(940,900);B2=(1450,900);C2=(940,180);d.line([A2,B2,C2,A2],fill=BLACK,width=6)
for p,t in [(A,'A'),(B,'B'),(C,'C'),(A2,"A′"),(B2,"B′"),(C2,"C′")]: d.text((p[0]-35,p[1]+15 if p[1]>500 else p[1]-55),t,font=F(30,True),fill=BLACK)
save(im,'similar_triangles_template.png')
# circle parts
im,d=new(); title(d,'Circle Parts Reference Template',22,38); cx,cy=800,620;R=430;d.ellipse((cx-R,cy-R,cx+R,cy+R),outline=BLACK,width=6)
# radius
d.line([(cx,cy),(cx+R*0.82,cy-R*0.3)],fill=BLACK,width=5); d.text((1020,450),'radius',font=F(26,True),fill=BLACK)
# chord
d.line([(cx-R*0.75,cy-R*0.35),(cx+R*0.65,cy-R*0.55)],fill=BLACK,width=5); d.text((500,320),'chord',font=F(26,True),fill=BLACK)
# secant
d.line([(220,900),(1420,510)],fill=DARK,width=4); d.text((1200,650),'secant',font=F(26,True),fill=DARK)
# tangent
x=cx+R; d.line([(x,250),(x,1040)],fill=DARK,width=4); d.text((1240,1020),'tangent',font=F(26,True),fill=DARK); d.ellipse((cx-8,cy-8,cx+8,cy+8),fill=BLACK); d.text((cx+14,cy+12),'center',font=F(24),fill=DARK)
save(im,'circle_parts_reference.png')
# 3d axes
im,d=new(); title(d,'3-D Coordinate Axes',20,38); o=(800,700); arrow(d,o,(1420,700),6,BLACK,22); arrow(d,o,(420,1040),6,BLACK,22); arrow(d,o,(800,130),6,BLACK,22); d.text((1430,680),'x',font=F(32,True),fill=BLACK); d.text((370,1035),'y',font=F(32,True),fill=BLACK); d.text((820,110),'z',font=F(32,True),fill=BLACK)
for i in range(1,6):
    # x ticks
    x=o[0]+i*100; d.line([(x,690),(x,710)],fill=BLACK,width=3)
    # y ticks along diagonal
    x=o[0]-i*65; y=o[1]+i*58; d.line([(x-8,y-8),(x+8,y+8)],fill=BLACK,width=3)
    # z ticks
    y=o[1]-i*90; d.line([(790,y),(810,y)],fill=BLACK,width=3)
save(im,'coordinate_axes_3d.png')

# Physics
im,d=new(); title(d,'Free-Body Diagram Blank',24,40); cx,cy=800,650; d.rectangle((690,540,910,760),outline=BLACK,width=6)
for end in [(800,180),(800,1100),(300,650),(1300,650),(450,300),(1150,300),(450,1000),(1150,1000)]: arrow(d,(800,650),end,5,DARK,18)
d.text((705,610),'object',font=F(30,True),fill=BLACK)
save(im,'free_body_diagram_blank.png')
# motion strip
im,d=new(); title(d,'Motion Diagram Strip',24,40)
for row in range(3):
    y=260+row*300; arrow(d,(120,y),(1480,y),4,DARK,16)
    for i in range(11): x=180+i*120; d.ellipse((x-9,y-9,x+9,y+9),outline=BLACK,width=3)
    d.text((120,y+50),['Position dots','Velocity vectors','Acceleration vectors'][row],font=F(26,True),fill=BLACK)
save(im,'motion_diagram_strip.png')
# PVA axes
im,d=new(); title(d,'Position / Velocity / Acceleration Axes',20,36)
for i,label in enumerate(['Position x(t)','Velocity v(t)','Acceleration a(t)']):
    y0=100+i*350; y1=y0+280; ox,oy,sx,sy=axes(d,(160,y0,1460,y1),8,3,labels=False,grid=True); d.text((20,y0+110),label,font=F(28,True),fill=BLACK)
save(im,'pva_graph_axes.png')
# projectile motion grid
im,d=new(); title(d,'Projectile Motion Grid',20,36); ox,oy,sx,sy=axes(d,(120,100,1480,1100),10,8,labels=True,grid=True,first_quadrant=True); d.text((170,1040),'launch point',font=F(24),fill=DARK); save(im,'projectile_motion_grid.png')
# inclined plane
im,d=new(); title(d,'Inclined Plane Template',22,38); A=(250,950);B=(1380,950);C=(1080,350); d.line([A,B,C,A],fill=BLACK,width=6); # block
# rotated block approx polygon along slope
poly=[(715,650),(850,580),(910,690),(775,760)]; d.polygon(poly,outline=BLACK,fill=WHITE); d.line(poly+[poly[0]],fill=BLACK,width=5); d.arc((200,820,480,1100),280,330,fill=DARK,width=4); d.text((380,870),'θ',font=F(36,True),fill=BLACK)
save(im,'inclined_plane_template.png')
# pulleys
im,d=new(); title(d,'Pulley Diagram Templates',20,36)
# fixed pulley
cx,cy=430,360; d.ellipse((cx-110,cy-110,cx+110,cy+110),outline=BLACK,width=6); d.line([(cx,120),(cx,250)],fill=BLACK,width=5); d.line([(cx-110,360),(cx-110,870)],fill=BLACK,width=5); d.line([(cx+110,360),(cx+110,870)],fill=BLACK,width=5); d.rectangle((250,870,390,1030),outline=BLACK,width=5); d.rectangle((470,870,610,1030),outline=BLACK,width=5); d.text((275,1060),'fixed pulley',font=F(28,True),fill=BLACK)
# movable/simple two pulley
for cx,cy in [(1050,300),(1050,700)]: d.ellipse((cx-90,cy-90,cx+90,cy+90),outline=BLACK,width=6)
d.line([(960,300),(960,700)],fill=BLACK,width=5); d.line([(1140,300),(1140,700)],fill=BLACK,width=5); d.line([(1050,790),(1050,920)],fill=BLACK,width=5); d.rectangle((970,920,1130,1080),outline=BLACK,width=5); d.text((920,1100),'two-pulley setup',font=F(28,True),fill=BLACK)
save(im,'pulley_diagram_templates.png')
# spring block
im,d=new(); title(d,'Spring-Block Template',22,38); d.line([(160,250),(160,950)],fill=BLACK,width=7)
# spring zigzag
pts=[(160,600),(220,600)]
x=220
for i in range(12): pts.append((x+40,560 if i%2==0 else 640)); x+=40
pts.append((740,600)); d.line(pts,fill=BLACK,width=5); d.rectangle((740,500,1000,700),outline=BLACK,width=6); d.line([(1000,700),(1440,700)],fill=BLACK,width=6); d.text((810,570),'m',font=F(40,True),fill=BLACK); arrow(d,(870,780),(1230,780),5,DARK,18); d.text((1000,810),'x',font=F(30,True),fill=BLACK)
save(im,'spring_block_template.png')
# circuit symbols
im,d=new(); title(d,'Circuit Symbols Reference',20,38)
symbols=[('wire','wire'),('battery','battery'),('resistor','resistor'),('lamp','lamp'),('switch open','switch'),('capacitor','capacitor'),('ammeter','ammeter'),('voltmeter','voltmeter')]
for idx,(lab,typ) in enumerate(symbols):
    r=idx//2;c=idx%2; x=160+c*760; y=170+r*240
    d.text((x,y),lab,font=F(30,True),fill=BLACK); cy=y+95; xL=x+250; xR=x+620
    d.line([(xL,cy),(xL+80,cy)],fill=BLACK,width=5); d.line([(xR-80,cy),(xR,cy)],fill=BLACK,width=5)
    mid=(xL+xR)//2
    if typ=='wire': d.line([(xL+80,cy),(xR-80,cy)],fill=BLACK,width=5)
    elif typ=='battery': d.line([(mid-22,cy-55),(mid-22,cy+55)],fill=BLACK,width=5); d.line([(mid+22,cy-35),(mid+22,cy+35)],fill=BLACK,width=5)
    elif typ=='resistor':
        pts=[(xL+80,cy)]; xx=xL+90
        for k in range(8): pts.append((xx+30*k,cy-35 if k%2==0 else cy+35))
        pts.append((xR-80,cy)); d.line(pts,fill=BLACK,width=5)
    elif typ=='lamp': d.ellipse((mid-55,cy-55,mid+55,cy+55),outline=BLACK,width=5); d.line([(mid-38,cy-38),(mid+38,cy+38)],fill=BLACK,width=4); d.line([(mid-38,cy+38),(mid+38,cy-38)],fill=BLACK,width=4)
    elif typ=='switch': d.ellipse((mid-70,cy-7,mid-56,cy+7),fill=BLACK); d.ellipse((mid+56,cy-7,mid+70,cy+7),fill=BLACK); d.line([(mid-56,cy),(mid+45,cy-45)],fill=BLACK,width=5)
    elif typ=='capacitor': d.line([(mid-22,cy-55),(mid-22,cy+55)],fill=BLACK,width=5); d.line([(mid+22,cy-55),(mid+22,cy+55)],fill=BLACK,width=5)
    elif typ in ('ammeter','voltmeter'):
        d.ellipse((mid-55,cy-55,mid+55,cy+55),outline=BLACK,width=5); label_center(d,(mid-55,cy-55,mid+55,cy+55),'A' if typ=='ammeter' else 'V',34,True)
save(im,'circuit_symbols_reference.png')
# series parallel blank
im,d=new(); title(d,'Blank Series / Parallel Circuits',22,38)
# series rectangle loop
for xoff,label in [(100,'Series'),(850,'Parallel')]:
    d.text((xoff+220,120),label,font=F(32,True),fill=BLACK)
    if label=='Series':
        d.rectangle((xoff+80,240,xoff+620,950),outline=BLACK,width=5)
        for yy in [430,700]: d.rectangle((xoff+300,yy-55,xoff+400,yy+55),outline=MID,width=4)
        d.line([(xoff+80,570),(xoff+180,570)],fill=BLACK,width=5); d.line([(xoff+180,520),(xoff+180,620)],fill=BLACK,width=5); d.line([(xoff+220,540),(xoff+220,600)],fill=BLACK,width=5); d.line([(xoff+220,570),(xoff+620,570)],fill=BLACK,width=5)
    else:
        d.rectangle((xoff+80,240,xoff+620,950),outline=BLACK,width=5); d.line([(xoff+280,240),(xoff+280,950)],fill=BLACK,width=5); d.line([(xoff+450,240),(xoff+450,950)],fill=BLACK,width=5)
        for xx in [xoff+280,xoff+450]: d.rectangle((xx-45,500,xx+45,620),outline=MID,width=4)
save(im,'blank_series_parallel_circuits.png')
# ray templates
im,d=new(); title(d,'Ray-Diagram Templates',22,38)
for r,label in enumerate(['Converging lens','Concave mirror']):
    y=300+r*520; d.line([(120,y),(1480,y)],fill=MID,width=3)
    if r==0:
        d.line([(800,y-180),(800,y+180)],fill=BLACK,width=6); d.arc((740,y-180,860,y+180),90,270,fill=BLACK,width=4); d.arc((740,y-180,860,y+180),270,90,fill=BLACK,width=4)
    else:
        d.arc((720,y-220,920,y+220),90,270,fill=BLACK,width=6)
    for fx in [520,1080]: d.ellipse((fx-7,y-7,fx+7,y+7),fill=BLACK); d.text((fx-10,y+18),'F',font=F(22,True),fill=BLACK)
    d.text((120,y-210),label,font=F(28,True),fill=BLACK)
save(im,'ray_diagram_templates.png')
# wave template
im,d=new(); title(d,'Wave Template',22,38); x0,x1=120,1480; y=610; arrow(d,(x0,y),(x1,y),4,DARK,16); pts=[]
for k in range(800):
    x=x0+(x1-x0)*k/799; t=4*math.pi*k/799; yy=y-220*math.sin(t); pts.append((x,yy))
d.line(pts,fill=BLACK,width=5); d.line([(350,y),(350,y-220)],fill=MID,width=3); d.line([(350,y-220),(690,y-220)],fill=MID,width=3); d.text((405,y-270),'amplitude',font=F(26,True),fill=BLACK); d.line([(350,900),(690,900)],fill=MID,width=3); d.text((450,915),'wavelength',font=F(26,True),fill=BLACK)
save(im,'wave_template.png')
# vector component grid
im,d=new(); title(d,'Vector Components Grid',20,38); ox,oy,sx,sy=axes(d,(120,100,1480,1100),10,8,labels=True,grid=True); arrow(d,(ox,oy),(ox+6*sx,oy-5*sy),6,BLACK,24); d.line([(ox+6*sx,oy-5*sy),(ox+6*sx,oy)],fill=MID,width=4); d.line([(ox,oy-5*sy),(ox+6*sx,oy-5*sy)],fill=MID,width=4); d.text((ox+3*sx,oy-5*sy-45),'Vx',font=F(28,True),fill=BLACK); d.text((ox+6*sx+20,oy-2.5*sy),'Vy',font=F(28,True),fill=BLACK); save(im,'vector_components_grid.png')
# electric field grid
im,d=new(); title(d,'Electric Field Grid',20,38)
# light square grid
for i in range(17):
    x=140+i*82.5; d.line([(x,120),(x,1080)],fill=GRID,width=2)
for j in range(13):
    y=120+j*80; d.line([(140,y),(1460,y)],fill=GRID,width=2)
for x,sign in [(520,'+'),(1080,'−')]:
    d.ellipse((x-55,600-55,x+55,600+55),outline=BLACK,width=5); label_center(d,(x-55,545,x+55,655),sign,48,True)
save(im,'electric_field_grid.png')

# General science
im,d=new(); title(d,'SI Prefix Reference',24,40)
rows=[('G','giga','10⁹'),('M','mega','10⁶'),('k','kilo','10³'),('','base unit','10⁰'),('m','milli','10⁻³'),('μ','micro','10⁻⁶'),('n','nano','10⁻⁹')]
x0=250; y0=150; widths=[260,550,360]; headers=['Symbol','Prefix','Factor'];
for i,h in enumerate(headers): d.rectangle((x0+sum(widths[:i]),y0,x0+sum(widths[:i+1]),y0+90),outline=BLACK,width=3); label_center(d,(x0+sum(widths[:i]),y0,x0+sum(widths[:i+1]),y0+90),h,30,True)
for r,row in enumerate(rows):
    y=y0+90+r*120
    for i,val in enumerate(row):
        xa=x0+sum(widths[:i]); xb=x0+sum(widths[:i+1]); d.rectangle((xa,y,xb,y+120),outline=MID,width=2); label_center(d,(xa,y,xb,y+120),val,34,False)
save(im,'si_prefix_reference.png')
# metric ruler
im,d=new(1800,520); d.text((80,35),'Metric Ruler (centimeters / millimeters)',font=F(34,True),fill=BLACK); x0,x1=100,1700; y=320; d.line([(x0,y),(x1,y)],fill=BLACK,width=6)
for mm in range(0,201):
    x=x0+(x1-x0)*mm/200; ifh=110 if mm%10==0 else (75 if mm%5==0 else 45); d.line([(x,y),(x,y-ifh)],fill=BLACK,width=4 if mm%10==0 else 2)
    if mm%10==0: d.text((x-10,y+20),str(mm//10),font=F(23),fill=BLACK)
save(im,'metric_ruler.png')
# scientific notation scale
im,d=new(); title(d,'Scientific-Notation Scale',24,40); y=580; x0,x1=140,1460; arrow(d,(x0,y),(x1,y),5,BLACK,20); arrow(d,(x1,y),(x0,y),5,BLACK,20)
for e in range(-12,13,3):
    x=x0+(x1-x0)*(e+12)/24; d.line([(x,y-35),(x,y+35)],fill=BLACK,width=4); txt=f'10^{e}'; bb=d.textbbox((0,0),txt,font=F(28,True)); d.text((x-(bb[2]-bb[0])/2,y+55),txt,font=F(28,True),fill=BLACK)
d.text((170,360),'smaller magnitude',font=F(28),fill=DARK); d.text((1160,360),'larger magnitude',font=F(28),fill=DARK)
save(im,'scientific_notation_scale.png')
# sig figs reminder
im,d=new(); title(d,'Significant Figures Reminder',24,40); rules=[('1','All nonzero digits are significant.'),('2','Zeros between nonzero digits are significant.'),('3','Leading zeros are not significant.'),('4','Trailing zeros after a decimal are significant.'),('5','Exact counted quantities have unlimited significant figures.')]
for i,(n,txt) in enumerate(rules):
    y=170+i*180; d.ellipse((130,y,210,y+80),outline=BLACK,width=4); label_center(d,(130,y,210,y+80),n,30,True); d.text((250,y+18),txt,font=F(30),fill=BLACK)
save(im,'significant_figures_reminder.png')
# weather front symbols
im,d=new(); title(d,'Weather Front Symbols',22,38)
items=[('Cold front','triangles'),('Warm front','semis'),('Stationary front','stationary'),('Occluded front','occluded')]
for i,(lab,typ) in enumerate(items):
    y=230+i*220; d.text((120,y-55),lab,font=F(30,True),fill=BLACK); d.line([(420,y),(1420,y)],fill=BLACK,width=5)
    for k in range(6):
        x=500+k*150
        if typ in ('triangles','stationary','occluded') and (typ!='stationary' or k%2==0): d.polygon([(x,y),(x+30,y-45),(x+60,y)],outline=BLACK)
        if typ in ('semis','stationary','occluded') and (typ!='stationary' or k%2==1): d.arc((x,y-45,x+60,y+15),180,360,fill=BLACK,width=4)
save(im,'weather_front_symbols.png')
# data tables
im,d=new(); title(d,'Blank Data Table Templates',22,38)
# left 4x6
for bx,cols,rows in [(100,4,7),(880,3,10)]:
    x0=bx; y0=160; bw=560; bh=820
    for c in range(cols+1): x=x0+bw*c/cols; d.line([(x,y0),(x,y0+bh)],fill=BLACK if c in (0,cols) else MID,width=4 if c in (0,cols) else 2)
    for r in range(rows+1): y=y0+bh*r/rows; d.line([(x0,y),(x0+bw,y)],fill=BLACK if r in (0,rows) else MID,width=4 if r in (0,rows) else 2)
save(im,'blank_data_table_templates.png')
# graph paper variants
for name,step in [('graph_paper_fine.png',40),('graph_paper_coarse.png',80)]:
    im,d=new();
    for x in range(40,W,step): d.line([(x,20),(x,H-20)],fill=GRID,width=2)
    for y in range(40,H,step): d.line([(20,y),(W-20,y)],fill=GRID,width=2)
    d.rectangle((20,20,W-20,H-20),outline=MID,width=3); save(im,name)

print('done')
