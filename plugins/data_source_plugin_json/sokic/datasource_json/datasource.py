import collections
from collections import deque
from itertools import cycle

from sokic.api.models import Graph
from sokic.api.services.DataSourcePlugin import DataSourcePlugin
from sokic.api.models.graph import Graph
from sokic.api.models.graph_direction import GraphDirection
from sokic.api.models.graph_cycle import GraphCycle
from sokic.api.models.node import Node
from sokic.api.models.edge import Edge
import json

class JsonDataSource(DataSourcePlugin):
    def __init__(self, config: dict[str, str] | None = None):
        """
        :param config: Dictionary of configuration parameters,
                        must have keys: id_attribute, ref_attribute, children_attribute.
                        If key is missing it will use default key. If config is not provided it will use default_config
        """
        default_config = {
            "id_attribute": "@id",
            "ref_attribute": "@ref",
            "children_attribute": "children"
        }

        if config:
            self.config = {**default_config, **config}
        else:
            self.config = default_config


    def convert_to_graph(self, stream: str) -> Graph | None:
        try:

            data = json.load(stream)

            g = Graph()

            id_attr = self.config.get("id_attribute")
            ref_attr = self.config.get("ref_attribute")
            child_attr = self.config.get("children_attribute")

            self.__process(g, data, id_attr, ref_attr, child_attr)

            return g

        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError as e:
            print(e)

    def __process(self, g: Graph, data: dict, id_attr: str, ref_attr: str, child_attr: str):
        queue = collections.deque()

        if isinstance(data, list):
            for item in data:
                queue.append((item, None))
        else:
            queue.append((data, None))

        while queue:
            current, parent_id = queue.popleft()

            node_id = current.get(id_attr)
            ref_id = current.get(ref_attr)
            actual_id = node_id or ref_id

            if not actual_id:
                continue

            if actual_id not in g.nodes:
                node_data = {
                    key: value for key, value in current.items() if key not in [id_attr, ref_attr, child_attr]
                }
                g.add_node(Node(actual_id, **node_data))

            if parent_id:
                edge_id = f'{parent_id}->{actual_id}'
                g.add_edge(Edge(edge_id, parent_id, actual_id))

            children = current.get(child_attr)

            if isinstance(children, list):
                for child in children:
                    queue.append((child, actual_id))

    def name(self) -> str:
        return "json"

    def type(self) -> str:
        return "datasource"