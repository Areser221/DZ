#cписок занятий: (время_начала, время_окончания)
lessons = [
    (1, 3),
    (2, 5),
    (4, 6),
    (6, 7)
]


def get_max_lessons(schedule):
    # 1. Сортируем занятия по времени конца (второй элемент кортежа)
    schedule.sort(key=lambda x: x[1])

    selected_lessons = []
    last_finish_time = 0

    for start, end in schedule:
        # Если занятие начинается после (или в момент) окончания предыдущего
        if start >= last_finish_time:
            selected_lessons.append((start, end))
            # Обновляем время окончания последнего выбранного занятия
            last_finish_time = end

    return selected_lessons

result = get_max_lessons(lessons)

print(f"максимальное количество занятий на которое мы можем успеть: {len(result)}")
print(f"Типа расписание(со скольки до скольки будут уроки): {result}")
