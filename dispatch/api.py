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
        Y = operates live on object? '''
        if isinstance(action, Action):
            return (False, False)
        return (False, False)

    def reload(self):
        ''' reload the data '''
        pass

    def get_actions_for(self, action, query=""):
        '''Return list of actions.
        if live = True current query will be given.
        operates_on(obj) guarenteed to be true.
        If you are live, it is your responsibility to make sure
        that the actions returned match the query'''
        return []


class AppAction(Action):
    def __init__(self, name, description, run, data=None, icon=None, cacheable=True):
        Action.__init__(self, name, description, run, data, icon, cacheable)


class AppWithArgsAction(Action):
    def __init__(self, name, description, run, data=None, icon=None, cacheable=True):
        Action.__init__(self, name, description, run, data, icon, cacheable)


class TextAction(Action):
    def __init__(self, name, description, run, data=None, icon=None, cacheable=True):
        Action.__init__(self, name, description, run, data, icon, cacheable)
