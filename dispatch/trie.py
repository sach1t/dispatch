class _TrieNode:
    def __init__(self, prefix, parent):
        self.prefix = prefix
        self.parent = parent
        self.children = {}
        self.data = []

    def __str__(self):
        return self.prefix


class Trie:
    def __init__(self):
        self._root = _TrieNode("", None)

    def insert(self, prefix, data):
        ''' Insert prefix with attached data'''
        node = self._root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                node.children[char] = _TrieNode(node.prefix + char, node)
                node = node.children[char]
        node.data.append(data)

    def find_matches(self, prefix):
        '''Find matches for the given prefix'''
        node = self._find_prefix_node(prefix)
        results = []
        if node is not None:
            stack = [node]
            while stack:
                u = stack.pop()
                results.extend(u.data)
                stack.extend(u.children.values())
        return results

    def _find_prefix_node(self, prefix):
        '''Find the node whose prefix is equal to the given prefix'''
        node = self._root
        if node:
            for char in prefix:
                if char in node.children:
                    node = node.children[char]
                else:
                    return None
        return node
