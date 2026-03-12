#отрезки из таблицы: (начало, конец)
segments = [
    (1, 4),
    (2, 5),
    (5, 6),
    (7, 9)
]
#не забывай что конец тут невключительно

def get_min_points(seg_list):
    #Сортируем отрезки по их концу
    seg_list.sort(key=lambda x: x[1])

    points = []
    #ставим первую точку в конец самого первого отрезка
    last_point = seg_list[0][1]-1
    points.append(last_point)

    for start, end in seg_list:
        # Если начало текущего отрезка больше, чем наша последняя точка,
        # значит этот отрезок не покрыт
        if start > last_point:
            last_point = end-1
            points.append(last_point)

    return points


# Запуск
result_points = get_min_points(segments)

print(f"Minimum points needed: {len(result_points)}")
print(f"Points coordinates: {result_points}")
