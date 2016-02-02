from dispatch.api import Action, ActionOperator, get_icon
import subprocess
import os
import fnmatch

class FileAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)

class DirectoryAction(Action):
    def __init__(self, name, description, run, data=None, icon=None):
        Action.__init__(self, name, description, run, data, icon)

class FileActionOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)

    def operates_on(self, action):
        if isinstance(action, FileAction):
            return (True, False)
        return (False, False)

    def get_actions_for(self, action, query=""):
        subl3 = Action(
                name = "Edit with subl3",
                description = "open with sublime",
                run = self._open,
                data = {"cmd": "subl3 " + action.data["path"]},
                icon = get_icon("text-x-generic")
            )
        return [subl3]

    def _open(self, action):
        if "cmd" in action.data:
            subprocess.Popen(action.data["cmd"].split())

    def reload(self):
        pass

class DirectoryPathOperator(ActionOperator):
    def __init__(self):
        ActionOperator.__init__(self)

    def operates_on(self, action):
        if isinstance(action, DirectoryAction):
            return (True, False)
        return (False, False)

    def reload(self):
        pass

    def get_actions_for(self, action, query=""):
        path = action.data["path"]
        actions = []
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)
            if os.path.isfile(fpath):
                act = FileAction(
                    name = fname,
                    description = "file:" + fpath,
                    run = self._open,
                    data = {"path": fpath},
                    icon = get_icon("text-x-generic")
                )
                actions.append(act)
            elif os.path.isdir(fpath):
                act = DirectoryAction(
                    name = fname,
                    description = "dir:" + fpath,
                    run = self._open,
                    data = {"path": fpath},
                    icon = get_icon("folder")
                )
                actions.append(act)
        return actions

    def _open(self, action):
        if "path" in action.data:
            cmd = ["xdg-open", action.data["path"]]
            subprocess.Popen(cmd)
            return []

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
                    description = "file:" + curr,
                    run = self._open,
                    data = {"path": curr},
                    icon = get_icon("text-x-generic")
                )
                file_actions.append(action)

            elif os.path.isdir(curr) and not os.path.islink(curr):
                action = DirectoryAction(
                    name = curr_basename,
                    description = "dir:" + curr,
                    run = self._open,
                    data = {"path": curr},
                    icon = get_icon("folder")
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
