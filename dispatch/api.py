from gi.repository import Gtk
class Action:
    def __init__(self, name, description, run, data=None, icon=None, cacheable=True):
        self.name = name
        self.description = description
        self.run = run
        self.data = data
        self.icon = icon
        self.cacheable = cacheable

    def __str__(self):
        return "{0}".format(self.name)

    def __repr__(self):
        return "<" + self.name + ">"


class ActionOperator:
    name = "ActionOperator"
    description = "Some thing"

    def operates_on(self, action):
        '''Return (X,Y)
        X = operates on object?
        Y = operates live on object? 
        The action should not be modified. '''
        if isinstance(action, Action):
            return (False, False)
        return (False, False)

    def reload(self):
        ''' reload the data if need be'''
        pass

    def get_actions_for(self, action, query=""):
        '''Return list of actions.
        if live = True current query will be given.
        operates_on(obj) guarenteed to be true.
        If you are live, it is your responsibility to make sure
        that the actions returned match the query
        The action should not be modified. '''
        return []


def get_icon(name):
    icon_theme = Gtk.IconTheme.get_default()
    icon_info = icon_theme.lookup_icon(name, 16, Gtk.IconLookupFlags.FORCE_SIZE)
    if icon_info is not None:
        pixbuf = icon_info.load_icon()
        return Gtk.Image().new_from_pixbuf(pixbuf)
    return None

class TextAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)
