from dispatch.trie import Trie


class Searcher:
    def __init__(self, operators):
        self.past_data = {}
        self.operators = operators
        self.cache = {}


    def empty_cache(self):
        self.cache = {}


    def search_operators(self, action, query):
        actions_live = []
        actions_static_trie = []
        if action in self.cache:
            actions_static_trie = self.cache[action]
            for op in self.operators:
                op_operates, op_live = op.operates_on(action)
                if op_operates and op_live:
                    actions_live.extend(op.get_actions_for(action, query))
        else:
            for op in self.operators:
                op_operates, op_live = op.operates_on(action)
                if op_operates and op_live:
                    actions_live.extend(op.get_actions_for(action, query))
                elif op_operates and not op_live:
                    actions_static_trie.extend(op.get_actions_for(action, query))
            actions_static_trie = self._create_trie(actions_static_trie)
            if action is None or action.cacheable:
                self.cache[action] = actions_static_trie
        return [actions_static_trie, actions_live]


    def search(self, query, action):
        query = query.strip().lower()
        if query == "":
            return []
        elif query.startswith("/"):
            query = query[1:]

        static_actions_trie, live_actions = self.search_operators(action, query)

        matches = []
        for match in static_actions_trie.find_matches(query):
            matches.append(match)

        if len(matches) <= 10:
            matches = self.order_by_usage(matches)

        return matches + live_actions


    def order_by_usage(self, matches):
        return sorted(matches, key=lambda z: -1*self.past_data.get(z.name, 0))


    def heuristic_data(self, query, action):
        self.past_data[action.name] = self.past_data.get(action.name, 0) + 1


    def _create_trie(self, actions):
        T = Trie()
        if actions:  # individual words allow same lookup of object
            for e in actions:
                T.insert(e.name.lower(), e)
                for word in e.name.split()[1:]:
                    T.insert(word.lower(), e)
        return T
