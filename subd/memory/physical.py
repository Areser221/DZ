from .clock import ClockEviction

class PhysicalMemory:
    PAGE_SIZE = 4096

    def __init__(self, num_frames=64):
        self.num_frames = num_frames
        self.memory = [bytearray(self.PAGE_SIZE) for _ in range(num_frames)]
        self.clock = ClockEviction(num_frames)
        self.frame_to_page = [-1] * num_frames  # Изменил None на -1

    def read_frame(self, frame_idx):
        """Читает данные из фрейма"""
        if frame_idx < 0 or frame_idx >= self.num_frames:
            raise IndexError(f"Invalid frame index: {frame_idx}")
        return bytes(self.memory[frame_idx])

    def write_frame(self, frame_idx, data):
        """Записывает данные во фрейм"""
        if frame_idx < 0 or frame_idx >= self.num_frames:
            raise IndexError(f"Invalid frame index: {frame_idx}")
        if len(data) > self.PAGE_SIZE:
            raise ValueError(f"Data too large: {len(data)} > {self.PAGE_SIZE}")

        # Очищаем фрейм
        self.memory[frame_idx] = bytearray(self.PAGE_SIZE)
        # Записываем данные
        self.memory[frame_idx][:len(data)] = data

    def get_frame_for_page(self, page_id):
        """Возвращает frame_idx, если страница в памяти, иначе None"""
        for idx, pid in enumerate(self.frame_to_page):
            if pid == page_id:
                self.clock.access(idx)
                return idx
        return None