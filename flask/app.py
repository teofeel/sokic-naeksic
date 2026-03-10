from flask import Flask, render_template_string, render_template, request, jsonify

#from api.models import Graph
from core.sokic.core.use_cases.InMemoryWorkspaceRepository import InMemoryWorkspaceRepository
from core.sokic.core.use_cases.WorkspaceManager import WorkspaceManager
from core.sokic.core.use_cases.plugin_loader import PluginLoader
from core.sokic.core.use_cases.Workspace import Workspace
from core.sokic.core.use_cases import SearchServiceImpl, FilterServiceImpl, FilterParseError, FilterTypeError
import json
from utils.workspace import create_default_workspace
from utils.graph import generate_graph

loader = PluginLoader()
loader.load_all()
workspace_manager = WorkspaceManager(loader, InMemoryWorkspaceRepository())

search_service = SearchServiceImpl()
filter_service = FilterServiceImpl()

import os
from pathlib import Path
current_dir = Path(__file__).resolve().parent
template_path = current_dir.parent / 'core' / 'templates'
app = Flask(__name__)


# @app.route("/")
# def index():
#     return ("<p> hello teammates, please implement me </p>"
#             "🥺"
#             "<p>👉👈</p>")

@app.route('/')
def test_visualizer():
    #yaml_plugin = loader.plugins['datasource']['json']
    #print(yaml_plugin)
#
    #graph_model = yaml_plugin.convert_to_graph('test.json')
    #print("graf: ")
    #print(graph_model.edges)
    #print(graph_model.nodes)
#
    #visualizer = loader.plugins['visualizer']['block']
    #visualizer = loader.plugins['visualizer']['simple']
    #graph_html = visualizer.visualize(graph_model)
    #print(graph_html)

    return render_template('header.html')


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


@app.route("/workspace-test")
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

@app.route("/plugins/available")
def available():
    type = request.args.get('type')
    if not type:
        return []

    available_plugins = loader.get_all_available_plugins(type)
    return available_plugins

@app.route('/workspace/data/<workspace_id>', methods=['PUT'])
def change_data(workspace_id):
    try:
        if workspace_id is None: raise ValueError('Workspace id is required')

        if 'data' not in request.files: raise ValueError('No data provided')

        file = request.files['data']
        graph, _ = generate_graph(loader, file)

        if workspace_manager.get_workspace(workspace_id) is None:
            raise ValueError('Workspace not found')

        workspace_manager.set_new_graph(workspace_id, graph)

        return jsonify({'success': True}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/workspace/visualizer/<workspace_id>', methods=['PUT'])
def change_visualizer(workspace_id):
    try:
        if workspace_id is None: raise ValueError('Workspace id is required')
        visualizer_key = request.form.get('visualizer')

        success = workspace_manager.set_visualizer(workspace_id, visualizer_key)

        if not success:
            raise Exception('Some issues occurred....')

        return jsonify({'success': True}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/workspace")
def get_workspaces():
    try:
        workspaces = workspace_manager.get_all_workspaces_metadata()
        if not workspaces:
            create_default_workspace(workspace_manager)
            return workspace_manager.get_all_workspaces_metadata()

        return workspaces, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/workspace", methods=['POST'])
def create_workspace():
    try:
        if 'data' not in request.files: raise ValueError('No data provided')

        file = request.files['data']
        workspace_name = request.form.get('name')
        visualizer_key = request.form.get('visualizer')

        graph, extension = generate_graph(loader, file)

        workspace_id = workspace_manager.create_workspace(workspace_name, graph, extension, visualizer_key)

        return jsonify({'success': True, 'workspace_id': workspace_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/workspace/<workspace_id>")
def get_workspace_metadata(workspace_id):
    try:
        ws: Workspace = workspace_manager.get_workspace(workspace_id)
        if not ws:
            raise ValueError('Workspace not found')

        res = {
            'filters': ws.get_filters(),
            'search': ws.get_search(),
            'name': ws.name,
            'id': ws.id,
            'visualizer': ws.visualizer.name()
        }

        return res, 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    create_default_workspace(workspace_manager)
    app.run(debug=True)
