from sokic.api.models import Edge

from core.sokic.core.use_cases.base_command import BaseCommand, CommandArguments


class AddEdgeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "add-edge"

    @property
    def required_args(self) -> list[str]:
        return ["id", "source", "target"]

    def execute(self, workspace) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        edge_id = str(self.args.data["id"])
        source = str(self.args.data["source"])
        target = str(self.args.data["target"])
        data = {key: val for key, val in self.args.data.items() if key not in ["id", "source", "target"]}
        edge = Edge(edge_id, source, target, **data)
        success = workspace.active_graph.add_edge(edge)
        if success:
            return f'SUCCESS - added edge {edge_id}'
        return f'ERROR - failed to add edge {edge_id}'

class UpdateEdgeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "update-edge"

    @property
    def required_args(self) -> list[str]:
        return ["id"]

    def execute(self, workspace) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        edge_id = str(self.args.data["id"])
        success = workspace.active_graph.update_edge(edge_id, **self.args.data)
        if success:
            return f'SUCCESS - updated node {edge_id}'
        return f'ERROR - failed to update edge {edge_id}'

class RemoveEdgeCommand(BaseCommand):
    def __init__(self, args: CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "remove-edge"

    @property
    def required_args(self) -> list[str]:
        return ["id"]

    def execute(self, workspace) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        edge_id = str(self.args.data["id"])
        success = workspace.active_graph.remove_edge(edge_id)
        if success:
            return f'SUCCESS - removed edge {edge_id}'
        return f'ERROR - failed to remove edge {edge_id}'