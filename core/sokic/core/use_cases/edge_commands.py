from core.sokic.core.use_cases.base_command import BaseCommand, CommandArguments


class AddEdgeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "add-edge"

    def execute(self) -> str:
        if not self.args.data or len(self.args.data) < 3:
            return "ERROR - not enough arguments provided"
        if "id" not in self.args.data or "source" not in self.args.data or "target" not in self.args.data:
            return "ERROR - required arguments are missing"
        edge_id = self.args.data["id"]
        # TODO add edge to corresponding graph
        return f'SUCCESS - added edge {edge_id}'

class UpdateEdgeCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "update-edge"

    def execute(self) -> str:
        if not self.args.data:
            return "ERROR - no arguments provided"
        if "id" not in self.args.data or len(self.args.data) < 2:
            return "ERROR - required arguments are missing"
        edge_id = self.args.data["id"]
        # TODO updating edge logic
        return f'SUCCESS - updated node {edge_id}'

class RemoveEdgeCommand(BaseCommand):
    def __init__(self, args: CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "remove-edge"

    def execute(self) -> str:
        if not self.args.data:
            return "ERROR - no arguments provided"
        if "id" not in self.args.data:
            return "ERROR - no id provided"
        edge_id = self.args.data["id"]
        # TODO remove edge from corresponding graph
        return f'SUCCESS - removed node {edge_id}'