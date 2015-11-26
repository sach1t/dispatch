from dispatch.search import Searcher
from dispatch.ui.mainwindow import MainWindow
from gi.repository import Gtk
from dispatch.plugin_manager import PluginManager
import os


def main():
    plugin_manager = PluginManager()
    plugin_manager.load_plugins()
    plugins = plugin_manager.get_plugins()
    print("Loaded Plugins : ", plugins)
    searcher = Searcher(plugins)
    os.chdir(os.path.expanduser("~"))
    win = MainWindow(searcher)
    win.show_all()
    Gtk.main()
