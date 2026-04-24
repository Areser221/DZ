import os

class SwapManager:
    def __init__(self, filename="swap.bin", page_size=4096):
        self.filename = filename
        self.page_size = page_size
        # Просто очищаем файл при старте
        open(self.filename, 'wb').close()

    def write_page(self, v_page_id, data):
        with open(self.filename, 'r+b') if os.path.exists(self.filename) else open(self.filename, 'wb') as f:
            f.seek(v_page_id * self.page_size)
            f.write(data)

    def read_page(self, v_page_id):
        if not os.path.exists(self.filename): return None
        with open(self.filename, 'rb') as f:
            f.seek(v_page_id * self.page_size)
            return f.read(self.page_size)
