from dispatch.ui.mainwindow import MainWindow
from gi.repository import Gtk
from dispatch.controller import Controller
import os


def main():
    controller = Controller()
    os.chdir(os.path.expanduser("~"))
    window = MainWindow(controller)
    window.show_all()
    Gtk.main()
