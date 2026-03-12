import heapq
from collections import Counter

text = "abracadabra"


def get_huffman_codes(data):
    #считаем частоту каждого символа
    frequencies = Counter(data)

    #создаем "кучу" (heap), где каждый элемент - [частота, [символ, код]]
    # В начале код у всех пустой
    nodes = [[freq, [char, ""]] for char, freq in frequencies.items()]
    heapq.heapify(nodes)

    #строим дерево: берем два узла с мин. частотой и объединяем
    while len(nodes) > 1:
        low = heapq.heappop(nodes)
        high = heapq.heappop(nodes)

        #всем символам из левой ветки добавляем "0", из правой - "1"
        for pair in low[1:]:
            pair[1] = "0" + pair[1]
        for pair in high[1:]:
            pair[1] = "1" + pair[1]

        #кладем объединенный узел обратно в кучу
        heapq.heappush(nodes, [low[0] + high[0]] + low[1:] + high[1:])

    #получаем финальный словарь с кодами
    final_node = heapq.heappop(nodes)
    codes = dict(final_node[1:])
    return codes, frequencies


huffman_codes, freqs = get_huffman_codes(text)
text_length = len(text)

#считаем среднюю длину кода (L_avg)
avg_length = sum((freqs[char] / text_length) * len(code) for char, code in huffman_codes.items())

#Вывод
print(f"Коды символов для слова '{text}':")
for char in sorted(huffman_codes):
    print(f"'{char}': {huffman_codes[char]}")

print(f"Средняя длина кода (L_avg): {avg_length:.2f}")
