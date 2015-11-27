from dispatch.api import Action, ActionOperator, AppAction, AppWithArgsAction
from xdg.DesktopEntry import DesktopEntry 
from dispatch.plugins.cmds import CmdAction
import subprocess
import os
import glob


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
            description = "run with args",
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
        

class AppsOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)
        self.paths = ["/usr/share/applications", "~/.local/share/applications"]
        self.file_type = "*.desktop"
        self.actions = []
        for p in self.paths:
            self.actions.extend(self._generate_app_actions(p))

    def reload(self):
        self.actions = []
        for p in self.paths:
            self.actions.extend(self._generate_app_actions(p))   

    def operates_on(self, action):
        if action is None:
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        #if isinstance(action, QueryAction) ... 
        # not necessary since operates_on only 1 object
        #return [x for x in self.actions if x.name.lower().startswith(query)]
        return self.actions

    def get_cmd(self, de):
        cmd = de.getExec()
        if "%" in cmd:
            cmd = cmd[:cmd.index("%")]
        return cmd

    def _generate_app_actions(self, path):
        app_actions = []
        for filename in glob.glob(os.path.expanduser(os.path.join(path, self.file_type))):
            app = DesktopEntry(filename) # check the return now 

            if app.getType() == "Application" and not app.getNoDisplay() and not app.getHidden() \
            and not app.getTerminal():
            # not getTerminal bc we have no good way to find default terminal so user will have
            # to open term then launch it
            # TODO: Comply with  full DesktopEntries spec - OnlyShowIn, TryExec
                action = AppAction(
                    name = app.getName(),
                    description = "",
                    run = self._launch_application, 
                    data = {"desktop_entry": app, "cmd":self.get_cmd(app)}, # could reduce later to save on memory replace with cmd
                )
                app_actions.append(action)
        return app_actions

    def _launch_application(self, action):
        if "cmd" in action.data:
            subprocess.Popen(action.data["cmd"].split())
