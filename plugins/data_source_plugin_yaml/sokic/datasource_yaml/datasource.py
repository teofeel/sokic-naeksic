from collections import deque

from sokic.api.services.DataSourcePlugin import DataSourcePlugin
from sokic.api.models.graph import Graph
from sokic.api.models.graph_direction import GraphDirection
from sokic.api.models.graph_cycle import GraphCycle
from sokic.api.models.node import Node
from sokic.api.models.edge import Edge
import yaml


class YamlDataSource(DataSourcePlugin):
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


    def convert_to_graph(self, filepath: str) -> Graph | None:
        """
        Method to convert yaml file to graph
        :param filepath: Full path to yaml file
        :return:
        """
        try:
            with open(filepath, "r", encoding="utf-8") as stream:
                data = yaml.safe_load(stream)

            direction = GraphDirection.DIRECTED if self._is_directed(data) else GraphDirection.UNDIRECTED
            cycle_policy = GraphCycle.CYCLIC if self._is_cyclic(data) else GraphCycle.ACYCLIC

            g = Graph(direction=direction, cycle_policy=cycle_policy)

            id_attr = self.config.get("id_attribute")
            ref_attr = self.config.get("ref_attribute")
            child_attr = self.config.get("children_attribute")

            self.__process(g, data, id_attr, ref_attr, child_attr)

            return g

        except FileNotFoundError:
            print("File not found")
        except yaml.YAMLError as exc:
            print(exc)


    def __process(self, g: Graph, data: dict, id_attr="@id", ref_attr="@ref", child_attr="children") -> None:
        """
        Recursively process the data
        :param g:
        :param data:
        :param parent_id:
        :param id_attr:
        :param ref_attr:
        :param child_attr:
        :return:
        """
        queue = deque([(data, None)])

        while queue:
            current_data, parent_id = queue.popleft()

            node_id = current_data.get(id_attr)
            ref_id = current_data.get(ref_attr)
            actual_id = node_id or ref_id

            if not actual_id:
                return

            if actual_id not in g.nodes:
                node_data = {
                    key: val for key,val in current_data.items() if key not in [id_attr, ref_attr, child_attr]
                }

                g.add_node(Node(actual_id, **node_data))

            if parent_id:
                edge_id = f'{parent_id}->{actual_id}'
                g.add_edge(Edge(edge_id, parent_id, actual_id))

            children = current_data.get(child_attr)

            if isinstance(children, list):
                for child in children:
                    queue.append((child, actual_id))


    def _is_cyclic(self, data: dict) -> bool:
        """
        Check if data is a cyclic or acyclic graph
        :param data:
        :return:
        """
        ref_attr = self.config.get("ref_attribute")
        queue = deque([data])

        while queue:
            item = queue.popleft()

            if isinstance(item, dict):
                if ref_attr in item:
                    return True

                for value in item.values():
                    queue.append(value)

            elif isinstance(item, list):
                for value in item:
                    queue.append(value)

        return False


    def _is_directed(self, data: dict) -> bool:
        """
        Check if data is a directed graph\n
        Looks for field in .yaml file which determines if directed or undirected
        :param data:
        :return:
        """
        value = data.get("direction")

        if not value:
            return True

        if isinstance(value, str):
            return True if value.upper() == "DIRECTED" else False

        return True
