from gi.repository import Gtk


class Action:
    '''Action base class'''

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


class TextAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class FileAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class DirectoryAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class ActionOperator:
    '''Operator base class'''

    name = "ActionOperator"
    description = "Description"

    def operates_on(self, action):
        '''Return (operates_on, live)
        operates_on = operates on the given action?
        live = returns non-static results for the action

        If the operator does not require an action to work, i.e. it
        shows actions on main screen and not as an option to an existing action
        it should check that the action is None first.
        (look at FileOperator in file_dir_plugin)

        The action should not be modified.'''
        if isinstance(action, Action):
            return (False, False)
        return (False, False)

    def reload(self):
        ''' reload the data if need be'''
        pass

    def get_actions_for(self, action, query=""):
        '''Return list of actions.
        Action is guaranteed to be of required type, as specified by
        operates_on function. if non_static was specified as True when
        operates_on was called, the users current query will be given,
        and this function should ensure that the actions returned match
        the query as no filtering of the results will occur. The the
        action should not be modified. '''
        return []


def get_icon(name):
    icon_theme = Gtk.IconTheme.get_default()
    icon_info = icon_theme.lookup_icon(name, 16, Gtk.IconLookupFlags.FORCE_SIZE)
    if icon_info is not None:
        pixbuf = icon_info.load_icon()
        return Gtk.Image().new_from_pixbuf(pixbuf)
    return None
