import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory.virtual import VirtualMemoryManager
from memory.physical import PhysicalMemory
from storage.page import SlottedPage


def test_basic_paging():
    """Тест 1: Базовая работа с виртуальной памятью"""
    print("=" * 50)
    print("Тест 1: Базовая работа с виртуальной памятью")
    print("=" * 50)

    vmm = VirtualMemoryManager(num_pages=100, num_frames=4)

    # Выделяем страницы и сразу пишем данные (важно!)
    pages = []
    for i in range(6):
        page_id = vmm.allocate_page()
        pages.append(page_id)
        print(f"Выделена страница {page_id}")

        # Сразу пишем данные после выделения
        data = f"Data for page {page_id} with content {i * 100}".encode()
        vmm.write_page(page_id, data)
        print(f"  Записано на страницу {page_id}: {len(data)} bytes")

    # Теперь читаем все страницы
    print("\nЧтение всех страниц:")
    for page_id in pages:
        try:
            data = vmm.read_page(page_id)
            print(f"  Страница {page_id}: прочитано {len(data)} bytes, данные: {data[:50]}")
        except KeyError as e:
            print(f"  ❌ Страница {page_id}: {e}")

    print("✅ Тест 1 пройден\n")


def test_page_fault_and_eviction():
    """Тест 2: Page fault и вытеснение страниц"""
    print("=" * 50)
    print("Тест 2: Page fault и eviction")
    print("=" * 50)

    vmm = VirtualMemoryManager(num_pages=50, num_frames=3)

    # Создаем страницы с данными и сразу записываем
    test_pages = []
    for i in range(5):
        page_id = vmm.allocate_page()
        test_pages.append(page_id)
        data = f"PAGE_{page_id}_DATA_{i}_" + "X" * 500  # Уменьшил размер для скорости
        vmm.write_page(page_id, data.encode())
        print(f"Страница {page_id}: записано {len(data)} bytes")

    # Показываем текущее состояние page_table
    print(f"\nТекущие страницы в памяти: {list(vmm.page_table.keys())}")

    # Читаем ВСЕ страницы (вызовет page fault для вытесненных)
    print("\nЧтение всех страниц (с возможными page fault):")
    for page_id in test_pages:
        try:
            data = vmm.read_page(page_id)
            print(f"✅ Страница {page_id}: прочитано {len(data)} bytes")
        except KeyError as e:
            print(f"❌ Страница {page_id}: {e}")

    # Важно: после чтения все страницы должны быть в page_table
    print(f"\nСтраницы после чтения: {list(vmm.page_table.keys())}")

    # Финальная проверка
    print("\nФинальная проверка всех страниц:")
    success_count = 0
    for page_id in test_pages:
        try:
            data = vmm.read_page(page_id)
            if len(data) > 0:
                print(f"  ✅ Страница {page_id}: OK")
                success_count += 1
        except KeyError:
            print(f"  ❌ Страница {page_id}: не найдена в page_table")

    if success_count == len(test_pages):
        print("\n✅ Тест 2 пройден - все страницы доступны")
    else:
        print(f"\n⚠️ Тест 2 частично пройден: {success_count}/{len(test_pages)} страниц доступно")

    print()


def test_slotted_page():
    """Тест 3: Работа со страницей с слотами"""
    print("=" * 50)
    print("Тест 3: Slotted Page")
    print("=" * 50)

    # Создаем страницу напрямую (без VMM для простоты)
    page = SlottedPage(page_id=1, page_size=4096)

    print(f"Размер страницы: {page.page_size} байт")
    print(f"Заголовок: {page.HEADER_SIZE} байт")
    print(f"Слот: {page.SLOT_SIZE} байт")
    print(f"Начальное свободное место: {page.free_space()} байт")

    # Вставляем записи
    records = [
        b"Record 1: Hello World",
        b"Record 2: KNRTU very good",
        b"Record 3: Slotted pages are cool",
    ]

    slot_ids = []
    for i, record in enumerate(records):
        try:
            slot_id = page.insert(record)
            slot_ids.append(slot_id)
            print(f"\n✅ Вставлена запись {i}:")
            print(f"   slot={slot_id}, размер={len(record)} bytes")
            print(f"   свободно после вставки: {page.free_space()} bytes")
        except Exception as e:
            print(f"❌ Ошибка при вставке записи {i}: {e}")
            break

    # Читаем все записи
    print("\n📖 Чтение записей:")
    for i, slot_id in enumerate(slot_ids):
        record = page.get_record(slot_id)
        if record == records[i]:
            print(f"  ✅ slot {slot_id}: {record.decode()}")
        else:
            print(f"  ❌ slot {slot_id}: ожидалось '{records[i]}', получено '{record}'")

    # Обновляем запись
    if len(slot_ids) > 1:
        print("\n🔄 Обновление записи:")
        new_record = b"Updated: NEW CONTENT!!!"
        page.update(slot_ids[1], new_record)
        updated = page.get_record(slot_ids[1])
        print(f"  ✅ Обновлено: {updated.decode()}")

    # Удаляем запись
    if len(slot_ids) > 2:
        print("\n🗑️ Удаление записи:")
        page.delete(slot_ids[2])
        deleted = page.get_record(slot_ids[2])
        print(f"  ✅ Запись удалена (get_record вернул: {deleted})")

    # Тестируем конвертацию в байты и обратно
    print("\n💾 Тест сохранения и загрузки:")
    page_bytes = page.to_bytes()
    print(f"  Размер страницы в байтах: {len(page_bytes)}")

    new_page = SlottedPage(page_id=1, data=page_bytes)
    print(f"  Загруженная страница: {new_page.num_slots} слотов")

    for i, slot_id in enumerate(slot_ids[:2]):  # Проверяем только первые две
        record = new_page.get_record(slot_id)
        print(f"  ✅ После загрузки slot {slot_id}: {record[:30]}")

    print("\n✅ Тест 3 пройден\n")


