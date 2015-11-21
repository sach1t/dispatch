from dispatch.api import Action, ActionOperator
from xdg.DesktopEntry import DesktopEntry 
import subprocess
import os
import glob


class AppAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class AppsOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)
        self.paths = ["/usr/share/applications", "~/.local/share/applications"]
        self.file_type = "*.desktop"

    def operates_on(self, action):
        if isinstance(action, QueryAction):
            return (True, False)

    def get_actions_for(self, action, query_action=None):
        #if isinstance(action, QueryAction) ... 
        # not necessary since operates_on only 1 object
        actions = []
        for p in self.paths:
            actions.extend(self._generate_app_actions(p))
        return actions

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