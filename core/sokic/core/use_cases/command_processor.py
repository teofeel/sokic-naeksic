from core.sokic.core.use_cases.Workspace import Workspace
from core.sokic.core.use_cases.base_command import CommandArguments
from core.sokic.core.use_cases.command_factory import CommandFactory


class CommandProcessor:
    """
    Processes arguments and parses them into CommandArguments
    Processes command name and instantiates the corresponding command
    Executes command
    """
    def __init__(self) -> None:
        self._commandFactory = CommandFactory()

    def process_command(self, command_str: str, active_workspace: Workspace) -> str:
        command_args = self.parse_arguments(command_str)
        command = self._commandFactory.create_command(command_args)
        return command.execute(active_workspace)


    def parse_arguments(self, command: str):
        parts = command.split()
        if not parts:
            return CommandArguments(command_name="", data={})

        command_name = parts[0]
        data = {}

        for item in parts[1:]:
            if command_name == "filter" or command_name == "search":
                data[item] = item
            elif "=" in item:
                key, value = item.split("=", 1)
                data[key] = self._convert_type(value)

        return CommandArguments(command_name=command_name, data=data)


    def _convert_type(self, value: str):
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value
