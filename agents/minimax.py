from utils import findEmptyCells
from utils import get_opponent
from utils import check_winner
from copy import deepcopy
import functools
from agents.random import pick_random_move


@functools.lru_cache(100000)
def minimax(state, actions, player):  # minimax(state, actions, player = 'O')
    """heiristic algorithm to improve the winning ratio"""
    winner = check_winner(state)

    if winner:
        return (None, None), winner

    else:
        state = (list([list(row) for row in state]))
        draw_move = None
        # print("I am going to evaluate", actions)
        for action in actions:
            # print("Evaluated Action: ", action)
            newBoard = deepcopy(state)
            row = action[0]
            column = action[1]
            newBoard[row][column] = player  # insert 'O'

            # updates the empty_cells list and calls the function itself with the board as the newBoard
            _newBoard = (tuple([tuple(row) for row in newBoard]))
            newEmptyCells = findEmptyCells(_newBoard)
            # print("Who is the winner for?", newBoard)
            move, winner = minimax(_newBoard, newEmptyCells, get_opponent(player))
            # print("The winner is", winner)

            # output: who is going to win?
            # ----> 'O', 'X', DRAW
            if player == 'O':
                if winner == 'O':
                    # print("The winner is 'O'")
                    return (row, column), winner
                if winner == "It's a Draw":
                    draw_move = action

            if player == 'X':
                if winner == 'X':
                    return (row, column), winner

        output = pick_random_move(state)

        # TODO: BUG HERE! vvvv
        return output, winner
