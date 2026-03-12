from flask import render_template

from core.sokic.core.use_cases.Workspace import Workspace


class ViewRenderer:

    def render_views_from_workspace(self, workspace: Workspace):
        if workspace is None or workspace.source_graph is None or workspace.visualizer is None:
            return None

        plugin_html = workspace.render()
        return render_template("combined-views.html", plugin_html=plugin_html)

    def render_views_from_html(self, plugin_html: str):
        return render_template("combined-views.html", plugin_html=plugin_html)
