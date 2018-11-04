"""Tic Tac Toe Game between two lovers: input()"""
import argparse
from copy import deepcopy
import os.path
import functools
import utils
import game_engine

manu_policy = {}


def manu_s_agent(board):
    board_string = ''.join([item for sublist in board for item in sublist])
    if not os.path.isfile('manu_policy.txt'):
        import generate_manu_policy
        generate_manu_policy.main()

    if len(manu_policy) == 0:
        with open('manu_policy.txt') as fin:
            for row in fin:
                state, action = row[:-1].split(':')
                if action != '-1':
                    manu_policy[state] = [int(a) for a in action[1:-1].split(',')]

    if board_string in manu_policy:
        return manu_policy[board_string]
    return utils.pick_random_move(board)


@functools.lru_cache(100000)
def minimax(state, actions, player):  # minimax(state, actions, player = 'O')
    """heiristic algorithm to improve the winning ratio"""
    winner = utils.check_winner(state)

    if winner:
        return (None, None), winner

    else:
        state = (list([list(row) for row in state]))
        for action in actions:
            newBoard = deepcopy(state)
            row = action[0]
            column = action[1]
            newBoard[row][column] = player  # insert 'O'

            # updates the empty_cells list and calls the function itself with the board as the newBoard
            _newBoard = (tuple([tuple(row) for row in newBoard]))
            newEmptyCells = utils.findEmptyCells(_newBoard)
            move, winner = minimax(_newBoard, newEmptyCells, utils.get_opponent(player))

            # output: who is going to win?
            # ----> 'O', 'X', DRAW
            if player == 'O':
                if winner == 'O':
                    # print("The winner is 'O'")
                    return (row, column), winner
            if player == 'X':
                if winner == 'X':
                    return (row, column), winner

        output = utils.pick_random_move(state)

        # TODO: BUG HERE! vvvv
        return output, winner


@functools.lru_cache(10000)
def lia_s_agent(board):
    actions = utils.findEmptyCells(board)

    if len(actions) == 9 and False:
        row = 1
        column = 1
        return row, column
    else:
        output = minimax(board, actions, player='O')
        return output[0]


def main(args=None):
    game = game_engine.TicTacToeGame(
        args=args,
    )

    nr_games_to_play = 10000
    lia_s_winning_ratio = game.play_games(
        nr_games_to_play,
        player1=lia_s_agent,
        player2=manu_s_agent,
    )
    print("Lia's winning ratio is :", lia_s_winning_ratio)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--manu_is_drunk', '-M', dest='manu_is_drunk', action='store_true',
                        help='check whether manu should play randomly')
    args = parser.parse_args()
    main(args)
    print(args)
