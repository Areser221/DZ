class PhysicalMemory:
    def __init__(self, num_frames, page_size):
        self.num_frames = num_frames
        self.page_size = page_size
        # Сами данные в памяти: {frame_id: bytearray}
        self.frames = {i: bytearray(page_size) for i in range(num_frames)}
        # Свободные фреймы
        self.free_frames = list(range(num_frames))

    def put_page(self, frame_id, data):
        self.frames[frame_id] = bytearray(data).ljust(self.page_size, b'\x00')

    def get_page(self, frame_id):
        return self.frames[frame_id]

    def allocate_frame(self):
        if not self.free_frames:
            return None
        return self.free_frames.pop(0)
