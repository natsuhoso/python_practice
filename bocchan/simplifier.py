
with open('bocchan.txt', encoding='shift_jis') as r:
    string=r.read()

a=list(string)


rubi = False
for i in range(len(a)):
    if a[i] == '《' or a[i] == '［':
        rubi = True
        a[i] = 'rubi'
    elif a[i] == '》' or a[i] == '］':
        a[i] = 'rubi'
        rubi = False
    elif rubi == True:
        a[i] = 'rubi'

while 'rubi' in a:
    a.remove('rubi')
while '\n' in a:
    a.remove('\n')
while '｜' in a:
    a.remove('｜')
    
with open('bocchan-simplified.txt', mode='w', encoding='shift_jis') as w:
    w.write(''.join(a))
