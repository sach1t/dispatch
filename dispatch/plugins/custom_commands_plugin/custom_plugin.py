from dispatch.api import Action, ActionOperator, FileAction, get_icon
import subprocess


class RandomOperator(ActionOperator):
    '''Operator for random actions'''

    def __init__(self):
        ActionOperator.__init__(self)

    def reload(self):
        pass

    def operates_on(self, action):
        if action is None:
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        act1 = Action(
            name="suspend",
            description="systemctl",
            run=self._run,
            data={"cmd": "systemctl suspend"}
        )
        return [act1]

    def _run(self, action):
        cmd = action.data["cmd"]
        subprocess.Popen(cmd, shell=True)


class SublimeOperator(ActionOperator):
    '''Actions to open a file with sublime'''

    def __init__(self):
        ActionOperator.__init__(self)

    def operates_on(self, action):
        if isinstance(action, FileAction):
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        subl3 = Action(
                name="Edit with subl3",
                description="open with sublime",
                run=self._open,
                data={"cmd": "subl3 " + action.data["path"]},
                icon=get_icon("text-x-generic")
            )
        return [subl3]

    def _open(self, action):
        if "cmd" in action.data:
            subprocess.Popen(action.data["cmd"].split())

    def reload(self):
        pass
