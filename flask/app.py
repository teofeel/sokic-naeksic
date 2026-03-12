from flask import Flask, render_template_string, render_template, request, jsonify
from sokic.core.use_cases.InMemoryWorkspaceRepository import InMemoryWorkspaceRepository
from sokic.core.use_cases.WorkspaceManager import WorkspaceManager
from sokic.core.use_cases.command_processor import CommandProcessor
from sokic.core.use_cases.plugin_loader import PluginLoader
from sokic.core.use_cases.Workspace import Workspace
from sokic.core.use_cases import SearchServiceImpl, FilterServiceImpl, FilterParseError, FilterTypeError
from sokic.core.use_cases.view_renderer import ViewRenderer
from utils.workspace import create_default_workspace
from utils.graph import generate_graph

from pathlib import Path
from jinja2 import ChoiceLoader, FileSystemLoader

command_processor = CommandProcessor()
loader = PluginLoader()
loader.load_all()
workspace_manager = WorkspaceManager(loader, InMemoryWorkspaceRepository())
search_service = SearchServiceImpl()
filter_service = FilterServiceImpl()
renderer = ViewRenderer()

current_dir = Path(__file__).resolve().parent
core_templates = current_dir.parent / 'core' / 'templates'

app = Flask(__name__)

app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader(str(core_templates)),
])


@app.route('/')
def test_visualizer():

    return render_template('index.html')


@app.route('/cli-command')
def cli_command():
    cmd = request.args.get('command')
    workspace_id = request.args.get('workspace')
    active_workspace = workspace_manager.get_workspace(workspace_id)
    res = command_processor.process_command(cmd, active_workspace)
    workspace_manager.repository.update(active_workspace)
    return res

@app.route('/workspace/views/<workspace_id>')
def get_workspace_views(workspace_id):
    workspace = workspace_manager.get_workspace(workspace_id)

    return renderer.render_views_from_workspace(workspace) or '', 200


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

@app.route('/workspace/<workspace_id>/search', methods=['PUT'])
def search_workspace(workspace_id):
    try:
        ws = workspace_manager.get_workspace(workspace_id)
        if not ws:
            raise ValueError('Workspace not found')

        query = request.form.get('query')
        if not query:
            raise ValueError('Search query is required')

        workspace_manager.add_search(query, workspace_id)
        graph_html = workspace_manager.get_render(workspace_id)

        return jsonify({'success': True, 'html': graph_html}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/workspace/<workspace_id>/filter', methods=['PUT'])
def filter_workspace(workspace_id):
    try:
        ws = workspace_manager.get_workspace(workspace_id)
        if not ws:
            raise ValueError('Workspace not found')

        filter_query = request.form.get('filter')
        if not filter_query:
            raise ValueError('Filter query is required')

        workspace_manager.add_filter(filter_query, workspace_id)
        graph_html = workspace_manager.get_render(workspace_id)

        return jsonify({'success': True, 'html': graph_html}), 200

    except FilterParseError as e:
        return jsonify({'error': str(e), 'type': 'parse_error'}), 400
    except FilterTypeError as e:
        return jsonify({'error': str(e), 'type': 'type_error'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/workspace/<workspace_id>/reset', methods=['PUT'])
def reset_workspace(workspace_id):
    try:
        ws = workspace_manager.get_workspace(workspace_id)
        if not ws:
            raise ValueError('Workspace not found')

        workspace_manager.reset_workspace(workspace_id)
        graph_html = workspace_manager.get_render(workspace_id)

        return jsonify({'success': True, 'html': graph_html}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    create_default_workspace(workspace_manager)
    app.run(debug=True)
