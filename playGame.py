"""Tic Tac Toe Game between two lovers: input()"""
import argparse
import functools
import os.path
import random

import matplotlib.pyplot as plt
import numpy as np
import tqdm
from duplicity.errors import UserError

from agents.minimax import minimax
from agents.q_learning import QLearning
from agents.random import pick_random_move
from utils import check_winner
from utils import findEmptyCells
from utils import who_is_the_winner

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

    return pick_random_move(board)


@functools.lru_cache(10000)
def lia_s_agent(board):
    actions = findEmptyCells(board)

    if len(actions) == 9 and False:
        row = 1
        column = 1
        return row, column
    else:
        output = minimax(board, actions, player='O')
        return output[0]


def main(args=None):
    variances = []
    nr_games_to_play = [
        100000, ]  # try to get mean of same size like: [10,10,10,10,10], the winning ratio gets crazyly high
    for game_size in nr_games_to_play:
        samples = []
        for sample in range(5):
            var_ratio = play_games(game_size, 0, args=args)
            samples.append(var_ratio)
        variance = np.var(samples)
        variances.append(variance)
        mean = np.mean(samples)

        print("The mean is {} and the variance of {} games size is: {}".format(mean, game_size, variance))
    plt.loglog(nr_games_to_play, variances)
    plt.title("manu_policy={}".format(args.manu_policy))
    try:
        plt.show()
    except UserError:
        print('trying to save to file')
        plt.savefig("/tmp/variance.png")


def play_games(nr_games_to_play, gameShow=0, args=None, crash_on_cheat=True):
    if args.manu_policy == "qlearning":
        q_learning = QLearning()
        previous_state = None

    # nr_games_to_play = [10, 100, 1000, 10000]
    leaderboard = {
        'Lia': 0,
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
                    print('Lia picked', row, column)

                if board[row][column] != ' ':
                    print('Lia cheated!')
                    break
                board[row][column] = 'O'
                who_plays = 1

            elif who_plays == 1:
                if args.manu_policy == "random":
                    row, column = pick_random_move(frozen_board)
                elif args.manu_policy == "not_drunk":
                    row, column = manu_s_agent(frozen_board)
                elif args.manu_policy == "qlearning":
                    previous_state = frozen_board
                    row, column = q_learning.choose(frozen_board,game_nr)

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

            if winner:
                name = who_is_the_winner(winner, game_nr, gameShow)
                leaderboard[name] += 1
                if args.manu_policy == "qlearning":
                    reward = 0 if name == "Draw" else 1 if name == "Manu" else -1
                    current_state = None
                    q_learning.update(current_state,previous_state, (row,column),reward)
                break
            else:
                if args.manu_policy == "qlearning":
                    reward = 0
                    q_learning.update(frozen_board,previous_state, (row,column),reward)


    print(leaderboard)
    total_wins = float(leaderboard['Lia'] + leaderboard['Manu'])
    winning_ratio = float(leaderboard['Lia']) / total_wins
    return winning_ratio


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manu-policy", default="qlearning", choices=["not_drunk", "qlearning", "random"],
                        help="chose Manu policy")

    args = parser.parse_args()
    main(args)
    print(args)
