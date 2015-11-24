from dispatch.api import Action, ActionOperator
import subprocess
import os
import fnmatch

class FileAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)

class DirectoryAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)


class FileOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)
        self.paths = ["~"]
        self.actions = []
        self.exclude = ["*.pyc", "__pycache__"]
        for p in self.paths:
            self.actions.extend(self._generate_file_actions(p))


    def operates_on(self, action):
        if action is None:
            return (True, False)
        return (False, False)


    def reload(self):
        self.actions = []
        for p in self.paths:
            self.actions.extend(self._generate_file_actions(p))


    def get_actions_for(self, action, query=""):
        return self.actions

    def matches_exclude(self, basename):
        for pattern in self.exclude:
            if fnmatch.fnmatch(basename, pattern):
                return True

    def _generate_file_actions(self, path):
        # we dont follow links bc of potential link loops

        path = os.path.expanduser(path)
        file_actions = []

        stack = [path]
        while stack:
            curr = stack.pop()
            curr_basename = os.path.basename(curr)

            if curr_basename.startswith(".") or self.matches_exclude(curr_basename):
                pass
            elif os.path.isfile(curr) and not os.path.islink(curr):
                action = FileAction(
                    name = curr_basename,
                    description = "file",
                    run = self._open,
                    data = {"path": curr}
                )
                file_actions.append(action)

            elif os.path.isdir(curr) and not os.path.islink(curr):
                action = DirectoryAction(
                    name = curr_basename,
                    description = "directory",
                    run = self._open,
                    data = {"path": curr}
                )
                file_actions.append(action)

                for f in os.listdir(curr):
                    f_path = os.path.join(curr, f)
                    stack.append(f_path)
        return file_actions


    def _open(self, action):
        if "path" in action.data:
            cmd = ["xdg-open", action.data["path"]]
            subprocess.Popen(cmd)
            return []
