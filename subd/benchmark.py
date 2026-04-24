import time
from main import MyDatabase
import seed


def run_benchmarks():
    db = MyDatabase()
    data = seed.generate_test_data(1000)

    print("--- Заполнение БД данными ---")
    for k, v in data:
        db.add_record(k, v)
    print(f"Записей добавлено: {len(data)}")

    point_queries, _ = seed.get_search_queries(1000)

    # 1. Тест без индекса
    print("\nЗапуск поиска БЕЗ индекса (Full Scan)...")
    start = time.perf_counter()
    for q in point_queries:
        db.get_by_key_no_index(q)
    end = time.perf_counter()
    print(f"Среднее время запроса (Scan): {(end - start) / 1000:.6f} сек")

    # 2. Тест с индексом
    print("Запуск поиска С индексом (B+Tree)...")
    start = time.perf_counter()
    for q in point_queries:
        db.get_by_key_with_index(q)
    end = time.perf_counter()
    print(f"Среднее время запроса (Index): {(end - start) / 1000:.6f} сек")


if __name__ == "__main__":
    run_benchmarks()
