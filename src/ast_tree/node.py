from abc import ABC, abstractmethod
from src.visitor.visitor import Visitor


class Node(ABC):

    @abstractmethod
    def accept(self, visitor: Visitor):
        pass
