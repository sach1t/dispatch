from dispatch.search import Searcher
from dispatch.ui.mainwindow import MainWindow
from gi.repository import Gtk, GObject
from dispatch.plugin_manager import PluginManager
import os 
def read_css(filename):
    with open(filename) as f:
        data = f.read()
    return data


def main():
    plugin_manager = PluginManager()
    plugin_manager.load_plugins()
    plugins = plugin_manager.get_plugins()
    print("Loaded Plugins : ", plugins)
    searcher = Searcher(plugins)
    style = read_css("./dispatch/ui/style.css")
    os.chdir(os.path.expanduser("~"))
    win = MainWindow(searcher, style)
    win.show_all()
    Gtk.main()
