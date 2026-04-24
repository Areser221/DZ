import random

def generate_test_data(count=1000):
    random.seed(42)  # Для воспроизводимости
    data = []
    for i in range(count):
        # Генерируем ключ и случайную строку данных
        key = i
        payload = f"value_{random.randint(1, 10000)}".encode()
        data.append((key, payload))
    return data

def get_search_queries(count=1000, max_range=1000):
    random.seed(99)
    # Точечные запросы
    point_queries = [random.randint(0, max_range-1) for _ in range(count)]
    # Диапазонные запросы (для B+Tree)
    range_queries = []
    for _ in range(count):
        a = random.randint(0, max_range-10)
        b = a + random.randint(1, 10)
        range_queries.append((a, b))
    return point_queries, range_queries
