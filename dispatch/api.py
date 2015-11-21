class Action:
    def __init__(self, name, description, run, data=None, icon=None):
        self.name = name
        self.description = description
        self.run = run
        self.data = data
        self.icon = icon

    def __str__(self):
        return "{0} : {1}".format(self.name, self.description)

    def __repr__(self):
        return "<" + self.name + ">"


class ActionOperator:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def operates_on(obj):
        '''Return (X,Y)
        X = operates on object?
        Y = operates live on object?
        '''
        if isinstance(obj, Action):
            return (True, False)

    def get_actions_for(obj, query=""):
    '''
    Return list of actions.
    if live = True current query will be given.
    operates_on(obj) guarenteed to be true.
    '''
    return []

