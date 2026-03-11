from typing import Final, Sequence

from core.sokic.core.use_cases.base_command import BaseCommand, CommandArguments
from core.sokic.core.use_cases.edge_commands import AddEdgeCommand, UpdateEdgeCommand, RemoveEdgeCommand
from core.sokic.core.use_cases.graph_commands import FilterGraphCommand, SearchGraphCommand, DeleteGraphCommand
from core.sokic.core.use_cases.node_commands import AddNodeCommand, UpdateNodeCommand, RemoveNodeCommand


class CommandFactory:
    """
    Used for finding available commands and returning the corresponding instances
    Handles invalid command names as well
    """
    def __init__(self):
        self._available_commands: Final[Sequence[BaseCommand]] = (
            AddNodeCommand(),
            UpdateNodeCommand(),
            RemoveNodeCommand(),
            AddEdgeCommand(),
            UpdateEdgeCommand(),
            RemoveEdgeCommand(),
            FilterGraphCommand(),
            SearchGraphCommand(),
            DeleteGraphCommand()
        )

    def create_command(self, args: CommandArguments) -> BaseCommand:
        command = next(
            (cmd for cmd in self._available_commands if cmd.command_name == args.command_name),
            NotFoundCommand(args.command_name)
        )
        command.args = args
        return command

class NotFoundCommand(BaseCommand):
    def __init__(self, command_name: str) -> None:
        self._name = command_name

    @property
    def command_name(self) -> str:
        return self._name

    def execute(self) -> str:
        return f"ERROR - command not found: {self.command_name}"