from core.sokic.core.use_cases.base_command import BaseCommand, CommandArguments


class AddNodeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "add-node"

    @property
    def required_args(self) -> list[str]:
        return ["id"]

    def execute(self) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        node_id = self.args.data["id"]
        # TODO add the node to the corresponding graph
        return f'SUCCESS - added node {node_id}'

class UpdateNodeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "update-node"

    @property
    def required_args(self) -> list[str]:
        return ["id"]

    def execute(self) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        if len(self.args.data) < 2:
            return "ERROR - no attributes listed to update"
        node_id = self.args.data["id"]
        # TODO updating node logic
        return f'SUCCESS - updated node {self.args.data["id"]}'

class RemoveNodeCommand(BaseCommand):
    def __init__(self, args: CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "remove-node"

    @property
    def required_args(self) -> list[str]:
        return ["id"]

    def execute(self) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"

        node_id = self.args.data["id"]
        # TODO actually remove the node from the graph
        # TODO check if node can be removed without hindrance to edges
        return f'SUCCESS - removed node {node_id}'