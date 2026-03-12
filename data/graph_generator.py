import json
import yaml
import random
from pathlib import Path

TOPICS = {
    "1": {
        "name": "Org Chart",
        "prefix": "employee",
        "attributes": {
            "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi"],
            "title": ["Director", "Manager", "Senior Dev", "Junior Dev", "Analyst", "Designer"],
            "department": ["Engineering", "HR", "Marketing", "Sales", "Finance"],
            "performance_rating": [1, 2, 3, 4, 5]
        }
    },
    "2": {
        "name": "File System",
        "prefix": "node",
        "attributes": {
            "name": ["system", "bin", "user", "documents", "config.yaml", "script.py", "data.csv", "backup.tar.gz"],
            "type": ["directory", "file", "archive", "executable"],
            "permissions": ["rwxr-xr-x", "rw-r--r--", "rwx------", "r--r--r--"],
            "size_mb": [0, 1, 15, 120, 500, 1024]
        }
    },
    "3": {
        "name": "Computer Network",
        "prefix": "device",
        "attributes": {
            "hostname": ["gateway-01", "switch-core", "db-node", "web-server", "load-balancer", "firewall"],
            "device_type": ["Router", "Switch", "Server", "Firewall", "Access Point"],
            "status": ["online", "offline", "maintenance", "degraded"],
            "vlan": [10, 20, 30, 100, 999]
        }
    }
}


class GenericGraphGenerator:
    def __init__(self, topic_config, target_nodes=200):
        self.config = topic_config
        self.target_nodes = target_nodes
        self.existing_ids = []
        self.id_counter = 1

    def generate_id(self):
        node_id = f"{self.config['prefix']}_{self.id_counter}"
        self.id_counter += 1
        return node_id

    def _create_single_node(self):
        node_id = self.generate_id()
        self.existing_ids.append(node_id)
        node = {"@id": node_id}

        for attr_key, attr_values in self.config["attributes"].items():
            if random.random() < 0.8:
                node[attr_key] = random.choice(attr_values)

        first_attr_key = list(self.config["attributes"].keys())[0]
        if first_attr_key not in node:
            node[first_attr_key] = random.choice(self.config["attributes"][first_attr_key])

        return node

    def generate(self):

        root = self._create_single_node()

        available_parents = [root]

        while self.id_counter <= self.target_nodes:

            parent = random.choice(available_parents)

            if "children" not in parent:
                parent["children"] = []

            if len(self.existing_ids) > 1 and random.random() < 0.15:
                ref_node = {"@ref": random.choice(self.existing_ids)}
                parent["children"].append(ref_node)
            else:
                new_node = self._create_single_node()
                parent["children"].append(new_node)

                available_parents.append(new_node)

        return root


if __name__ == "__main__":
    print("Select a topic to generate data for:")
    for key, topic in TOPICS.items():
        print(f"{key}. {topic['name']}")

    choice = input("Choice: ")

    num_nodes = int(input("Enter number of desired nodes: "))


    if choice in TOPICS:
        selected_topic = TOPICS[choice]

        generator = GenericGraphGenerator(selected_topic, target_nodes=num_nodes)
        random_graph = generator.generate()

        yaml_output = yaml.dump(random_graph, sort_keys=False, allow_unicode=True, default_flow_style=False)

        rand_num = random.randint(1, 50000)

        dir_path = Path(f"./{selected_topic['name']}")
        dir_path.mkdir(parents=True, exist_ok=True)

        yaml_filename = dir_path / f"test_{rand_num}.yaml"
        with open(yaml_filename, "w") as f:
            f.write(yaml_output)

        json_output = json.dumps(random_graph, indent=2, ensure_ascii=False)
        json_filename = dir_path / f"test_{rand_num}.json"
        with open(json_filename, "w") as f:
            f.write(json_output)
