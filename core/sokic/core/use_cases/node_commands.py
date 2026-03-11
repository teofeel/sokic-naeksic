from core.sokic.core.use_cases.base_command import BaseCommand, CommandArguments


class AddNodeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "add-node"

    def execute(self) -> str:
        if not self.args.data:
            return "ERROR - no arguments provided"
        if "id" not in self.args.data:
            return "ERROR - no id provided"
        node_id = self.args.data["id"]
        # TODO add the node to the corresponding graph
        return f'SUCCESS - added node {node_id}'

class UpdateNodeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "update-node"

    def execute(self) -> str:
        if not self.args.data:
            return "ERROR - no arguments provided"
        if "id" not in self.args.data or len(self.args.data) < 2:
            return "ERROR - no required arguments provided"
        node_id = self.args.data["id"]
        # TODO updating node logic
        return f'SUCCESS - updated node {self.args.data["id"]}'

class RemoveNodeCommand(BaseCommand):
    def __init__(self, args: CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "remove-node"

    def execute(self) -> str:
        if not self.args.data:
            return "ERROR - no arguments provided"
        if "id" not in self.args.data:
            return "ERROR - no id provided"
        node_id = self.args.data["id"]
        # TODO actually remove the node from the graph
        # TODO check if node can be removed without hindrance to edges
        return f'SUCCESS - removed node {node_id}'