import pkgutil
import sys
import os


class PluginManager:
    '''Loads plugin operators.'''

    PATH = os.path.join(os.path.dirname(__file__), "plugins")
    PACKAGE = "dispatch.plugins"
    MODULES = pkgutil.iter_modules(path=[PATH])

    def __init__(self):
        self.plugins = []
        self.load_operators()

    def load_operators(self):
        for loader, module_name, ispkg in PluginManager.MODULES:
            if module_name not in sys.modules:
                loaded_module = __import__(PluginManager.PACKAGE + "." + module_name,
                                           fromlist=[module_name])
                class_names = \
                    [x for x in dir(loaded_module) if x.endswith("Operator")]
                for class_name in class_names:
                    loaded_class = getattr(loaded_module, class_name)
                    obj = loaded_class()
                    self.plugins.append(obj)

    def get_operators(self):
        return self.plugins

    def _get_class_name(self, module_name):
        words = module_name.split("_")
        for word_index in range(len(words)):
            words[word_index] = words[word_index].title()
        words.append("Operator")
        classname = "".join(words)
        return classname
