import collections

from sokic.api.services.data_source_plugin import DataSourcePlugin
from sokic.api.models.graph import Graph
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


    def name(self) -> str:
        return "yaml"


    def type(self) -> str:
        return "datasource"


    def convert_to_graph(self, stream: str) -> Graph | None:
        """
        Method to convert yaml file to graph
        :param filepath: Full path to yaml file
        :return:
        """
        try:
            # update this not to read whole file, instead only file object
            data = yaml.safe_load(stream)

            g = Graph()

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
        queue = collections.deque()

        if isinstance(data, list):
            for item in data:
                queue.append((item, None))
        else:
            queue.append((data, None))

        while queue:
            current_data, parent_id = queue.popleft()

            node_id = current_data.get(id_attr)
            ref_id = current_data.get(ref_attr)
            actual_id = node_id or ref_id

            if not actual_id:
                continue

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
