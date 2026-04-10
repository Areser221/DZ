# storage/page.py (исправленная версия с правильной компактификацией)
import struct


class SlottedPage:
    HEADER_FORMAT = ">II"  # num_slots, free_offset
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    SLOT_FORMAT = ">II"  # offset, length
    SLOT_SIZE = struct.calcsize(SLOT_FORMAT)

    def __init__(self, page_id, data=None, page_size=4096):
        self.page_id = page_id
        self.page_size = page_size

        if data is None:
            # Создаем новую пустую страницу
            self.data = bytearray(page_size)
            self.num_slots = 0
            self.free_offset = page_size  # Начинаем с конца
            self.slots = []
            self._write_header()
        else:
            # Загружаем существующую страницу
            self.data = bytearray(data)
            self._read_header()
            self._read_slots()

    def _write_header(self):
        """Записывает заголовок страницы"""
        # Убеждаемся, что значения в допустимых пределах
        if self.free_offset < 0 or self.free_offset > self.page_size:
            print(f"[ERROR] Invalid free_offset: {self.free_offset}")
            self.free_offset = max(0, min(self.page_size, self.free_offset))
        if self.num_slots < 0:
            self.num_slots = 0

        struct.pack_into(self.HEADER_FORMAT, self.data, 0, self.num_slots, self.free_offset)

    def _read_header(self):
        """Читает заголовок страницы"""
        self.num_slots, self.free_offset = struct.unpack_from(self.HEADER_FORMAT, self.data, 0)

    def _write_slots(self):
        """Записывает все слоты"""
        offset = self.HEADER_SIZE
        for slot_offset, slot_length in self.slots:
            if slot_offset < 0 or slot_offset > self.page_size:
                print(f"[ERROR] Invalid slot_offset: {slot_offset}")
                slot_offset = max(0, min(self.page_size, slot_offset))
            struct.pack_into(self.SLOT_FORMAT, self.data, offset, slot_offset, slot_length)
            offset += self.SLOT_SIZE

    def _read_slots(self):
        """Читает все слоты"""
        self.slots = []
        offset = self.HEADER_SIZE
        for _ in range(self.num_slots):
            slot_offset, slot_length = struct.unpack_from(self.SLOT_FORMAT, self.data, offset)
            if slot_length > 0:  # Только живые записи
                self.slots.append((slot_offset, slot_length))
            offset += self.SLOT_SIZE

    def _calculate_free_space(self):
        """Вычисляет свободное место на странице"""
        # Место, занятое заголовком и слотами
        header_used = self.HEADER_SIZE + (len(self.slots) * self.SLOT_SIZE)
        # Место, занятое данными
        data_used = sum(length for _, length in self.slots if length > 0)
        free = self.page_size - (header_used + data_used)
        return max(0, free)

    def insert(self, record_data):
        """Вставляет запись и возвращает номер слота"""
        record_len = len(record_data)

        # Проверяем, есть ли место
        needed = record_len + self.SLOT_SIZE
        free = self._calculate_free_space()

        print(f"[DEBUG] Insert: need={needed}, free={free}, record_len={record_len}")

        if free < needed:
            # Пытаемся сделать компактификацию
            self._compact()
            free = self._calculate_free_space()
            if free < needed:
                raise Exception(f"Page full: need {needed} bytes, have {free} bytes")

        # Размещаем данные с конца
        new_offset = self.free_offset - record_len

        # Проверяем, не пересекаемся ли с заголовком
        min_offset = self.HEADER_SIZE + (len(self.slots) + 1) * self.SLOT_SIZE
        if new_offset < min_offset:
            # Делаем компактификацию и пробуем снова
            self._compact()
            new_offset = self.free_offset - record_len
            min_offset = self.HEADER_SIZE + (len(self.slots) + 1) * self.SLOT_SIZE
            if new_offset < min_offset:
                raise Exception(f"Not enough space even after compaction")

        # Записываем данные
        self.data[new_offset:new_offset + record_len] = record_data

        # Добавляем слот
        slot_idx = len(self.slots)
        self.slots.append((new_offset, record_len))
        self.free_offset = new_offset

        # Обновляем заголовок и слоты
        self.num_slots = len(self.slots)
        self._write_header()
        self._write_slots()

        return slot_idx

    def get_record(self, slot_idx):
        """Получает запись по номеру слота"""
        if slot_idx >= len(self.slots):
            return None

        offset, length = self.slots[slot_idx]
        if length == 0:
            return None

        return bytes(self.data[offset:offset + length])

    def update(self, slot_idx, new_data):
        """Обновляет запись"""
        if slot_idx >= len(self.slots):
            raise IndexError(f"Invalid slot {slot_idx}")

        old_offset, old_len = self.slots[slot_idx]
        new_len = len(new_data)

        if new_len <= old_len:
            # Новые данные помещаются в старое место
            self.data[old_offset:old_offset + new_len] = new_data
            self.slots[slot_idx] = (old_offset, new_len)
        else:
            # Нужно переместить запись
            self.delete(slot_idx)
            new_slot_idx = self.insert(new_data)
            # Меняем слоты местами, чтобы сохранить индекс
            if new_slot_idx != slot_idx:
                self.slots[slot_idx], self.slots[new_slot_idx] = self.slots[new_slot_idx], self.slots[slot_idx]

        self._write_header()
        self._write_slots()

    def delete(self, slot_idx):
        """Помечает запись как удаленную"""
        if slot_idx >= len(self.slots):
            raise IndexError(f"Invalid slot {slot_idx}")

        # Помечаем длину как 0 (удалено)
        offset, _ = self.slots[slot_idx]
        self.slots[slot_idx] = (offset, 0)
        self._write_slots()

    def _compact(self):
        """Дефрагментация страницы"""
        print("[DEBUG] Compacting page...")

        # Собираем только живые записи
        live_records = [(offset, length) for offset, length in self.slots if length > 0]

        if not live_records:
            self.free_offset = self.page_size
            self.slots = []
            self.num_slots = 0
            self._write_header()
            self._write_slots()
            return

        # Сортируем по смещению (от конца к началу)
        live_records.sort(key=lambda x: x[0], reverse=True)

        new_offset = self.page_size
        new_slots = []

        for old_offset, length in live_records:
            new_offset -= length
            # Копируем данные на новое место
            if new_offset != old_offset:
                self.data[new_offset:new_offset + length] = self.data[old_offset:old_offset + length]
            new_slots.append((new_offset, length))

        # Обновляем слоты (сохраняем порядок)
        self.slots = new_slots
        self.free_offset = new_offset
        self.num_slots = len(self.slots)
        self._write_header()
        self._write_slots()

        print(f"[DEBUG] Compaction complete: {self.num_slots} slots, free_offset={self.free_offset}")

    def to_bytes(self):
        """Возвращает байтовое представление страницы"""
        return bytes(self.data)

    def free_space(self):
        """Возвращает свободное место на странице"""
        return self._calculate_free_space()