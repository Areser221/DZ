a = input('Введите значение N и M через пробел: ').split()
N = int(a[0])
M = int(a[1])
s = []
for i in range(M):
    b = input('введите u и v: ').split()
    x = [int(b[0]),int(b[1])]
    s.append(x)
s = sorted(s)
s1 = []
for u, v in s:
    x = [v,u]
    s1.append(x)
for i in range(len(s1)):
    s.append(s1[i])
#получил все связи пользователей друг с другом
#Создаем список посещенных пользователей. Сначала все False.
visited = [False] * N

comp_cnt = 0  # Счётчик количества компаний
max_size = 0  # Размер самой большой компании

#Перебираем каждого пользователя от 0 до N-1
for i in range(N):
    # Если мы этого человека еще не рассматривали, значит нашли новую компанию!
    if visited[i] == False:
        comp_cnt += 1
        
        # Начинаем собирать всех членов этой компании в список `queue`
        queue = [i]
        visited[i] = True  # Отмечаем первого участника как посещенного
        
        # Текущий размер этой компании
        current_size = 0
        
        # Пока в нашей компании есть люди, которых мы еще не "обработали"
        while len(queue) > 0:
            # Берем первого человека из списка и убираем его оттуда
            current_user = queue.pop(0)
            current_size += 1  # Считаем его +1 к размеру компании
            
            # Ищем всех его друзей в нашем списке всех связей s
            for u, v in s:
                if u == current_user:
                    if visited[v] == False:
                        visited[v] = True  # Отмечаем друга
                        queue.append(v)    # Добавляем в список на обработку
                        
        # Когда цикл while закончился — вся компания успешно собрана!
        # Проверяем, не больше ли она, чем наш текущий максимум
        if current_size > max_size:
            max_size = current_size
print(comp_cnt, max_size)

