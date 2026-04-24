import struct
from memory.virtual import VirtualMemory
from storage.heap_file import HeapFile
from indexes.bplus_tree import BPlusTree
import seed

class MyDatabase:
    def __init__(self):
        # Настраиваем память: 10 фреймов по 1024 байта (мало, чтобы вызвать eviction)
        self.v_memory = VirtualMemory(num_frames=10, page_size=1024)
        self.storage = HeapFile(self.v_memory)
        self.index = BPlusTree(t=5)

    def add_record(self, key, data):
        # Упаковываем ключ и данные: [int_key (I)] + [data]
        record_bytes = struct.pack("<I", key) + data
        # Сохраняем в HeapFile
        record_id = self.storage.insert(record_bytes)
        # Обновляем индекс
        self.index.insert(key, record_id)

    def get_by_key_no_index(self, key):
        """Поиск полным сканированием (O(N))"""
        # Проходим по всем страницам, которые создал HeapFile
        for v_id in self.storage.page_ids:
            page_data = self.v_memory.get_page(v_id)
            from storage.page import SlottedPage
            page = SlottedPage(page_data)

            count, _ = page.get_header()
            for slot_id in range(count):
                rec = page.get_record(slot_id)
                if rec:
                    # Извлекаем ключ (первые 4 байта)
                    k = struct.unpack_from("<I", rec, 0)[0]  # Добавил [0], чтобы получить число из кортежа
                    if k == key:
                        return rec[4:]  # Возвращаем данные без ключа
        return None

    def get_by_key_with_index(self, key):
        """Поиск через B+Tree (O(log N))"""
        rid = self.index.search(key)
        if rid is not None:  # Добавили проверку на None
            rec = self.storage.select_by_id(rid)
            return rec[4:] if rec else None
        return None

