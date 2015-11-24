from dispatch.api import Action, ActionOperator, TextAction, AppAction, AppWithArgsAction
import subprocess
import os
import stat

class StdoutAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)

class CmdAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class StdoutPipeOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)    

    def operates_on(self, action):
        if isinstance(action, StdoutAction):
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        if "cmd" in action.data:
            cmd = action.data["cmd"]
        cmd += " "
        if "args" in action.data:
            cmd += action.data["args"]    
        output = subprocess.check_output(cmd.split()).decode("utf-8")
        return [TextAction(
            name = output,
            description = output,
            run = self._print,
            data = {}
            )]

    def _print(self, action):
        pass
        #subprocess.Popen('notify-send ' + '"`{}`"'.format(action.name), shell=True)



class StdoutOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)

    def operates_on(self, action):
        if isinstance(action, CmdAction) or isinstance(action, AppWithArgsAction):
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        return [StdoutAction(
            name = "get output",
            description = "",
            run = self._open,
            data = action.data
            )]

    def _open(self, action):
        if "cmd" in action.data:
            cmd = action.data["cmd"]
        cmd += " "
        if "args" in action.data:
            cmd += action.data["args"]
        subprocess.Popen('notify-send ' + '"`{}`"'.format(cmd), shell=True)



class CmdOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)
        self.actions = []
        #self.paths = "/usr/local/sbin:/usr/local/bin:/usr/bin:/opt/android-sdk/platform-tools:/opt/android-sdk/tools:/"
        self.paths = os.environ['PATH'].split(':')
        self.terminal = "gnome-terminal"
        self.generate_actions(self.paths)

    def find_executables(self, directory):
        executables = []
        for filename in os.listdir(directory):
            path = directory + "/" + filename
            if os.path.isfile(path) and self.is_executable(path) and not os.path.islink(path):
                executables.append(filename)
        return executables

    def generate_actions(self, paths):
        env_paths = os.environ['PATH'].split(':')
        for path in env_paths:
            execs = self.find_executables(path)
            for filename in execs:
                act = CmdAction(
                    name = filename,
                    description = "",
                    run = self._open,
                    data = {"cmd":  filename}
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
            subprocess.Popen("gnome-terminal -e " + cmd, shell=True)