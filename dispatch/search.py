from dispatch.trie import Trie
from dispatch.ordered_set import OrderedSet


class Searcher:
    '''Searches actions from operators'''

    RESULT_LIMIT = 25  # for speed
    WORD_SPLIT_LIMIT = 100

    def __init__(self):
        self.past_data = {}
        self.cache = {}

    def empty_cache(self):
        self.cache = {}

    def _search_operators(self, operators, action, query):
        actions_live = []
        actions_static_trie = []
        if action in self.cache:
            actions_static_trie = self.cache[action]
            for op in operators:
                op_operates, op_live = op.operates_on(action)
                if op_operates and op_live:
                    actions_live.extend(op.get_actions_for(action, query))
        else:
            for op in operators:
                op_operates, op_live = op.operates_on(action)
                if op_operates and op_live:
                    actions_live.extend(op.get_actions_for(action, query))
                elif op_operates and not op_live:
                    actions_static_trie.extend(
                        op.get_actions_for(action, query)
                    )
            actions_static_trie = self._create_trie(actions_static_trie)
            if action is None or action.cacheable:
                self.cache[action] = actions_static_trie
        return [actions_static_trie, actions_live]

    def search(self, operators, query, action):
        query = query.strip().lower()
        if query == "":
            return []
        elif query.startswith("/"):
            query = query[1:]

        static_actions_trie, live_actions = \
            self._search_operators(operators, action, query)

        matches = OrderedSet()
        for match in static_actions_trie.find_matches(query):
            matches.add(match)

        matches = list(matches)
        matches = self._order_by_usage(matches)
        matches = matches[:Searcher.RESULT_LIMIT]

        return matches + live_actions

    def _order_by_usage(self, matches):
        return sorted(matches, key=lambda z: -1*self.past_data.get(z.name, 0))

    def heuristic_data(self, query, action):
        self.past_data[action.name] = self.past_data.get(action.name, 0) + 1

    def _get_suffixes(self, x):
        suffixes = [x]
        end = len(x) - 1
        while end >= 0:
            if x[end] == " ":
                suffixes.append(x[end+1:])
            end -= 1
        return suffixes

    def _create_trie(self, actions):
        T = Trie()
        if actions:  # individual words allow same lookup of object
            for e in actions:
                if len(e.name) < Searcher.WORD_SPLIT_LIMIT:
                    for word in self._get_suffixes(e.name):
                        T.insert(word.lower(), e)
                else:
                    T.insert(e.name.lower(), e)
        return T
