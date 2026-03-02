from flask import Flask, render_template_string, render_template
from core.sokic.core.use_cases.plugin_loader import PluginLoader
from sokic.api.services.search_service import SearchService, FilterTypeError, FilterParseError
loader = PluginLoader()
loader.load_all()

search_service = SearchService()
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

    yaml_plugin = loader.plugins['datasource']['yaml']
    print(yaml_plugin)

    graph_model = yaml_plugin.convert_to_graph('test.yaml')
    print("graf: ")
    print(graph_model.edges)
    print(graph_model.nodes)

    visualizer = loader.plugins['visualizer']['block']

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
def test_all():
    yaml_plugin = loader.plugins['datasource']['yaml']
    graph = yaml_plugin.convert_to_graph('test.yaml')

    results = {}

    # ── SEARCH tests ─────────────────────────────────────────────
    results["search_nikola"]  = [n.id for n in search_service.search_nodes(graph, "nikola")]
    results["search_born"]    = [n.id for n in search_service.search_nodes(graph, "born")]
    results["search_1995"]    = [n.id for n in search_service.search_nodes(graph, "1995")]
    results["search_grandpa"] = [n.id for n in search_service.search_edges(graph, "grandpa")]

    # ── FILTER tests ─────────────────────────────────────────────
    results["filter_born>=1990"]  = [n.id for n in search_service.filter_nodes(graph, "born >= 1990")]
    results["filter_born==1995"]  = [n.id for n in search_service.filter_nodes(graph, "born == 1995")]
    results["filter_born<1970"]   = [n.id for n in search_service.filter_nodes(graph, "born < 1970")]
    results["filter_role==Sin"]   = [n.id for n in search_service.filter_nodes(graph, "role == Sin")]
    results["filter_name!=Marko"] = [n.id for n in search_service.filter_nodes(graph, "name != Marko")]

    # ── CHAINING: filter then search ─────────────────────────────
    g2 = search_service.filter_subgraph(graph, "born >= 1990")
    g3 = search_service.search_subgraph(g2, "a")
    results["chain_filter_then_search"] = [n.id for n in g3.nodes.values()]

    # ── ERROR handling  ───────────────────────────
    try:
        search_service.filter_nodes(graph, "born >= notanumber")
    except FilterTypeError as e:
        results["type_error"] = str(e)

    try:
        search_service.filter_nodes(graph, "this is not valid")
    except FilterParseError as e:
        results["parse_error"] = str(e)

    return results
if __name__ == "__main__":
    app.run(debug=True)
