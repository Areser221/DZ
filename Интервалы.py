N = int(input('N: ')) # то сколько будет интервалов
s = [] #список куда будем складывать конец и начало интервалов
for i in range(N):
    s1 = []
    start = int(input('start: '))
    if start < 0:
        print('Начало времени не может быть отрицательно')
        exit()
    end = int(input('end: '))
    if end < 0:
        print('Конец времени не может быть отрицательно')
        exit() 
    s1.append(end)
    s1.append(start)
    s.append(s1)
cnt = 0
last = 0
#сортируем интервалы по времени окончания (end), так как я ранее записал их в виде [end, start]
s.sort()
for end, start in s:
    #если начало текущего интервала не пересекается с концом предыдущего, берем его
    if start >= last:
        cnt += 1
        last = end
print(cnt)