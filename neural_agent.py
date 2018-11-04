from typing import Tuple

from agents.base_agent import Agent


class NeuralAgent(Agent):
    def __init__(self):
        self.model = ...

    def training(self, dataset):
        ...

    def choose(self, observation) -> Tuple[int, int]:
        row, column = ..., ...
        return row, column
