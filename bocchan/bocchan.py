import numpy as np
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = 'AppleGothic'
import matplotlib.pyplot as plt

aiueo = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ、。アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポー…―っッゃゅょャュョ「」'


#読み取ってaに格納
with open('bocchan.txt', encoding='shift_jis') as r:
    a=list(r.read())


#《》などのいらないところを探して消す。
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
        


#a[i]の前後500文字以内に同じ文字が何個あるかをb[i]に格納
b=np.zeros((len(a)))
for i in range(500,len(a)-500):
    if not a[i] in aiueo:
        for j in range(-500,500):
            if a[i]==a[i+j]:
                b[i] = b[i] + 1


#('字',(位置)のリスト,(文字数)のリスト)のリストcを作る
c=[]
for i in range(500,len(a)-500):
    if a[i] in aiueo:
        continue
    elif a[i] in a[0:i]:
        for j in range(len(c)):
            if c[j][0] == a[i]:
                c[j][1].append((i))
                c[j][2].append((b[i]))
    else:
        c.append((a[i],[(i)],[(b[i])]))
        
        

#グラフを描画する
for i in range(len(c)):
    x_data = c[i][1]
    y_data = c[i][2]
    y_max = max(y_data)
    if y_max > 10:
        plt.plot(x_data, y_data, label=c[i][0], alpha=0.5)
        for j in range(len(c[i][1])):
            if c[i][2][j] == y_max:
                x_max = c[i][1][j]
                plt.annotate(c[i][0], xy=(x_max,y_max), fontsize=10)
                break
    else:
        plt.plot(x_data, y_data, alpha=0.1)
plt.show()



