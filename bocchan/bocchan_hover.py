import numpy as np
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = 'AppleGothic'
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy import optimize
from scipy.interpolate import PchipInterpolator
import copy

aiueo = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ、。アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポー…―っッゃゅょャュョ「」-:|：｜'

#読み取り
with open('bocchan-simplified.txt', encoding='shift_jis') as r:
    string=r.read()

a=list(string)


lena=len(a)


c=[]
for i in range(len(a)):
    if a[i] in aiueo:
        continue
    elif a[i] in a[0:i]:
        for j in range(len(c)):
            if c[j][0] == a[i]:
                c[j][1].append([i,0])
    else:
        c.append((a[i],[[i,0]]))

def gause(x,a,b):
    return np.exp(-((x-a)**2/b**2))

for i in range(len(c)):  
    ci=c[i][1]
    for j in range(len(ci)):
        temp = 0
        for k in range(len(ci)): 
            temp = temp + gause(ci[k][0],ci[j][0],10000)
        ci[j][1] = temp

c = [x for x in c if max([z for [y,z] in x[1]]) > 20]
lenc = len(c)
#kanjiは('字',(位置,文字数)のリスト)のリスト


fig, ax = plt.subplots()
labels = [x for (x,y) in c]
#xlist = [y for (x,y) in c]

poss = []
for i in range(lenc):
    y_max = max([y for (x,y) in c[i][1]])
    for j in range(len(c[i][1])):
        if c[i][1][j][1] is y_max:
            x_max = c[i][1][j][0]
            break
    poss=poss+[(x_max,y_max)]

xlist=[]
for i in range(lenc):
    ci=c[i][1]
    x_data2 = [x for [x,y] in ci]
    y_data2 = [y for [x,y] in ci]
    #cubic_interp = PchipInterpolator(x_data, y_data)
    #x_data2 = list(range(x_data[0],x_data[-1],100))
    #y_data2 = cubic_interp(x_data2)
    in_xlist=[]
    for j in range(len(x_data2)):
        in_xlist=in_xlist+[(x_data2[j],y_data2[j])]
    xlist=xlist+[in_xlist]


selected = np.zeros(lenc, dtype=int)

r = np.zeros(lenc)
g = np.random.rand(lenc)
b = np.random.rand(lenc)
a = np.ones(lenc)*0.2
defalt_colors = np.array([r,g,b,a]).T

def color_on(num):
    colors = copy.copy(defalt_colors)
    colors[num] = [1,0,0,1]
    return colors

lines = LineCollection(xlist, pickradius=3, colors=defalt_colors, cmap=plt.cm.RdYlGn, linewidths = 0.5)
lines.set_picker(True)

ax.add_collection(lines)
ax.set_ylim(0,110)
ax.set_xlim(0,lena)

annot = ax.annotate("a", xy=(0,0), xytext=(0,5),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"))
annot.set_visible(False)

def ann(ind):
    annot.xy=poss[ind]
    annot.set_text(labels[ind])
    annot.get_bbox_patch().set_alpha(0.4)
    #annot.set_visible(selected[ind])


def hover(evt):
    vis = annot.get_visible()
    if evt.inaxes == ax:
        hit, ind = lines.contains(evt)
        num = ind['ind'][0]
        if hit:
            selected[num] = 1
            lines.set_color(color_on(num))
            ann(num)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        elif vis:
            selected[0:] = np.zeros(lenc, dtype=int)
            lines.set_color(defalt_colors)
            annot.set_visible(False)
            fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()
