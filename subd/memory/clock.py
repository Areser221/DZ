class ClockEviction:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.hand = 0
        self.use_bits = [0] * num_frames
        self.frame_to_vpage = {} # Чтобы знать, какую виртуальную страницу выселяем

    def mark_used(self, frame_id):
        self.use_bits[frame_id] = 1

    def find_victim(self):
        while True:
            if self.use_bits[self.hand] == 0:
                victim_frame = self.hand
                self.hand = (self.hand + 1) % self.num_frames
                return victim_frame
            else:
                self.use_bits[self.hand] = 0
                self.hand = (self.hand + 1) % self.num_frames
