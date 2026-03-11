from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CommandArguments:
    command_name: str
    data : Dict[str, Any]

class BaseCommand(ABC):
    @property
    @abstractmethod
    def command_name(self) -> str:
        pass

    @abstractmethod
    def execute(self) -> str:
        pass