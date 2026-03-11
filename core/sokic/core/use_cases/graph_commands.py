from core.sokic.core.use_cases.base_command import BaseCommand, CommandArguments


class SearchGraphCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "search"

    def execute(self) -> str:
        # TODO implement logic
        pass

class FilterGraphCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "filter"

    def execute(self) -> str:
        # TODO implement logic
        pass

class DeleteGraphCommand(BaseCommand):
    def __init__(self, args : CommandArguments = None) -> None:
        self.args = args

    @property
    def command_name(self) -> str:
        return "delete"

    def execute(self) -> str:
        # TODO implement logic
        pass