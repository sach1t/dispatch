from dispatch.api import Action, ActionOperator
import os
import subprocess
import sys


class CommandOperator(ActionOperator):
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
            name = "suspend",
            description = "systemctl",
            run = self._run,
            data = {"cmd": "systemctl suspend"}
        )

        # Add commands here ... like above

        return [act1]

    def _run(self, action):
        cmd = action.data["cmd"]
        subprocess.Popen(cmd, shell=True)
