from collections import OrderedDict

class ClockEviction:
    """Алгоритм Clock (Second Chance) для вытеснения страниц."""
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = [None] * num_frames  # виртуальные page_id в фреймах
        self.reference_bits = [0] * num_frames
        self.hand = 0

    def access(self, frame_idx):
        """Отметить обращение к фрейму."""
        if frame_idx is not None:
            self.reference_bits[frame_idx] = 1

    def evict(self):
        """Выбрать фрейм для вытеснения."""
        while True:
            if self.reference_bits[self.hand] == 0:
                victim = self.hand
                self.hand = (self.hand + 1) % self.num_frames
                return victim
            else:
                self.reference_bits[self.hand] = 0
                self.hand = (self.hand + 1) % self.num_frames

    def set_frame(self, frame_idx, page_id):
        self.frames[frame_idx] = page_id

    def get_page_in_frame(self, frame_idx):
        return self.frames[frame_idx]