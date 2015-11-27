from dispatch.search import Searcher
from dispatch.plugin_manager import PluginManager

class Controller:
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_operators()
        plugins = self.plugin_manager.get_operators()
        self.searcher = Searcher(plugins)

    def run_action(self, action):
        if action.run is not None:
            action.run(action)
            return True
        return False

    def add_heuristic_data(self, query, action):
        self.searcher.heuristic_data(query, action)
    
    def reload_plugins(self):
        for plug in self.plugin_manager.get_plugins():
            plug.reload()
        self.searcher.empty_cache()

    def search(self, query, action=None):
        return self.searcher.search(query, action)