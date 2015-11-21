from dispatch.trie import Trie


class Searcher:
    def __init__(self, sources):
        self.sources = sources
        self.past_data = {}
        self.source_data = self.get_data(sources)

    def search(self, query, chain):
        return self.experminental_search(query, chain)
        if query.strip() == "":
            return []
        matches = []
        for (s, st) in self.source_data.items():
            matches.extend(st.find_matches(query.lower()))
        self.rank(query, matches)
        return matches



        # What happens when backspaces we must go out of context


    def experminental_search(self, query, chain):
        # chain = action chain = choices that led to this point
        if query == "":
            return []

        if chain == []:
            search_context = self.source_data
        else:
            search_context =  {}
            if chain[-1] is None or chain[-1].option_callback is None:
                possible_actions = []
            else:
                possible_actions = chain[-1].option_callback(chain[-1])
            search_context[chain[-1]] = self._create_trie(possible_actions)

        # finds matches of each word in  query, and takes intersection of
        # those matches to find matches with all word parts

        query = query.strip().lower()
        if "/" in query:
            query = query[query.index("/")+1:]

        if query == "":
            matches = set()
            for search_tree in search_context.values():
                for match in search_tree.find_matches(query):
                    matches.add(match)
            matches = list(matches)
            return matches
        else:
            search_words = query.split()
            match_sets = []
            for word in search_words:
                matches = set()
                for search_tree in search_context.values():
                    matches = matches.union(set(search_tree.find_matches(word)))
                match_sets.append(matches)

            if match_sets:
                intersection = list(set.intersection(*match_sets))
            else:
                intersection = []
            self.rank(query, intersection)
            return intersection 


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
                words = e.name.split()
                for index in range(len(words)):
                    insert = " ".join(words[index:])
                    T.insert(insert.lower(), e)
        return T

    def get_data(self, sources):
        source_data_map = {}
        for src in self.sources:
            source_data_map[src] = self._create_trie(src.get_actions())
        return source_data_map

    def update_sources(self):
        for src in self.sources:
            if src.has_updates():
                self.source_data_map[src] = self._create_trie(src.get_actions())
        return True 
   