from flask import Flask, render_template_string
from core.sokic.core.use_cases.plugin_loader import PluginLoader
loader = PluginLoader()
loader.load_all()

app = Flask(__name__)


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

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head><title>Graph Test</title></head>
        <body>
            <h1>Graph Visualization Test</h1>
            {{ graph_content | safe }}
        </body>
        </html>
    """, graph_content=graph_html)


if __name__ == "__main__":
    app.run(debug=True)
