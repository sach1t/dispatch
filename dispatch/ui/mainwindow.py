import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject
from keybinder.keybinder_gtk import KeybinderGtk


class MainWindow(Gtk.Window):
    def __init__(self, searcher, style):
        Gtk.Window.__init__(self, title="Dispatch")
        self.searcher = searcher

        self._set_window_properties()
        self._create_layout()
        self._register_key_bindings()
        self._set_style(style)
        self._register_gtk_callbacks()
        self.non_character_keypress = False
        self.chain = []
        self.non_delete_update = False

    def _set_window_properties(self):
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_resizable(True)
        self.set_default_geometry(
            self.get_screen().get_width()*.20,
            self.get_screen().get_height()
        )
        self.move(0, 0)
        self.set_opacity(.95)
        self.set_name("MainWindow")

        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual is not None and self.screen.is_composited():
            self.set_visual(self.visual)

    def _create_layout(self):
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
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.listbox)
        self.main_box.pack_start(scrolled, True, True, 0)


        self.main_box.set_focus_chain([self.entry])



    def _register_key_bindings(self):
        self.keybinder = KeybinderGtk()
        key = "<Ctrl>space"
        self.keybinder.register(key, self.toggle_visibility)
        self.keybinder.start()

    def _set_style(self, css):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css.encode())
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

        self.entry.connect("key-press-event", self._on_search_key) #key pressed 
        self.entry.connect("changed", self._on_search_changed) # before entry changes
        #self.entry.connect("key-release-event", self._on_search_key_release) #key pressed 

        self.entry.connect("activate", self._on_search_submit)
        #self.entry.connect("insert-text", self._on_insert)
        self.entry.connect("delete-text", self._on_delete)

        self.listbox.connect("row-activated", self._run_action)


    def _listbox_row_delta(self, listbox, delta):
        picked_row_index = listbox.get_selected_row().get_index()
        next_row_index = picked_row_index + delta
        if next_row_index >= len(listbox.get_children()):
            next_row_index = 0
        elif next_row_index < 0:
            next_row_index = len(listbox.get_children()) - 1
        return next_row_index


    def _on_delete(self, widget, start, end):
        print("text = ", self.entry.get_text())
        print("del = ", self.entry.get_text()[start:end])
        print("=", self.entry.get_text())
        if self.non_delete_update:
            self.non_delete_update = False
        else:
            deleted_contexts = self.entry.get_text()[start:end].count('/')
            for x in range(deleted_contexts):
                self.chain.pop()
        print("chain (del) = ", self.chain)


    def _on_search_key(self, widget, event):
        if event.keyval == Gdk.KEY_slash:    
            self.non_character_keypress = False       
            current_row = self.listbox.get_selected_row()
            if current_row:
                new_text = current_row.action.name
                entry_text = self.entry.get_text()
                if "/" in entry_text:
                    new_text = entry_text[:entry_text.rindex('/')+1] + new_text
                self.entry.set_text(new_text)
                self.chain.append(current_row.action)
            else:
                self.chain.append(None)
            self.entry.set_position(len(self.entry.get_text()))
            print("chain (sla) = ", self.chain)


        elif event.keyval == Gdk.KEY_Tab and len(self.listbox.get_children()) > 0:
            self.non_character_keypress = True
            self.non_delete_update = True
            current_row = self.listbox.get_selected_row()
            entry_text = self.entry.get_text()
            start_of_current = 0
            if "/" in entry_text:
                start_of_current = entry_text.rindex('/')+1
            current_text = entry_text[start_of_current:]

            if current_row.action.name != current_text:
                self.entry.set_text(entry_text[:start_of_current]+current_row.action.name)
            else:
                next_row_index = self._listbox_row_delta(self.listbox, +1)
                next_row = self.listbox.get_row_at_index(next_row_index)
                if next_row and hasattr(next_row, "action"):
                    self.listbox.select_row(next_row)
                    new_text = next_row.action.name
                    entry_text = self.entry.get_text()
                    if "/" in entry_text:
                        new_text = entry_text[:entry_text.rindex('/')+1] + new_text
                    self.entry.set_text(new_text)
                    self.entry.grab_focus() #want sideeffect of selecting all text

        elif event.keyval == Gdk.KEY_Down and len(self.listbox.get_children()) > 0:
            self.non_character_keypress = True
            self.non_delete_update = True
            next_row_index = self._listbox_row_delta(self.listbox, +1)
            next_row = self.listbox.get_row_at_index(next_row_index)
            if next_row and hasattr(next_row, "action"):
                self.listbox.select_row(next_row)
                new_text = next_row.action.name
                entry_text = self.entry.get_text()
                if "/" in entry_text:
                    new_text = entry_text[:entry_text.rindex('/')+1] + new_text
                self.entry.set_text(new_text)
                self.entry.grab_focus()


        elif event.keyval == Gdk.KEY_Up and len(self.listbox.get_children()) > 0:
            self.non_character_keypress = True
            self.non_delete_update = True
            next_row_index = self._listbox_row_delta(self.listbox, -1)
            next_row = self.listbox.get_row_at_index(next_row_index)
            if next_row and hasattr(next_row, "action"):
                self.listbox.select_row(next_row)
                new_text = next_row.action.name
                entry_text = self.entry.get_text()
                if "/" in entry_text:
                    new_text = entry_text[:entry_text.rindex('/')+1] + new_text
                self.entry.set_text(new_text)
                self.entry.grab_focus()


    def _on_search_changed(self, widget):
        if self.non_character_keypress:
            self.non_character_keypress = False
        else:
            text = widget.get_text()
            for child in self.listbox.get_children():
                child.destroy() # this could be more efficient instead of always flushing out the old results
            matches = self.searcher.search(text, self.chain)
            self._show_matches(matches)


    def _on_search_submit(self, widget):
        row = self.listbox.get_selected_row()
        if row:
            self._run_action(self.listbox, row)



    def _on_quit(self,  *args):
        self.keybinder.stop()

    def _on_lost_focus(self, widget, event):
        self.hide()

    def _on_key_release(self,  widget, event, data=None):
        if event.keyval == Gdk.KEY_Escape:
            self.toggle_visibility()

    def _show(self):
        self.move(0, 0)
        self.show()
        self.entry.grab_focus()
        return False

    def toggle_visibility(self):
        if self.is_visible():
            self.hide()
        else:
            GObject.idle_add(self._show)

    def _show_matches(self, matches):
        for match in matches:
            row = self.create_row(match)
            self.listbox.add(row)
            row.show_all()
        if matches:
            self.listbox.select_row(self.listbox.get_row_at_index(0))

    def create_row(self, action):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label = Gtk.Label(action.name, xalign=0)
        hbox.pack_start(label, True, True, 0)
        row.add(hbox)
        row.action = action
        return row


    def _run_action(self, listbox, listrow):
        if hasattr(listrow, "action"):
            listrow.action.exec_callback(listrow.action)
            # we dont execute through another function bc we want it to be as fast as possible
            # even though another function call is cheap, pennies count
            self.searcher.heuristic_data(self.entry.get_text(), listrow.action)
            self.toggle_visibility()
