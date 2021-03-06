from gi.repository import Gtk, Gdk, GObject, Keybinder
import os
# import time


class MainWindow(Gtk.Window):
    DEFAULT_CSS = os.path.join(os.path.dirname(__file__), "style.css")
    TRIGGER = "<Ctrl>space"
    ICONS = True

    def __init__(self, controller):
        Gtk.Window.__init__(self, title="Dispatch")

        self._set_window_properties()
        self._create_layout()
        self._set_style()
        self._register_gtk_callbacks()
        self._register_key_bindings()

        self.controller = controller
        self.non_character_keypress = False
        self.chain = []
        self.non_delete_update = False
        # window incorrectly reports non visible when visible but not in focus
        self.visible = self.is_visible() 

    def _set_window_properties(self):
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_resizable(True)
        self.set_default_geometry(
            self.get_screen().get_width()*.20,
            self.get_screen().get_height()
        )
        self.resize(
            self.get_screen().get_width()*.20,
            self.get_screen().get_height()
        )
        self.move(0, 0)
        self.set_opacity(1)
        self.set_name("MainWindow")

        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual is not None and self.screen.is_composited():
            self.set_visual(self.visual)

    def _create_layout(self):
        # container for search box and results
        self.main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=5
        )
        self.add(self.main_box)

        # search  box
        self.entry = Gtk.Entry()
        self.entry.set_has_frame(False)
        self.entry.set_name("SearchEntry")
        self.main_box.pack_start(self.entry, False, False, 0)

        # results box
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.listbox)
        self.main_box.pack_start(scrolled, True, True, 0)

        self.main_box.set_focus_chain([self.entry])

    def read_css(self, path):
        with open(os.path.expanduser(path)) as f:
            data = f.read()
        return data.encode()

    def _set_style(self):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(self.read_css(MainWindow.DEFAULT_CSS))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _register_gtk_callbacks(self):
        self.connect("delete-event", Gtk.main_quit)
        self.connect('destroy', self._on_quit)
        self.connect("focus-out-event", self._on_lost_focus)
        self.connect("key-release-event", self._on_key_release)

        self.entry.connect("key-press-event", self._on_search_key)  # key press
        self.entry.connect("changed", self._on_search_changed)  # before change
        self.entry.connect("activate", self._on_search_submit)
        self.entry.connect("delete-text", self._on_delete)

        self.listbox.connect("row-activated", self._run_action)

    def _register_key_bindings(self):
        Keybinder.init()
        Keybinder.bind(MainWindow.TRIGGER, self.toggle_visibility)

    def _listbox_row_delta(self, listbox, delta):
        picked_row_index = listbox.get_selected_row().get_index()
        next_row_index = picked_row_index + delta
        if next_row_index >= len(listbox.get_children()):
            next_row_index = 0
        elif next_row_index < 0:
            next_row_index = len(listbox.get_children()) - 1
        return next_row_index

    def _on_delete(self, widget, start, end):
        if self.non_delete_update:
            self.non_delete_update = False
        else:
            total_contexts = self.entry.get_text().count("/")
            del_contexts = self.entry.get_text()[start:end].count("/")
            self.chain = self.chain[:total_contexts-del_contexts]

    def _on_search_key(self, widget, event):
        if event.keyval == Gdk.KEY_slash:
            self._slash_key()
        elif len(self.listbox.get_children()) > 0:
            if event.keyval == Gdk.KEY_Tab:
                self._tab_key()
            elif event.keyval == Gdk.KEY_Down:
                self._arrow_key(+1)
            elif event.keyval == Gdk.KEY_Up:
                self._arrow_key(-1)

    def _slash_key(self):
        self.non_character_keypress = False
        current_row = self.listbox.get_selected_row()
        if current_row:
            new_text = current_row.action.name
            if len(new_text) > 20:
                new_text = new_text[:20] + "..."
            entry_text = self.entry.get_text()
            if "/" in entry_text:
                new_text = entry_text[:entry_text.rindex('/')+1] + new_text
            self.entry.set_text(new_text)
            self.chain.append(current_row.action)
            self.controller.add_heuristic_data(
                self._get_query(self.entry.get_text()),
                current_row.action
            )
        self.entry.set_position(len(self.entry.get_text()))

    def _tab_key(self):
        self.non_character_keypress = True
        self.non_delete_update = True
        current_row = self.listbox.get_selected_row()
        entry_text = self.entry.get_text()
        start_of_current = 0
        if "/" in entry_text:
            start_of_current = entry_text.rindex('/')+1
        current_text = entry_text[start_of_current:]
        if current_row.action.name != current_text:
            new_text = current_row.action.name
            if len(new_text) > 20:
                new_text = new_text[:20] + "..."
            self.entry.set_text(entry_text[:start_of_current]+new_text)
        else:
            next_row_index = self._listbox_row_delta(self.listbox, +1)
            next_row = self.listbox.get_row_at_index(next_row_index)
            if next_row and hasattr(next_row, "action"):
                self.listbox.select_row(next_row)
                new_text = next_row.action.name
                if len(new_text) > 20:
                    new_text = new_text[:20] + "..."
                entry_text = self.entry.get_text()
                if "/" in entry_text:
                    new_text = entry_text[:entry_text.rindex('/')+1] + new_text
                self.entry.set_text(new_text)
                self.entry.grab_focus()

    def _arrow_key(self, delta):
        self.non_character_keypress = True
        self.non_delete_update = True
        next_row_index = self._listbox_row_delta(self.listbox, delta)
        next_row = self.listbox.get_row_at_index(next_row_index)
        if next_row and hasattr(next_row, "action"):
            self.listbox.select_row(next_row)
            new_text = next_row.action.name
            if len(new_text) > 20:
                new_text = new_text[:20] + "..."
            entry_text = self.entry.get_text()
            if "/" in entry_text:
                new_text = entry_text[:entry_text.rindex('/')+1] + new_text
            self.entry.set_text(new_text)
            self.entry.grab_focus()

    def _get_query(self, full_query):
        if "/" in full_query:
            full_query = full_query[full_query.rindex("/"):]
        return full_query

    def _on_search_changed(self, widget):
        if self.non_character_keypress:
            self.non_character_keypress = False
        else:
            text = widget.get_text()
            # start = time.time()
            matches = self.controller.search(self._get_query(text), self.chain[-1] if len(self.chain) > 0 else None)
            # end = time.time()
            # print("SEARCH: ", end-start)
            self._show_matches(matches)

    def _on_search_submit(self, widget):
        row = self.listbox.get_selected_row()
        if row:
            self._run_action(self.listbox, row)

        self.entry.grab_focus()

    def _on_quit(self,  *args):
        pass

    def _on_lost_focus(self, widget, event):
        self.hide()

    def _on_key_release(self,  widget, event, data=None):
        if event.keyval == Gdk.KEY_Escape:
            self.toggle_visibility()
        elif event.keyval == Gdk.KEY_F6:
            self.entry.set_text("")
            for child in self.listbox.get_children():
                child.destroy()
            self.non_character_keypress = False
            self.non_delete_update = False
            self.chain = []
            self.controller.reload_plugins()

    def _show(self):
        self.move(0, 0)
        self.show()
        self.entry.grab_focus()
        return False

    def toggle_visibility(self, keystr=None, data=None):
        if self.visible:
            self.hide()
        else:
            self._show()
        self.visible = not self.visible

    def _show_matches(self, matches):
        # start=time.time()
        for child in self.listbox.get_children():
            child.destroy()
        # end=time.time()
        # print("DESTROY: ", end-start)
        # start=time.time()
        for match in matches:
            row = self.create_row(match)
            self.listbox.add(row)
        self.listbox.show_all()
        # end=time.time()
        # print("NEW ROWS: ", end-start)
        self.listbox.select_row(self.listbox.get_row_at_index(0))

    def create_row(self, action):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        name_label = Gtk.Label(action.name, xalign=0)
        description_label = Gtk.Label(action.description, xalign=0)
        vbox.pack_start(name_label, True, True, 0)
        vbox.pack_start(description_label, True, True, 0)

        if MainWindow.ICONS:
            if action.icon:
                hbox.pack_start(action.icon, False, True, 0)
                hbox.pack_start(vbox, True, True, 0)
            else:
                hbox.pack_start(vbox, True, True, 26)
        else:
            hbox.pack_start(vbox, True, True, 0)

        row.add(hbox)
        row.action = action
        return row

    def _run_action(self, listbox, listrow):
        can_run = self.controller.run_action(listrow.action)
        self.controller.add_heuristic_data(
            self._get_query(self.entry.get_text()),
            listrow.action
        )
        if can_run:
            self.toggle_visibility()
