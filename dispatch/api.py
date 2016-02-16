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
        '''Return (operates_on, non_static)
        operates_on = operates on the action?
        non_static = returns non-static results for action
        The action should not be modified. '''
        if isinstance(action, Action):
            return (False, False)
        return (False, False)

    def reload(self):
        ''' reload the data if need be'''
        pass

    def get_actions_for(self, action, query=""):
        '''Return list of actions.
        action is guarenteed to be of required type, as specified by operates_on function.
        if non_static was specified as True when operates_on was called, the users current
        query will be given, and this function should ensure that the actions returned match
        the query as no filtering of the results will occur.
        The the action should not be modified. '''
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
