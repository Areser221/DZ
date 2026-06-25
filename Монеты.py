a = input('Введите значение K и S через пробел: ').split()
x=[]
for i in range(len(a)):
    x.append(int(a[i]))
coins = []
K = x[0]
S = x[1]
res = []
for i in range(K):
    s1=[]
    b = input('Введите значение nominal и count через пробел: ').split()
    nominal = int(b[0])
    count = int(b[1])
    s1.append(nominal)
    s1.append(count)
    res.append(s1)
for nominal, count in res:
    needed = S//nominal
    taken = min(needed, count)
    S = S-taken*nominal
    coins.append((nominal,taken))
if S ==0:
    for nominal, taken in coins:
        print(nominal,": ",taken)
else:
    print("Impossible")

