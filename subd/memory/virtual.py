from .physical import PhysicalMemory
from .clock import ClockEviction
from .swap import SwapManager


class VirtualMemory:
    def __init__(self, num_frames=4, page_size=1024):
        self.page_size = page_size
        self.phys_mem = PhysicalMemory(num_frames, page_size)
        self.clock = ClockEviction(num_frames)
        self.swap = SwapManager(page_size=page_size)

        self.page_table = {}  # v_id -> {frame_id, present, dirty}
        self.v_page_counter = 0

    def get_page(self, v_id):
        entry = self.page_table[v_id]
        if entry['present']:
            self.clock.mark_used(entry['frame_id'])
            return self.phys_mem.get_page(entry['frame_id'])

        # Page Fault!
        return self._handle_page_fault(v_id)

    def _handle_page_fault(self, v_id):
        frame_id = self.phys_mem.allocate_frame()

        if frame_id is None:  # Память полна, нужен eviction
            victim_frame = self.clock.find_victim()
            victim_v_id = self.clock.frame_to_vpage[victim_frame]

            # Сохраняем жертву в своп
            data_to_swap = self.phys_mem.get_page(victim_frame)
            self.swap.write_page(victim_v_id, data_to_swap)

            self.page_table[victim_v_id]['present'] = False
            frame_id = victim_frame

        # Загружаем из свопа
        data = self.swap.read_page(v_id)
        if data:
            self.phys_mem.put_page(frame_id, data)

        self.page_table[v_id].update({'frame_id': frame_id, 'present': True})
        self.clock.frame_to_vpage[frame_id] = v_id
        self.clock.mark_used(frame_id)
        return self.phys_mem.get_page(frame_id)

    def allocate_v_page(self):
        v_id = self.v_page_counter
        self.page_table[v_id] = {'frame_id': None, 'present': False, 'dirty': False}
        self.v_page_counter += 1
        return v_id
