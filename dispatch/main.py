from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk
from dispatch.ui.mainwindow import MainWindow
from dispatch.controller import Controller
from dispatch.search import Searcher
from dispatch.plugin_manager import PluginManager
import os


def main():
    searcher = Searcher()
    print("Loading plugins")
    plugin_manager = PluginManager()
    print("Finished loading plugins")
    controller = Controller(plugin_manager, searcher)
    os.chdir(os.path.expanduser("~"))
    window = MainWindow(controller)
    window.show_all()
    Gtk.main()
