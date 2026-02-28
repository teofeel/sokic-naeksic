from sokic.api.services.DataSourcePlugin import DataSourcePlugin
from sokic.api.services.Plugin import Plugin
from sokic.api.services.VisualizerPlugin import VisualizerPlugin
from importlib.metadata import entry_points
from typing import Any, Union
from collections import defaultdict

class PluginLoader:
    """
    Using Registry Pattern to register all available plugins
    """
    def __init__(self):
        self.plugins: dict[str, dict[str, Union[DataSourcePlugin, VisualizerPlugin]]] = defaultdict(dict)


    def load_all(self):
        """
        Used to load all available plugins
        :return:
        """
        for ep in entry_points(group='sokic.plugin'):
            p = ep.load()
            plugin: Any = p()
            plugin_type: str = plugin.type()


            plugin_name: str = plugin.name()
            self.plugins[plugin_type][plugin_name] = plugin
        #self.load_all_datasource()
        #self.load_all_visualizer()


    #def load_all_datasource(self):
    #    """
    #    Used to load all available datasource plugins
    #    :return:
    #    """
    #    for ep in entry_points(group='sokic.datasource'):
    #        p = ep.load()
    #        plugin: DataSourcePlugin = p()
    #        plugin_type: str = plugin.type()
#
    #        if plugin_type != "datasource":
    #            continue
#
    #        plugin_name: str = plugin.name()
    #        self.plugins['datasource'][plugin_name] = plugin
#
#
    #def load_all_visualizer(self):
    #    """
    #    Used to load all available visualizer plugins
    #    :return:
    #    """
    #    for ep in entry_points(group='sokic.visualizer'):
    #        p = ep.load()
    #        plugin: Any = p()
    #        plugin_type: str = plugin.type()
#
    #        if plugin_type != "visualizer":
    #            continue
#
    #        plugin_name: str = plugin.name()
    #        self.plugins['visualizer'][plugin_name] = plugin
#

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
            p = ep.load()

            plugin: DataSourcePlugin | VisualizerPlugin = p()
            plugin_type: str = plugin.type()
            plugin_name: str = plugin.name()

            self.plugins[plugin_type][plugin_name] = plugin
