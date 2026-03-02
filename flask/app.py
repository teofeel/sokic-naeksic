from flask import Flask, render_template_string, render_template, request
from core.sokic.core.use_cases.plugin_loader import PluginLoader
loader = PluginLoader()
loader.load_all()


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


@app.route('/load-file', methods=['POST'])
def load_file():
    file = request.files['data']

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower().lstrip('.')

    plugin = loader.plugins['datasource'][ext]
    graph = plugin.convert_to_graph(file.stream)

    visualizer = loader.plugins['visualizer']['block']
    graph_html = visualizer.visualize(graph)

    return render_template('main-view.html', plugin_html=graph_html)

    # add to active workspace and show on page

if __name__ == "__main__":
    app.run(debug=True)
