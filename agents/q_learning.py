import numpy as np
import copy
from utils import findEmptyCells
from collections import namedtuple
import collections


class QLearning(object):
    def __init__(self):
        self.exp_rate = 1.0
        self.max_epsilon = 1.0
        self.min_epsilon = 0.1
        self.epsilon_decay_rate = 0.001
        self.gamma = 0.9
        self.lr = 0.2
        self.alpha = 0.5

        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i, j))
        self.Q = {}
        for action in self.actions:
            self.Q[action] = collections.defaultdict(int)
        self.rewards = []
        self.previous_state = None

    def choose(self, board,run):

        board_to_str = self.state_to_str(board)
        available_board_actions = list(findEmptyCells(board))

        if np.random.uniform(0, 1) < self.exp_rate:
            position = np.random.choice(len(available_board_actions))
            x, y = available_board_actions[position]
            action = (x, y)
        else:
            values = np.array([self.Q[a][board_to_str] for a in available_board_actions])
            best_position = np.argmax(values)
            action = available_board_actions[best_position]

        # self.eps *= (1. - self.eps_decay)
        self.exp_rate = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.epsilon_decay_rate * run)

        return action

    def update(self, current_state, previous_state, action, reward):
        """
        @param current_state:
        @param previous_state:
        @param action:
        @param reward:
        """
        if current_state is not None:  # not end game yet
            board_to_str = self.state_to_str(current_state)
            available_board_actions = list(findEmptyCells(current_state))
            Q_options = [self.Q[action][board_to_str] for action in available_board_actions]
            self.Q[action][previous_state] += self.alpha * (
                        reward + self.gamma * np.max(Q_options) - self.Q[action][previous_state])
        else:
            self.Q[action][previous_state] += self.alpha * (reward - self.Q[action][previous_state])

        self.rewards.append(reward)

    @staticmethod
    def state_to_str(board):
        return str(board)
