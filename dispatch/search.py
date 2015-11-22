from dispatch.trie import Trie


class Searcher:
    def __init__(self, operators):
        self.past_data = {}
        self.operators = operators
        self.cache = {}

    def basic_search(self, query, chain):
        if query.strip() == "":
            return []
        matches = []
        for (s, st) in self.source_data.items():
            matches.extend(st.find_matches(query.lower()))
        self.rank(query, matches)
        return matches


    def search_plugins(self, action, query):
        print("acts = ", action)
        print("query = ", query)

        actions_live = []
        actions_static = []
        if action in self.cache:
            print("chache hit")
            actions_static = self.cache[action]
            for op in self.operators:
                op_operates,op_live = op.operates_on(action)
                if op_operates and op_live:
                    print("queried lve")
                    actions_live.extend(op.get_actions_for(action, query))
        else:
            print("cacche miss")
            for op in self.operators:
                op_operates,op_live = op.operates_on(action)
                if op_operates and op_live:
                    actions_live.extend(op.get_actions_for(action, query))
                elif op_operates and not op_live:
                    actions_static.extend(op.get_actions_for(action, query))
            self.cache[action] = actions_static

        print("static = ", actions_static)
        print("live = ", actions_live)
        print("\n\n\n\n\n")

        return actions_static, actions_live


    def search(self, query, chain):
        # chain =  operator chain
        #print("-----")
        #print("chain = ", chain)
        if query == "":
            return []

        query = query.strip().lower()
        if "/" in query:
            query = query[query.index("/")+1:]
            
        last_action = chain[-1] if len(chain) > 0 else None
        actions, live_actions = self.search_plugins(last_action, query)

        search_tree = self._create_trie(actions)

        # finds matches of each word in  query, and takes intersection of
        # those matches to find matches with all word parts
        matches = []
        for match in search_tree.find_matches(query):
            matches.append(match)
        return matches + live_actions
   

    def rank(self, query, matches):
        if query in self.past_data:
            for i in range(len(matches)):
                if matches[i].name == self.past_data[query]:
                    break
            found = matches.pop(i)
            matches.insert(0, found)

    def heuristic_data(self, query, action):
        self.past_data[query] = action.name

    def _create_trie(self, actions):
        T = Trie()
        if actions:# individual words allow same lookup of object
            for e in actions:
                T.insert(e.name.lower(), e)
        return T

