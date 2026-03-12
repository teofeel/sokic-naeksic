from core.sokic.core.use_cases.base_command import BaseCommand, CommandArguments


class SearchGraphCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "search"

    def required_args(self) -> list[str]:
        return []

    def execute(self, workspace) -> str:
        if not self.args.data or len(self.args.data) < 1:
            return "ERROR - must have at least one argument"
        query = ""
        for data in self.args.data:
            query += f"{data} "
        query.strip()
        workspace.set_search(query)
        return f'SUCCESS'


class FilterGraphCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "filter"

    def required_args(self) -> list[str]:
        return ["<attribute> <comparator> <value>"]

    def execute(self, workspace) -> str:
        if len(self.args.data) != 3:
            return "ERROR - expected following format: <attribute> <comparator> <value>"
        query = ""
        for data in self.args.data:
            query += f"{data} "
        query.strip()
        success = workspace.add_filter(query)
        if success:
            return f'SUCCESS - filtered graph'
        return f'ERROR - not filtered'

class DeleteGraphCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "delete-graph"

    def required_args(self) -> list[str]:
        return []

    def execute(self, workspace) -> str:
        workspace.active_graph.delete_graph()
        return f'SUCCESS - deleted graph'