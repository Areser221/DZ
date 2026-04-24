import os
import struct
from memory.virtual import VirtualMemory
from storage.heap_file import HeapFile

def test_memory_and_eviction():
    print("=== Тест 1: Виртуальная память и Eviction ===")
    # Всего 2 фрейма в физ. памяти по 64 байта
    v_mem = VirtualMemory(num_frames=2, page_size=64)
    storage = HeapFile(v_mem)

    print("Добавляем данные, чтобы заполнить больше 2-х страниц...")
    for i in range(5):
        # Каждая запись по 20 байт гарантирует быстрое заполнение страниц
        data = f"data_val_{i}".encode().ljust(20, b'#')
        rid = storage.insert(data)
        print(f"Вставлена запись {i} в RecordID: {rid}")

    print("\nПроверяем наличие файла свапа...")
    if os.path.exists("swap.bin") and os.path.getsize("swap.bin") > 0:
        print(f"Успех! Файл swap.bin создан, размер: {os.path.getsize('swap.bin')} байт")
    else:
        print("Ошибка: своп не создался!")

    print("\n=== Тест 2: Чтение данных из свапа (Page Fault) ===")
    # Пытаемся прочитать самую первую запись (она точно уже в свопе)
    first_rec = storage.select_by_id((0, 0))
    if first_rec:
        print(f"Данные успешно подняты из свопа: {first_rec.decode().strip('#')}")

if __name__ == "__main__":
    # Удаляем старый своп перед тестом
    if os.path.exists("swap.bin"): os.remove("swap.bin")
    test_memory_and_eviction()
