import pkgutil
import sys
import os 

path = os.path.join(os.path.dirname(__file__), "plugins")
package = "dispatch.plugins"
modules  = pkgutil.iter_modules	(path=[path])

# Job is to load the plugins and load any new ones -> 

class PluginManager:
	def __init__(self):
		self.plugins = []

	def load_plugins(self):
		for loader, module_name, ispkg in  modules:
			if module_name not in sys.modules:
				loaded_module = __import__(package + "." + module_name, fromlist=[module_name])

				class_name = self._get_class_name(module_name)
				loaded_class = getattr(loaded_module, class_name)

				obj = loaded_class()
				self.plugins.append(obj)

	def get_plugins(self):
		return self.plugins

	def _get_class_name(self, module_name):
		words = module_name.split("_")
		for word_index in range(len(words)):
			words[word_index] = words[word_index].title()
		words.append("Operator")
		classname = "".join(words)

		return classname