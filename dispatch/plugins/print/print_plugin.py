from dispatch.api import Action, ActionOperator, TextAction
import subprocess


class PrintAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class PrintOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)

    def operates_on(self, action):
        if isinstance(action, Action):
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        return [PrintAction(
            name = "print name",
            description = "print name",
            run = self.output,
            data = {"text": action.name}
        )]

    def output(self, action):
        cmd = "notify-send " + action.data["text"]
        subprocess.Popen(cmd, shell=True)
