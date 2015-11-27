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
        node = self.search(key)

        # BFS - The shortest match is shown first
        results = []
        if node is not None:
            stack = [node]
            while stack:
                u = stack.pop()
                results.extend(u.data)
                stack.extend(u.children.values())
        return results

    def search(self, key):
        '''Return node with suffix equal to given key.'''
        node = self.root
        if node:
            for char in key:
                if char in node.children:
                    node = node.children[char]
                else:
                    return None
        return node
