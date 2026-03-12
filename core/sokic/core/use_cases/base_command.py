from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Dict, Any

from core.sokic.core.use_cases.Workspace import Workspace


@dataclass
class CommandArguments:
    command_name: str
    data : Dict[str, Any]

class BaseCommand(ABC):
    @property
    @abstractmethod
    def command_name(self) -> str:
        pass

    @property
    @abstractmethod
    def required_args(self) -> list[str]:
        return []

    @abstractmethod
    def execute(self, active_workspace: Workspace) -> str:
        pass