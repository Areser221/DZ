#данные из таблицы (вес, ценность)
items = [
    (10, 40),
    (20, 90),
    (35, 120),
    (40, 100),
    (50, 80)
]
p_max = 135 #вместимость бекпека


def bober(items, p_max):
    # крч считаем удельную ценность цена\вес благодаря анонимной функции(lambda)
    sorted_items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)

    ans = 0
    for weight, value in sorted_items:
        if p_max >= weight:
            # Если предмет влезает целиком — забираем его
            p_max -= weight
            ans += value
        else:
            # Если не влезает отрезаем сколько надо
            chastichka = p_max / weight
            ans += value * chastichka
            break
    return ans


result = bober(items, p_max)
print(f"Максимальная ценность в рюкзаке: {result}")
