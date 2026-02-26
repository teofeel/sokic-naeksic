from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod
    def name(self) -> str:
        """
        Used to get the name of the plugin
        :return:
        """
        pass

    @abstractmethod
    def type(self) -> str:
        """
        Used to get type of the plugin
        :return:
        """
        pass