# memory/virtual.py
from .physical import PhysicalMemory
from .swap import SwapFile


class VirtualMemoryManager:
    def __init__(self, num_pages=1024, num_frames=64):
        self.phys_mem = PhysicalMemory(num_frames)
        self.swap = SwapFile()
        self.page_table = {}  # page_id -> (frame_idx, in_memory, dirty)
        self.frame_to_page = [-1] * num_frames  # frame index -> page_id
        self.next_page_id = 0
        print(f"[DEBUG] Инициализация VMM: {num_frames} фреймов")

    def allocate_page(self):
        """Выделяет новую виртуальную страницу"""
        page_id = self.next_page_id
        self.next_page_id += 1
        print(f"[DEBUG] allocate_page: создаем страницу {page_id}")

        # Ищем свободный фрейм
        for i in range(self.phys_mem.num_frames):
            if self.frame_to_page[i] == -1:
                print(f"[DEBUG] Найден свободный фрейм {i}")
                self.frame_to_page[i] = page_id
                self.page_table[page_id] = (i, True, False)
                return page_id

        # Нет свободных фреймов - вытесняем
        print(f"[DEBUG] Нет свободных фреймов, выполняем eviction")
        victim_frame = self.phys_mem.clock.evict()
        evicted_page = self.frame_to_page[victim_frame]
        print(f"[DEBUG] Вытесняем страницу {evicted_page} из фрейма {victim_frame}")

        # Сохраняем вытесненную страницу в swap
        if evicted_page != -1 and evicted_page in self.page_table:
            _, _, dirty = self.page_table[evicted_page]
            if dirty:
                print(f"[DEBUG] Страница {evicted_page} dirty, сохраняем в swap")
                data = self.phys_mem.read_frame(victim_frame)
                self.swap.write_page(evicted_page, data)
            # НЕ УДАЛЯЕМ из page_table, а помечаем как не в памяти
            self.page_table[evicted_page] = (victim_frame, False, dirty)
            print(f"[DEBUG] Страница {evicted_page} помечена как не в памяти")

        # Выделяем фрейм для новой страницы
        self.frame_to_page[victim_frame] = page_id
        self.page_table[page_id] = (victim_frame, True, False)
        self.phys_mem.write_frame(victim_frame, bytearray(PhysicalMemory.PAGE_SIZE))

        return page_id

    # memory/virtual.py (исправленная версия read_page)
    def read_page(self, page_id):
        """Читает данные со страницы"""
        print(f"[DEBUG] read_page: попытка чтения страницы {page_id}")

        # Если страница не в page_table, возможно она была вытеснена
        if page_id not in self.page_table:
            # Пытаемся восстановить из swap
            print(f"[PAGE FAULT] Страница {page_id} не в page_table, проверяем swap...")
            data = self.swap.read_page(page_id)
            if data is not None:
                # Восстанавливаем страницу из swap
                print(f"[PAGE FAULT] Страница {page_id} найдена в swap, восстанавливаем...")

                # Находим или выделяем фрейм
                free_frame = -1
                for i in range(self.phys_mem.num_frames):
                    if self.frame_to_page[i] == -1:
                        free_frame = i
                        break

                if free_frame == -1:
                    # Вытесняем какую-то страницу
                    victim_frame = self.phys_mem.clock.evict()
                    evicted_page = self.frame_to_page[victim_frame]
                    if evicted_page != -1:
                        # Сохраняем вытесненную страницу если она dirty
                        if evicted_page in self.page_table:
                            _, _, dirty = self.page_table[evicted_page]
                            if dirty:
                                old_data = self.phys_mem.read_frame(victim_frame)
                                self.swap.write_page(evicted_page, old_data)
                            del self.page_table[evicted_page]
                    free_frame = victim_frame

                # Загружаем данные в фрейм
                self.phys_mem.write_frame(free_frame, data)
                self.frame_to_page[free_frame] = page_id
                self.page_table[page_id] = (free_frame, True, False)
                print(f"[PAGE FAULT] Страница {page_id} восстановлена во фрейм {free_frame}")
                return data
            else:
                raise KeyError(f"Page {page_id} not allocated and not found in swap")

        # Нормальное чтение из памяти
        frame_idx, in_mem, dirty = self.page_table[page_id]

        if in_mem:
            # Страница в памяти
            print(f"[DEBUG] Страница {page_id} в памяти, читаем")
            self.phys_mem.clock.access(frame_idx)
            return self.phys_mem.read_frame(frame_idx)
        else:
            # Page fault - страница помечена как не в памяти, но должна быть в swap
            print(f"[PAGE FAULT] Страница {page_id} помечена как не в памяти, загружаем...")
            data = self.swap.read_page(page_id)
            if data is None:
                data = bytearray(PhysicalMemory.PAGE_SIZE)

            # Находим свободный фрейм
            free_frame = -1
            for i in range(self.phys_mem.num_frames):
                if self.frame_to_page[i] == -1:
                    free_frame = i
                    break

            if free_frame == -1:
                victim_frame = self.phys_mem.clock.evict()
                evicted_page = self.frame_to_page[victim_frame]
                if evicted_page != -1 and evicted_page in self.page_table:
                    _, _, old_dirty = self.page_table[evicted_page]
                    if old_dirty:
                        old_data = self.phys_mem.read_frame(victim_frame)
                        self.swap.write_page(evicted_page, old_data)
                    del self.page_table[evicted_page]
                free_frame = victim_frame

            # Загружаем данные
            self.phys_mem.write_frame(free_frame, data)
            self.frame_to_page[free_frame] = page_id
            self.page_table[page_id] = (free_frame, True, dirty)
            return data

    def write_page(self, page_id, data):
        """Записывает данные на страницу"""
        print(f"[DEBUG] write_page: попытка записи на страницу {page_id}")
        print(f"[DEBUG] Текущая page_table: {self.page_table}")

        if page_id not in self.page_table:
            raise KeyError(f"Page {page_id} not allocated")

        frame_idx, in_mem, _ = self.page_table[page_id]
        print(f"[DEBUG] Страница {page_id}: frame={frame_idx}, in_mem={in_mem}")

        if in_mem:
            # Страница в памяти
            print(f"[DEBUG] Запись на страницу {page_id} в памяти")
            self.phys_mem.write_frame(frame_idx, data)
            self.page_table[page_id] = (frame_idx, True, True)
            print(f"[DEBUG] Страница {page_id} помечена как dirty")
        else:
            # Страница не в памяти - пишем в swap
            print(f"[DEBUG] Страница {page_id} не в памяти, пишем в swap")
            self.swap.write_page(page_id, data)
            self.page_table[page_id] = (frame_idx, False, True)

    def free_page(self, page_id):
        """Освобождает страницу"""
        if page_id not in self.page_table:
            return

        frame_idx, in_mem, dirty = self.page_table[page_id]
        print(f"[DEBUG] Освобождение страницы {page_id}")

        if in_mem and dirty:
            data = self.phys_mem.read_frame(frame_idx)
            self.swap.write_page(page_id, data)

        if in_mem:
            # Освобождаем фрейм
            for i in range(self.phys_mem.num_frames):
                if self.frame_to_page[i] == page_id:
                    self.frame_to_page[i] = -1
                    break

        del self.page_table[page_id]