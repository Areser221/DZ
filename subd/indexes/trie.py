class TrieNode:
    def __init__(self):
        self.children = {}
        self.record_id = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key, record_id):
        node = self.root
        for char in str(key):
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.record_id = record_id

    def search(self, key):
        node = self.root
        for char in str(key):
            if char not in node.children:
                return None
            node = node.children[char]
        return node.record_id
