import struct


class SlottedPage:
    # Структура заголовка: [count (H), free_space_offset (H)] (4 байта)
    HEADER_FORMAT = "<HH"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    # Структура слота: [offset (H), length (H)] (4 байта)
    SLOT_SIZE = 4

    def __init__(self, buffer):
        self.buffer = buffer  # bytearray из физической памяти
        self.page_size = len(buffer)

    def format(self):
        """Инициализация новой пустой страницы"""
        struct.pack_into(self.HEADER_FORMAT, self.buffer, 0, 0, self.page_size)

    def get_header(self):
        return struct.unpack_from(self.HEADER_FORMAT, self.buffer, 0)

    def set_header(self, count, offset):
        struct.pack_into(self.HEADER_FORMAT, self.buffer, 0, count, offset)

    def insert_record(self, data):
        count, free_offset = self.get_header()
        data_len = len(data)

        # Проверяем, хватит ли места (слот + данные)
        needed_space = self.SLOT_SIZE + data_len
        current_free_end = free_offset
        current_slots_end = self.HEADER_SIZE + (count * self.SLOT_SIZE)

        if current_free_end - current_slots_end < needed_space:
            return None  # Места нет

        # 1. Записываем данные в конец свободного места
        new_free_offset = free_offset - data_len
        self.buffer[new_free_offset:free_offset] = data

        # 2. Добавляем слот
        slot_pos = self.HEADER_SIZE + (count * self.SLOT_SIZE)
        struct.pack_into("<HH", self.buffer, slot_pos, new_free_offset, data_len)

        # 3. Обновляем заголовок
        self.set_header(count + 1, new_free_offset)
        return count  # Возвращаем ID слота в этой странице

    def get_record(self, slot_id):
        count, _ = self.get_header()
        if slot_id >= count: return None

        slot_pos = self.HEADER_SIZE + (slot_id * self.SLOT_SIZE)
        offset, length = struct.unpack_from("<HH", self.buffer, slot_pos)
        if length == 0: return None  # Запись удалена

        return self.buffer[offset: offset + length]
