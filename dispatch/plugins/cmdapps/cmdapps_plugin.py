from dispatch.api import Action, ActionOperator, TextAction, get_icon
import subprocess
import os
import stat
from dispatch.plugins.apps import AppAction



class RunCommandOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)
        self.prompt = "run: "

    def operates_on(self, action):
        if action is None:
            return (True, True)
        return (False, False)
    def reload(self):
        pass

    def get_actions_for(self, action, query=""):
        query = query.strip()
        if query.startswith(self.prompt):
            query = query.replace(self.prompt, "", 1)

        act2 = CmdAction(
            name = self.prompt + query,
            description = "run command",
            run = self._launch_application,
            data = {"cmd": query},
            icon = get_icon("utilities-terminal"),
        )
        return [act2]

    def _launch_application(self, action):
        subprocess.Popen(action.data["cmd"], shell=True)


class AppWithArgsAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)

class AppArgumentOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)
        self.prompt = "args: "

    def operates_on(self, action):
        if isinstance(action, AppAction) or isinstance(action, CmdAction):
            return (True, True)
        return (False, False)

    def reload(self):
        pass

    def get_actions_for(self, action, query=""):
        query = query.strip()
        if query.startswith(self.prompt):
            query = query.replace(self.prompt, "", 1)

        act2 = AppWithArgsAction(
            name = self.prompt + query,
            description = "run with arguments",
            run = self._launch_application,
            data = action.data.copy()
        )
        act2.data["args"] = query
        if isinstance(action, CmdAction):
            act2.data["type"] = "cmd"
        else:
            act2.data["type"] = "app"
        return [act2]

    def _launch_application(self, action):
        cmd = ""
        if "type" in action.data and action.data["type"] == "cmd":
            cmd += "gnome-terminal -e "
        if "cmd" in action.data:
            cmd += action.data["cmd"]
        cmd += " "
        if "args" in action.data:
            cmd += action.data["args"]
        subprocess.Popen(cmd, shell=True)


class StdoutAction(Action):
    def __init__(self, name, description, run, data=None, icon=None, cacheable=False):
        Action.__init__(self, name, description, run, data, icon, cacheable)


class CmdAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class StdoutOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)

    def operates_on(self, action):
        if isinstance(action, CmdAction) or \
        isinstance(action, AppWithArgsAction) or \
        isinstance(action, AppAction) or \
        isinstance(action, StdoutAction):
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        if isinstance(action, StdoutAction):
            output = self._get_output(action)
            return [TextAction(
                name = output,
                description = "output from command",
                run = None,
                data = {}
            )]
        else:
            return [StdoutAction(
                name = "output",
                description = "get output",
                run = None,
                data = action.data
            )]

    def reload(self):
        pass

    def _get_output(self, stdout_action):
        if "cmd" in stdout_action.data:
            cmd = stdout_action.data["cmd"]
        cmd += " "
        if "args" in stdout_action.data:
            cmd += stdout_action.data["args"]   
        pipe = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        try:
            output = pipe.communicate(timeout=.250)[0].decode("utf-8").strip()
        except subprocess.TimeoutExpired:
            output = "Error: Process returned no output."
        return output


class CmdOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)
        self.actions = []
        self.paths = os.environ['PATH'].split(':')
        self.terminal = "gnome-terminal -e"
        self.generate_actions(self.paths)

    def reload(self):
        self.actions = []
        self.generate_actions(self.paths)

    def find_executables(self, directory):
        executables = []
        for filename in os.listdir(directory):
            path = directory + "/" + filename
            if os.path.isfile(path) and self.is_executable(path) and not os.path.islink(path):
                executables.append(filename)
        return executables

    def generate_actions(self, paths):
        for path in self.paths:
            execs = self.find_executables(path)
            for filename in execs:
                act = CmdAction(
                    name = filename,
                    description = "command line application",
                    run = self._open,
                    data = {"cmd":  filename},
                    icon = get_icon("utilities-terminal"),
                )
                self.actions.append(act)

    def is_executable(self, path):
        ''' Return True if the file or directory given by the path is
        executable '''
        executable = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
        st = os.stat(path)
        mode = st.st_mode
        if mode & executable:
            return True
        return False

    def operates_on(self, action):
        if action is None:
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        return self.actions

    def _open(self, action):
        if "cmd" in action.data:
            cmd = action.data["cmd"]
            subprocess.Popen(self.terminal + " " + cmd, shell=True)