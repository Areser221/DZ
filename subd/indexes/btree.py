class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.values = [] # RecordIDs
        self.children = []

class BTree:
    def __init__(self, t=3):
        self.root = BTreeNode(True)
        self.t = t

    def search(self, k, node=None):
        if node is None: node = self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return node.values[i]
        elif node.leaf:
            return None
        else:
            return self.search(k, node.children[i])

    def insert(self, k, rid):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode()
            self.root = new_root
            new_root.children.insert(0, root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, k, rid)
        else:
            self._insert_non_full(root, k, rid)

    def _split_child(self, parent, i):
        t = self.t
        node = parent.children[i]
        new_node = BTreeNode(leaf=node.leaf)
        parent.keys.insert(i, node.keys[t-1])
        parent.children.insert(i + 1, new_node)
        new_node.keys = node.keys[t:]
        new_node.values = node.values[t:]
        node.keys = node.keys[:t-1]
        node.values = node.values[:t-1]
        if not node.leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]

    def _insert_non_full(self, node, k, rid):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and k < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                node.values[i+1] = node.values[i]
                i -= 1
            node.keys[i+1] = k
            node.values[i+1] = rid
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k, rid)
