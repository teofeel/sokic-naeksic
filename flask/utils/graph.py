from werkzeug.datastructures import FileStorage
from core.sokic.core.use_cases import PluginLoader
import os

def generate_graph(loader: PluginLoader, file: FileStorage):
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower().lstrip('.')

    available_plugins = loader.get_all_available_plugins("datasource")
    if available_plugins is [] or extension not in available_plugins:
        raise ValueError(f'No plugin available for .{extension}')

    plugin_category = loader.plugins.get("datasource", {})
    if not plugin_category:
        raise Exception('There arent any datasource plugins registered')

    plugin = plugin_category.get(extension)
    graph = plugin.convert_to_graph(file.stream)

    return graph, extension