class TrieNode:
    def __init__(self, suffix, parent):
        '''Create node for Trie with given suffix and parent.'''
        self.suffix = suffix
        self.parent = parent
        self.children = {}
        self.data = []

    def __str__(self):
        return self.suffix


class Trie:
    def __init__(self):
        '''Create empty Trie.'''
        self.root = TrieNode("", None)
        self.last_query = ("", self.root)

    def insert(self, key, data):
        '''Insert key with corresponding data.'''
        node = self.root
        for char in key:
            if char in node.children:
                node = node.children[char]
            else:
                node.children[char] = TrieNode(node.suffix + char, node)
                node = node.children[char]
        node.data.append(data)

    def find_matches(self, key):
        '''Return data of all nodes with suffix equal to key'''

        if key.startswith(self.last_query[0]):
            start = self.last_query[1]
            key = key.replace(self.last_query[0], "", 1)
        else:
            start = self.root

        node = self.search(key, start)
        self.last_query=(key, node)

        # BFS - The shortest match is shown first
        results = []
        if node is not None:
            stack = [node]
            while stack:
                u = stack.pop()
                results.extend(u.data)
                stack.extend(u.children.values())
        return results

    def search(self, key, start):
        '''Return node with suffix equal to given key.'''
        node = start
        if node:
            for char in key:
                if char in node.children:
                    node = node.children[char]
                else:
                    return None
        return node
