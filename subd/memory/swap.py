# memory/swap.py
import pickle
import os

class SwapFile:
    def __init__(self, path="swap.bin"):
        self.path = path
        self.pages = {}  # page_id -> bytes
        if os.path.exists(path):
            self.load()

    def load(self):
        try:
            with open(self.path, "rb") as f:
                self.pages = pickle.load(f)
        except:
            self.pages = {}

    def save(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.pages, f)

    def write_page(self, page_id, data):
        self.pages[page_id] = data
        self.save()

    def read_page(self, page_id):
        return self.pages.get(page_id)

    def delete_page(self, page_id):
        if page_id in self.pages:
            del self.pages[page_id]
            self.save()