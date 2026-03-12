#набор номиналов
money = [1, 5, 10, 25]
target = 99


def get_min_coins(coins, total_amount):
    #cортируем от большего к меньшему
    coins.sort(reverse=True)

    #cловарь для хранения результата: {номинал: количество}
    result = {}

    for coin in coins:
        if total_amount >= coin:
            # cчитаем, сколько раз монета "влезает" в остаток суммы
            count = total_amount // coin
            result[coin] = count
            # оставляем только остаток от деления
            total_amount %= coin

    return result


ans = get_min_coins(money, target)

print(f"Чтобы получить вот столько {target}, надо взять:")
for coin, count in ans.items():
    print(f"Стоимость монеты {coin}: {count} штучек")
