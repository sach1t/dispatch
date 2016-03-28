class Controller:
    '''Interface by which the ui interacts with system'''

    def __init__(self, plugin_manager, searcher):
        self.plugin_manager = plugin_manager
        self.searcher = searcher

    def run_action(self, action):
        if action.run is not None:
            action.run(action)
            return True
        return False

    def add_heuristic_data(self, query, action):
        self.searcher.heuristic_data(query, action)

    def reload_plugins(self):
        for plug in self.plugin_manager.get_operators():
            plug.reload()
        self.searcher.empty_cache()

    def search(self, query, action=None):
        return self.searcher.search(
            self.plugin_manager.get_operators(),
            query,
            action
        )
