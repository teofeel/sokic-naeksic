from sokic.api.models import Node

from core.sokic.core.use_cases.Workspace import Workspace
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

    def execute(self, workspace: Workspace) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        node_id = str(self.args.data["id"])
        data = {key : value for key, value in self.args.data.items() if key != "id"}
        node = Node(node_id, **data)
        success = workspace.active_graph.add_node(node)
        if success:
            return f'SUCCESS - added node {node_id}'
        return f'ERROR - failed to add node {node_id}'

class UpdateNodeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "update-node"

    @property
    def required_args(self) -> list[str]:
        return ["id"]

    def execute(self, workspace) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        if len(self.args.data) < 2:
            return "ERROR - no attributes listed to update"
        node_id = str(self.args.data["id"])
        success = workspace.active_graph.update_node(node_id, **self.args.data)
        if success:
            return f'SUCCESS - updated node {self.args.data["id"]}'
        return f'ERROR - failed to update node {node_id}'

class RemoveNodeCommand(BaseCommand):
    def __init__(self, args: CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "remove-node"

    @property
    def required_args(self) -> list[str]:
        return ["id"]

    def execute(self, workspace) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"

        node_id = str(self.args.data["id"])
        success = workspace.active_graph.remove_node(node_id)
        if success:
            return f'SUCCESS - removed node {node_id}'
        return f'ERROR - failed to remove node {node_id}'