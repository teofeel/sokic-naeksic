from sokic.api.services.DataSourcePlugin import DataSourcePlugin
from importlib.metadata import entry_points
from typing import Any

class PluginLoader:
    """
    Using Registry Pattern to register all available plugins
    """
    def __init__(self):
        self.datasource_plugins: dict[str, DataSourcePlugin] = {}
        self.visualizer_plugins: dict[str, Any] = {}


    def load_all(self):
        """
        Used to load all available plugins
        :return:
        """
        self.load_all_datasource()
        self.load_all_visualizer()


    def load_all_datasource(self):
        """
        Used to load all available datasource plugins
        :return:
        """
        for ep in entry_points(group='sokic.datasource'):
            p = ep.load()
            plugin: DataSourcePlugin = p()
            plugin_type: str = plugin.type()

            if plugin_type != "datasource":
                continue

            plugin_name: str = plugin.name()
            self.datasource_plugins[plugin_name] = plugin


    def load_all_visualizer(self):
        """
        Used to load all available visualizer plugins
        :return:
        """
        for ep in entry_points(group='sokic.visualizer'):
            p = ep.load()
            plugin: Any = p()
            plugin_type: str = plugin.type()

            if plugin_type != "visualizer":
                continue

            plugin_name: str = plugin.name()
            self.visualizer_plugins[plugin_name] = plugin


    def load_plugin_by_name(self, group: str, name: str):
        """
        Used to load a plugin by its name
        :param group:
        :param name:
        :return:
        """
        eps = entry_points(group=group)
        target = eps.select(name=name)

        if target:
            ep = list(target)[0]
            plugin_instance = ep.load()()

            if group == 'sokic.datasource':
                self.datasource_plugins[name] = plugin_instance
            else:
                self.visualizer_plugins[name] = plugin_instance
