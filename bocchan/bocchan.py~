import numpy as np
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = 'AppleGothic'
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy import optimize
from scipy.interpolate import PchipInterpolator

aiueo = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ、。アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポー…―っッゃゅょャュョ「」-:|：｜'

#読み取り
with open('bocchan.txt', encoding='shift_jis') as r:
    string=r.read()

a=list(string)


#《》で囲われたルビを消す
rubi = False
for i in range(len(a)):
    if a[i] == '《' or a[i] == '[':
        rubi = True
        a[i] = 'rubi'
    elif a[i] == '》' or a[i] == ']':
        a[i] = 'rubi'
        rubi = False
    elif rubi == True:
        a[i] = 'rubi'

while 'rubi' in a:
    a.remove('rubi')
while '\n' in a:
    a.remove('\n')
        


#解析
#b=np.zeros((len(a)))
#for i in range(500,len(a)-500):
#    if not a[i] in aiueo:
#        for j in range(-500,500):
#            if a[i]==a[i+j]:
#                b[i] = b[i] + 1

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

        

for i in range(len(c)):  
    ci=c[i][1]
    for j in range(len(ci)):
        temp = 0
        for k in range(len(ci)): 
            if ci[j][0] - 1000 < ci[k][0] and ci[k][0] < ci[j][0] + 1000:
                temp = temp + 1
        ci[j][1] = temp
        

c = [x for x in c if max([z for [y,z] in x[1]]) > 5]
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
    x_data = [x for [x,y] in ci]
    y_data = [y for [x,y] in ci]
    cubic_interp = PchipInterpolator(x_data, y_data)
    x_data2 = list(range(x_data[0],x_data[-1],100))
    y_data2 = cubic_interp(x_data2)
    in_xlist=[]
    for j in range(len(x_data2)):
        in_xlist=in_xlist+[(x_data2[j],y_data2[j])]
    xlist=xlist+[in_xlist]


selected = np.zeros(lenc, dtype=int)

r = np.zeros(lenc)
g = np.random.rand(lenc)
b = np.random.rand(lenc)
a = np.ones(lenc)*0.2
colors = np.array([r,g,b,a]).T

def color_on(selected):
    for i in range(len(selected)):
        if selected[i]:
            colors[i] = [1,0,0,1]
        else:
            colors[i] = np.array([r,g,b,a]).T[i]
    return colors

lines = LineCollection(xlist, pickradius=5, colors=colors, cmap=plt.cm.RdYlGn, linewidths = 0.5)
lines.set_picker(True)

ax.add_collection(lines)
ax.set_ylim(0,30)
ax.set_xlim(0,90000)

annot = ax.annotate("a", xy=(0,0), xytext=(0,5),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"))
annot.set_visible(False)

def ann(ind):
    annot.xy=poss[ind]
    annot.set_text(labels[ind])
    annot.get_bbox_patch().set_alpha(0.4)
    annot.set_visible(selected[ind])
    

def on_pick(evt):
    if evt.artist is lines:
        ind = evt.ind[0]
        selected[ind] = 1 - selected[ind]
        selected[0:ind] = np.zeros(ind, dtype=int)
        selected[ind+1:] = np.zeros(len(xlist)-ind-1, dtype=int)
        lines.set_color(color_on(selected))
        ann(ind)
        fig.canvas.draw_idle()
    

fig.canvas.mpl_connect("pick_event", on_pick)
plt.show()
