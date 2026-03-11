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

    def execute(self) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        edge_id = self.args.data["id"]
        # TODO add edge to corresponding graph
        return f'SUCCESS - added edge {edge_id}'

class UpdateEdgeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "update-edge"

    @property
    def required_args(self) -> list[str]:
        return ["id"]

    def execute(self) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        edge_id = self.args.data["id"]
        # TODO updating edge logic
        return f'SUCCESS - updated node {edge_id}'

class RemoveEdgeCommand(BaseCommand):
    def __init__(self, args: CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "remove-edge"

    @property
    def required_args(self) -> list[str]:
        return ["id"]

    def execute(self) -> str:
        missing = [arg for arg in self.required_args if arg not in self.args.data]
        if missing:
            return f"ERROR - missing required: {', '.join(missing)}"
        edge_id = self.args.data["id"]
        # TODO remove edge from corresponding graph
        return f'SUCCESS - removed node {edge_id}'