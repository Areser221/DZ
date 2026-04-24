from .page import SlottedPage


class HeapFile:
    def __init__(self, v_memory):
        self.v_memory = v_memory
        self.page_ids = []  # Список Virtual Page IDs, принадлежащих таблице

    def insert(self, data_bytes):
        # 1. Пытаемся вставить в существующие страницы
        for v_id in self.page_ids:
            page_data = self.v_memory.get_page(v_id)
            page = SlottedPage(page_data)
            slot_id = page.insert_record(data_bytes)
            if slot_id is not None:
                return (v_id, slot_id)  # Это наш RecordID

        # 2. Если места нет, выделяем новую страницу
        new_v_id = self.v_memory.allocate_v_page()
        self.page_ids.append(new_v_id)

        # Инициализируем страницу (нужно сначала получить её через Page Fault)
        page_data = self.v_memory.get_page(new_v_id)
        page = SlottedPage(page_data)
        page.format()

        slot_id = page.insert_record(data_bytes)
        return (new_v_id, slot_id)

    def select_by_id(self, record_id):
        v_id, slot_id = record_id
        page_data = self.v_memory.get_page(v_id)
        page = SlottedPage(page_data)
        return page.get_record(slot_id)

    def scan(self):
        """Полный перебор (Full Table Scan) для тестов без индекса"""
        results = []
        for v_id in self.page_ids:
            page_data = self.v_memory.get_page(v_id)
            page = SlottedPage(page_data)
            count, _ = page.get_header()
            for slot_id in range(count):
                rec = page.get_record(slot_id)
                if rec:
                    results.append(rec)
        return results