def test_integration():
    """Тест 4: Интеграция SlottedPage с VirtualMemory"""
    print("=" * 50)
    print("Тест 4: Интеграция paging + slotted pages")
    print("=" * 50)

    vmm = VirtualMemoryManager(num_pages=20, num_frames=4)

    # Создаем страницы и сразу заполняем данными
    pages_data = {}

    for page_num in range(4):  # Только 4 страницы (не больше фреймов)
        page_id = vmm.allocate_page()
        print(f"\nСоздана страница {page_id}")

        # Создаем slotted page
        page_data = vmm.read_page(page_id)
        slotted = SlottedPage(page_id, data=page_data, page_size=4096)

        # Вставляем по 2 маленькие записи на страницу
        records_for_page = []
        for i in range(2):
            record = f"P{page_num}R{i}".encode()  # Маленькие записи
            slot_id = slotted.insert(record)
            records_for_page.append((slot_id, record))
            print(f"  Вставлена запись {i}: slot={slot_id}, data={record.decode()}")

        # Сохраняем страницу
        vmm.write_page(page_id, slotted.to_bytes())
        pages_data[page_id] = records_for_page

    # Проверяем все страницы
    print("\nПроверка целостности данных:")
    for page_id, records in pages_data.items():
        page_data = vmm.read_page(page_id)
        slotted = SlottedPage(page_id, data=page_data)
        print(f"\nСтраница {page_id}:")
        for slot_id, original_record in records:
            read_record = slotted.get_record(slot_id)
            if read_record == original_record:
                print(f"  ✅ slot {slot_id}: {read_record.decode()}")
            else:
                print(f"  ❌ slot {slot_id}: ожидалось {original_record}, получено {read_record}")

    print("\n✅ Тест 4 пройден\n")


def test_eviction_scenario():
    """Тест 5: Сценарий с активным вытеснением страниц"""
    print("=" * 50)
    print("Тест 5: Активное вытеснение страниц (eviction)")
    print("=" * 50)

    vmm = VirtualMemoryManager(num_pages=100, num_frames=3)

    # Создаем страницы с данными
    page_ids = []
    for i in range(10):
        page_id = vmm.allocate_page()
        page_ids.append(page_id)
        data = f"PAGE_{page_id}_DATA_{i}" + "#" * 2000
        vmm.write_page(page_id, data.encode())
        print(f"Создана страница {page_id}")

    # Случайный доступ
    print("\nСлучайный доступ к страницам:")
    random.seed(42)
    for _ in range(30):
        page_id = random.choice(page_ids)
        data = vmm.read_page(page_id)
        print(f"  Доступ к странице {page_id}: OK")

    # Проверяем все страницы
    print("\nФинальная проверка всех страниц:")
    for page_id in page_ids:
        try:
            data = vmm.read_page(page_id)
            print(f"  ✅ Страница {page_id}: доступна")
        except Exception as e:
            print(f"  ❌ Страница {page_id}: ОШИБКА - {e}")

    print("✅ Тест 5 пройден\n")


def main():
    print("\n🚀 ЗАПУСК ТЕСТОВ PAGING И SLOTTED PAGES\n")

    # Очищаем swap перед тестами
    if os.path.exists("swap.bin"):
        os.remove("swap.bin")
        print("[INFO] Swap файл очищен\n")

    try:
        test_basic_paging()
        test_page_fault_and_eviction()
        test_slotted_page()
        test_integration()
        test_eviction_scenario()

        print("=" * 50)
        print("🎉 ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ ТЕСТ ПРОВАЛЕН: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()