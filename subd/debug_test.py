import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory.virtual import VirtualMemoryManager


def debug_allocate():
    vmm = VirtualMemoryManager(num_pages=10, num_frames=4)

    print("Создаем страницу 0...")
    page_id = vmm.allocate_page()
    print(f"Страница создана: {page_id}")
    print(f"Page table после создания: {vmm.page_table}")
    print(f"frame_to_page: {vmm.frame_to_page}")

    print("\nПытаемся записать данные...")
    data = b"Test data"
    vmm.write_page(page_id, data)
    print("Запись успешна!")


if __name__ == "__main__":
    debug_allocate()