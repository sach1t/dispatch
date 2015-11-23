from dispatch.api import Action, ActionOperator
from xdg.DesktopEntry import DesktopEntry 
import subprocess
import os
import glob


class AppAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class TimedAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class RootOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)
        self.actions = []
        for x in os.listdir("/"):
            act = TimedAction(
                "|" + x,
                "",
                run = self.timed_run,
                data = {"cmd" : "xdg-open /" +x}
                )
            self.actions.append(act)

    def operates_on(self, action):
        if action is None:
            return (True, True)
        return (False, False)

    def get_actions_for(self, action, query=""):
        # it is your responsibility to make sure that the actions
        # returned match the query
        matches = [x for x in self.actions if x.name.startswith(query)]
        return matches

    def timed_run(self, action):
        cmd = action.data["cmd"]
        subprocess.Popen(cmd, shell=True)



class AppTimeOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)

    def operates_on(self, action):
        if isinstance(action, AppAction):
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        actions = []
        name = action.name
        cmd = action.data["desktop_entry"].getExec()
        if "%" in cmd:
            cmd = cmd[:cmd.index("%")]

        for x in range(0, 60, 5):
            act = TimedAction(
                "in " + str(x) + " sec",
                "",
                run = self.timed_run,
                data = {"cmd" : "sleep " + str(x) + " && " + cmd}
                )
            actions.append(act)
        return actions

    def timed_run(self, action):
        cmd = action.data["cmd"]
        subprocess.Popen(cmd, shell=True)
        


class AppArgumentOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)

    def operates_on(self, action):
        if isinstance(action, AppAction):
            return (True, True)
        return (False, False)

    def get_actions_for(self, action, query=""):
        if "desktop_entry" in action.data:
            cmd = action.data["desktop_entry"].getExec()
            if "%" in cmd:
                cmd = cmd[:cmd.index("%")]

        act = AppAction(
            name = "run with args: " + query,
            description = "run with args",
            run = self._launch_application,
            data = {"cmd": cmd + " " + query}
            )
        return [act]

    def _launch_application(self, action):
        if "cmd" in action.data:
            cmd = action.data["cmd"]
            subprocess.Popen(cmd.split())



class AppsOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)
        self.paths = ["/usr/share/applications", "~/.local/share/applications"]
        self.file_type = "*.desktop"
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
                    data = {"desktop_entry": app}, # could reduce later to save on memory replace with cmd
                )
                app_actions.append(action)
        return app_actions

    def _launch_application(self, action):
        if "desktop_entry" in action.data:
            cmd = action.data["desktop_entry"].getExec()
            if "%" in cmd:
                cmd = cmd[:cmd.index("%")]
            subprocess.Popen(cmd.split())
            return []