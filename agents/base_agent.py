from abc import ABC, abstractmethod
from typing import Tuple


class Agent(ABC):
    @abstractmethod
    def choose(self, observation) -> Tuple[int, int]:
        raise NotImplemented
