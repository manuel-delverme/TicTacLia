"""Tic Tac Toe Game between two lovers: input()"""
import random
import argparse
import tqdm
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
# import pandas as pd
import os.path
import functools


def pick_random_move(board):
    row = random.randint(0, 2)
    column = random.randint(0, 2)

    if board[row][column] != ' ':
        return pick_random_move(board)
    return row, column

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
    # return pick_random_move(board)
    return pick_random_move(board)


def manu_input(board):
    print("Please chose a row index, between 0 and 2:")
    row = input() # must be 0, 1 or 2
    print("Please chose a column index, between 0 and 2:")
    column = input() # must be 0, 1, or 2
    if board[row][column] != ' ':
        return manu_input(board)
    return row, column


def opponent(player):
    """Returns the opposite sign played by the current agent"""
    if player == 'X':
        return 'O'
    return 'X'


@functools.lru_cache(100000)
def minimax(state, actions, player):  # minimax(state, actions, player = 'O')
    """heiristic algorithm to improve the winning ratio"""
    winner = check_winner(state)

    if winner != False:
        return (None, None), winner

    else:
        state = (list([list(row) for row in state]))
        draw_move = None
        for action in actions:
            newBoard = deepcopy(state)
            row = action[0]
            column = action[1]
            newBoard[row][column] = player # insert 'O'

            # updates the empty_cells list and calls the function itself with the board as the newBoard
            _newBoard = (tuple([tuple(row) for row in newBoard]))
            newEmptyCells = findEmptyCells(_newBoard)
            move, winner = minimax(_newBoard, newEmptyCells, opponent(player))

            # output: who is going to win?
            # ----> 'O', 'X', DRAW
            if winner == player:
                return (row, column), winner

            if winner == opponent(player):
                pass

            if winner is None:
                draw_move = (row, column)
        # if it's a draw
        # but let's improve it by finding the best move
        if draw_move is not None:
            return draw_move, None
        else:
            output = pick_random_move(state)
            return output, opponent(player)


@functools.lru_cache(10000)
def lia_s_agent(board):
    actions = findEmptyCells(board)

    if len(actions) == 9 and False:
        row = 1
        column = 1
        return row, column
    else:
        # # import ipdb; ipdb.set_trace()
        output = minimax(board, actions, player = 'O')
        return output[0]


def findEmptyCells(board):
    empty_cells = []  # count_freeSpace or depth
    for rowLoop in range(len(board)):
        for columnLoop in range(len(board[rowLoop])):
            if board[rowLoop][columnLoop] == ' ':
                empty_cells.append((rowLoop, columnLoop))
    return tuple(empty_cells)


@functools.lru_cache(10000)
def check_winner(board):
    # check for matches and winner
    for j in range(len(board)):
        # check rows matches
        if board[j][0] == "X":
            if (board[j][1] == "X") and (board[j][2] == "X"):
                return "X"
        if board[j][0] == "O":
            if (board[j][1] == "O") and (board[j][2] == "O"):
                return "O"

        # Check columns matches
        if board[0][j] == "X":
            if (board[1][j] == "X") and (board[2][j] == "X"):
                return "X"

        if board[0][j] == "O":
            if (board[1][j] == "O") and (board[2][j] == "O"):
                return "O"

        # Check Left Diagonal matches
        if board[0][0] == "X":
            if (board[1][1] == "X") and (board[2][2] == "X"):
                return "X"
        if board[0][0] == "O":
            if (board[1][1] == "O") and (board[2][2] == "O"):
                return "O"

        # Check Right Diagonal matches
        if board[0][2] == "X":
            if (board[1][1] == "X") and (board[2][0] == "X"):
                return "X"
        if board[0][2] == "O":
            if (board[1][1] == "O") and (board[2][0] == "O"):
                return "O"

        checkBoard = findEmptyCells(board)
        if len(checkBoard) == 0:
            return "It's a Draw"

        return False


def main(args=None):
    variances = []
    nr_games_to_play = [1000000, ] # try to get mean of same size like: [10,10,10,10,10], the winning ratio gets crazyly high
    for game_size in nr_games_to_play:
        samples = []
        for sample in range(5):
            varRatio = play_games(game_size, 0, args=args)
            samples.append(varRatio)
        variance = np.var(samples)
        variances.append(variance)
        mean = np.mean(samples)

        print("The mean is {} and the variance of {} games size is: {}".format (mean, game_size, variance))
    plt.loglog(nr_games_to_play, variances)
    if args is not None:
        plt.title("manu_is_drunk={}".format(args.manu_is_drunk))
    try:
        plt.show()
    except UserError:
        print('trying to save to file')
        plt.savefig("/tmp/variance.png")



def play_games(nr_games_to_play, gameShow=0, args=None, crash_on_cheat=True):
    # nr_games_to_play = [10, 100, 1000, 10000]
    leaderboard = {
        'Lia':0,
        'Manu': 0,
        'Draw': 0
    }

    # for game_nr in range(nr_games_to_play):
    for game_nr in tqdm.tqdm(range(nr_games_to_play)):
        if game_nr < gameShow:
            print("======= GAME nr {} STARTED =======".format(game_nr))
        who_plays = random.randint(0, 1)
        turn = 0
        board = [
            [' ', ' ', ' ', ],
            [' ', ' ', ' ', ],
            [' ', ' ', ' ', ],
        ]
        board_seq = []
        frozen_board = (tuple([tuple(row) for row in board]))
        while True:
            if game_nr < gameShow:
                print('turn', turn)

            if who_plays == 0:
                row, column = lia_s_agent(frozen_board)
                if game_nr < gameShow:
                    print('Lia picked',  row, column)

                if board[row][column] != ' ':
                    print('Lia cheated!')
                    break
                board[row][column] = 'O'
                who_plays = 1

            elif who_plays == 1:
                if args is not None and args.manu_is_drunk:
                    row, column = pick_random_move(frozen_board)
                else:
                    row, column = manu_s_agent(frozen_board)

                if game_nr < gameShow:
                    print('Manu picked', row, column)
                # this check if a new place is being overwritten
                if board[row][column] != ' ':
                    if crash_on_cheat:
                        print('Manu cheated!')
                        break
                    else:
                        board[0] = ['O', 'O', 'O']
                board[row][column] = 'X'
                who_plays = 0

            # end of the turn
            if game_nr < gameShow:
                for row in board:
                    print(row)
                print()
            turn += 1
            frozen_board = (tuple([tuple(row) for row in board]))
            board_seq.append(frozen_board)

            # checking who is the winner now
            winner = check_winner(frozen_board)
            if winner == 'X':
                # for idx, b in enumerate(board_seq):
                #     print(idx)
                #     for row in b:
                #         print(row)
                #     print()
                if game_nr < gameShow:
                    print("Manu wins a kiss from Lia")
                leaderboard['Manu'] += 1
                break
            elif winner == 'O':
                if game_nr < gameShow:
                    print("Lia wins ten kisses from Manu")
                leaderboard['Lia'] += 1
                break
            # check if game is draw, and exit loop
            elif winner == "It's a Draw":
                if game_nr < gameShow:
                    print("It's a Draw")
                leaderboard['Draw'] += 1
                break

    print(leaderboard)
    total_wins = float(leaderboard['Lia'] + leaderboard['Manu'])
    winningRatio = float(leaderboard['Lia'])/total_wins
    return winningRatio

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--manu_is_drunk', '-M', dest='manu_is_drunk', action='store_true', help='check whether manu should play randomly')
    args = parser.parse_args()
    main(args)
    print(args)
