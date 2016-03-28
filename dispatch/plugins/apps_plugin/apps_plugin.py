from dispatch.api import Action, ActionOperator, get_icon
from xdg.DesktopEntry import DesktopEntry
import subprocess
import os
import glob


class AppAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class AppsOperator(ActionOperator):
    '''Actions for non command line applications'''
    PATHS = ["/usr/share/applications", "~/.local/share/applications"]
    FILE_TYPE = "*.desktop"

    def __init__(self):
        ActionOperator.__init__(self)

        self.reload()

    def reload(self):
        self.actions = []
        for p in AppsOperator.PATHS:
            self.actions.extend(self._generate_app_actions(p))

    def operates_on(self, action):
        if action is None:
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        return self.actions

    def get_cmd(self, de):
        cmd = de.getExec()
        if "%" in cmd:
            cmd = cmd[:cmd.index("%")]
        return cmd

    def _generate_app_actions(self, path):
        app_actions = []
        filename_pattern = os.path.expanduser(os.path.join(
                path,
                AppsOperator.FILE_TYPE
        ))
        for filename in glob.glob(filename_pattern):
            app = DesktopEntry(filename)

            # TODO: Comply with  full DesktopEntries spec - OnlyShowIn, TryExec
            if app.getType() == "Application" and not app.getNoDisplay() and \
                    not app.getHidden() and not app.getTerminal():
                action = AppAction(
                    name=app.getName(),
                    description="application",
                    run=self._launch_application,
                    data={"desktop_entry": app, "cmd": self.get_cmd(app)},
                    icon=get_icon(app.getIcon()),
                )
                app_actions.append(action)
        return app_actions

    def _launch_application(self, action):
        if "cmd" in action.data:
            subprocess.Popen(action.data["cmd"].split())
