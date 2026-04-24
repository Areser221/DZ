import bisect


class BPlusNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.values = []  # Для листов: [RecordID], для узлов: [BPlusNode]
        self.next = None  # Ссылка на следующий лист (для Range Scan)


class BPlusTree:
    def __init__(self, t=3):
        self.root = BPlusNode(leaf=True)
        self.t = t  # Степень дерева

    def insert(self, key, record_id):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BPlusNode()
            self.root = new_root
            new_root.values.insert(0, root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key, record_id)
        else:
            self._insert_non_full(root, key, record_id)

    def _split_child(self, parent, i):
        t = self.t
        node = parent.values[i]
        new_node = BPlusNode(leaf=node.leaf)
        parent.keys.insert(i, node.keys[t - 1])
        parent.values.insert(i + 1, new_node)

        new_node.keys = node.keys[t:]
        new_node.values = node.values[t:]
        node.keys = node.keys[:t - 1]
        node.values = node.values[:t - 1]

        if node.leaf:
            # Связываем листы в список
            new_node.next = node.next
            node.next = new_node
            # В B+ дереве ключ также остается в листе справа
            new_node.keys.insert(0, parent.keys[i])

    def _insert_non_full(self, node, key, record_id):
        if node.leaf:
            idx = bisect.bisect_left(node.keys, key)
            node.keys.insert(idx, key)
            node.values.insert(idx, record_id)
        else:
            idx = bisect.bisect_right(node.keys, key)
            if len(node.values[idx].keys) == (2 * self.t) - 1:
                self._split_child(node, idx)
                if key > node.keys[idx]:
                    idx += 1
            self._insert_non_full(node.values[idx], key, record_id)

    def search(self, key):
        """Точечный поиск (Запрос 6.1)"""
        node = self.root

        # 1. Если дерево пустое — сразу выходим
        if not node.keys:
            return None

        # 2. Спускаемся по внутренним узлам до листа
        while not node.leaf:
            idx = bisect.bisect_right(node.keys, key)
            # Гарантируем, что индекс не выйдет за пределы дочерних узлов
            safe_idx = min(idx, len(node.values) - 1)
            node = node.values[safe_idx]

        # 3. Ищем ключ в листе
        idx = bisect.bisect_left(node.keys, key)

        # ПРОВЕРКА: индекс должен быть внутри массива и ключ должен совпадать
        if idx < len(node.keys) and idx < len(node.values) and node.keys[idx] == key:
            return node.values[idx]

        return None

    def search_range(self, low, high):
        """Поиск по диапазону (Запрос 6.2)"""
        node = self.root
        while not node.leaf:
            idx = bisect.bisect_right(node.keys, low)
            node = node.values[idx]

        results = []
        while node:
            for i, key in enumerate(node.keys):
                if low <= key <= high:
                    results.append(node.values[i])
                if key > high:
                    return results
            node = node.next
        return results
