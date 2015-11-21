class TrieNode:
    def __init__(self, suffix, parent):
        self.suffix = suffix
        self.children = {}
        self.parent = parent
        self.data = []

    def __str__(self):
        return self.suffix

    def __repr__(self):
        return self.suffix


class Trie:
    def __init__(self):
        self.root = TrieNode("", None)
        self.last_search = self.root

    def insert(self, key, data):
        node = self.root
        for char in key:
            if char in node.children:
                node = node.children[char]
            else:
                node.children[char] = TrieNode(node.suffix + char, node)
                node = node.children[char]
        node.data.append(data)

    def find_matches(self, key, restart=True):
        if restart:
            node = self.search(key)
            self.last_search = node
        else:
            node = self.last_search

        # bfs -  thus closest match should be shown first in each tree 
        results = []
        if node is not None:
            stack = [node]
            while stack:
                u = stack.pop()
                results.extend(u.data)
                stack.extend(u.children.values())

        return results

    def search(self, key):
        node = self.root
        for char in key:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node
