from abc import ABC, abstractmethod
from visitor.visitor import Visitor


class Node(ABC):

    @abstractmethod
    def accept(self, visitor: Visitor):
        pass
