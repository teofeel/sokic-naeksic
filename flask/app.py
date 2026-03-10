from flask import Flask, render_template_string, render_template, request, jsonify

from core.sokic.core.use_cases.InMemoryWorkspaceRepository import InMemoryWorkspaceRepository
from core.sokic.core.use_cases.WorkspaceManager import WorkspaceManager
from core.sokic.core.use_cases.plugin_loader import PluginLoader
from core.sokic.core.use_cases import SearchServiceImpl, FilterServiceImpl, FilterParseError, FilterTypeError

loader = PluginLoader()
loader.load_all()
workspace_manager = WorkspaceManager(loader, InMemoryWorkspaceRepository())

search_service = SearchServiceImpl()
filter_service = FilterServiceImpl()

import os
from pathlib import Path
current_dir = Path(__file__).resolve().parent
template_path = current_dir.parent / 'core' / 'templates'
app = Flask(__name__, template_folder=str(template_path))


# @app.route("/")
# def index():
#     return ("<p> hello teammates, please implement me </p>"
#             "🥺"
#             "<p>👉👈</p>")

@app.route('/')
def test_visualizer():

    yaml_plugin = loader.plugins['datasource']['json']
    print(yaml_plugin)

    graph_model = yaml_plugin.convert_to_graph('test.json')
    print("graf: ")
    print(graph_model.edges)
    print(graph_model.nodes)

    #visualizer = loader.plugins['visualizer']['block']
    visualizer = loader.plugins['visualizer']['simple']
    graph_html = visualizer.visualize(graph_model)
    # print(graph_html)

    return render_template('main-view.html', plugin_html=graph_html)

    #return render_template_string("""
    #    <!DOCTYPE html>
    #    <html>
    #    <head><title>Graph Test</title></head>
    #    <body>
    #        <h1>Graph Visualization Test</h1>
    #        {{ graph_content | safe }}
    #    </body>
    #    </html>
    #""", graph_content=graph_html)
@app.route('/test-search')
def test_filter_and_search():
    yaml_plugin = loader.plugins['datasource']['yaml']
    graph = yaml_plugin.convert_to_graph('test.yaml')

    results = {}

    # ── SEARCH ───────────────────────────────────────────────────
    results["search_nikola"]  = [n.id for n in search_service.search_nodes(graph, "nikola")]
    results["search_born"]    = [n.id for n in search_service.search_nodes(graph, "born")]
    results["search_1995"]    = [n.id for n in search_service.search_nodes(graph, "1995")]
    results["search_grandpa"] = [n.id for n in search_service.search_edges(graph, "grandpa")]

    # ── FILTER ───────────────────────────────────────────────────
    results["filter_born>=1990"]  = [n.id for n in filter_service.filter_nodes(graph, "born >= 1990")]
    results["filter_born==1995"]  = [n.id for n in filter_service.filter_nodes(graph, "born == 1995")]
    results["filter_born<1970"]   = [n.id for n in filter_service.filter_nodes(graph, "born < 1970")]
    results["filter_role==Sin"]   = [n.id for n in filter_service.filter_nodes(graph, "role == Sin")]
    results["filter_name!=Marko"] = [n.id for n in filter_service.filter_nodes(graph, "name != Marko")]

    # ── CHAINING: filter to search ────────────────────────────────
    g2 = filter_service.filter_subgraph(graph, "born >= 1990")
    g3 = search_service.search_subgraph(g2, "a")
    results["chain_filter_then_search"] = [n.id for n in g3.nodes.values()]

    # ── ERROR handling ────────────────────────────────────────────
    try:
        filter_service.filter_nodes(graph, "born >= notanumber")
    except FilterTypeError as e:
        results["type_error"] = str(e)

    try:
        filter_service.filter_nodes(graph, "this is not valid")
    except FilterParseError as e:
        results["parse_error"] = str(e)

    return results


@app.route("/workspace")
def workspace():
    plugin = loader.plugins['datasource']['yaml']

    graph = plugin.convert_to_graph('test.yaml')

    manager = WorkspaceManager(loader, InMemoryWorkspaceRepository())

    id = manager.create_workspace('test', graph, 'yaml', 'block')

    # manager.add_filter("born > 1995", id)
    # manager.set_visualizer('simple', id)
    #manager.set_filters(id, ["born > 1995"])
    manager.set_visualizer(id, 'block')
    graph_html = manager.get_render(id)
   
    return render_template('main-view.html', plugin_html=graph_html)

@app.route("/available")
def available():
    available_plugins = loader.get_all_available_plugins("datasource")
    return available_plugins

@app.route('/load-file', methods=['POST'])
def load_file():
    workspace_id = request.args.get('id')
    
    try:
        if workspace_id is None: raise ValueError('Workspace id is required')

        if 'data' not in request.files: raise ValueError('No data provided')

        file = request.files['data']
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

        if workspace_manager.get_workspace(workspace_id) is None:
            raise ValueError('Workspace not found')

        workspace_manager.set_new_graph(workspace_id, graph)

        return jsonify({'success': True}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    id = workspace_manager.create_workspace('test', None, 'yaml', 'block')
    print(id)
    app.run(debug=True)
