"""Tic Tac Toe Game between two lovers: input()"""
import random
import argparse
import tqdm
import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd
import os.path

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
    return pick_random_move(board)


def manu_input(board):
    print("Please chose a row index, between 0 and 2:")
    row = input() # must be 0, 1 or 2
    print("Please chose a column index, between 0 and 2:")
    column = input() # must be 0, 1, or 2
    if board[row][column] != ' ':
        return manu_input(board)
    return row, column

def lia_s_agent(board):
    count_freeSpace = 0
    for rowLoop in range(len(board)):
        for columnLoop in range(len(board[rowLoop])):
            if board[rowLoop][columnLoop] == ' ':
                count_freeSpace += 1

    if count_freeSpace == 9:
        row = 1
        column = 1
        return row, column

    if count_freeSpace == 8:
        if board[0][1] == 'X' or board[1][0] == 'X' or board[1][2] == 'X' or board[2][1] == 'X':
            row = 1
            column = 1
            return row, column
        if board[1][1] == 'X':
            row = 0
            column = 0
            return row, column

    if count_freeSpace == 7:
        if board[1][1] == 'O':
            if board[0][1] == 'X' or board[1][0] == 'X' or board[1][2] == 'X' or board[2][1] == 'X':
                row = 0
                column = 0
                return row, column
            else:
                row = 1
                column = random.choice([0, 2])
                return row, column
        if board[1][1] == 'X':
            if board[0][0] != ' ':
                row = 0
                column = 1
                return row, column
            else:
                if board[0][2] != ' ':
                    row = 0
                    column = 1
                    return row, column
                else:
                    if board[2][2] != ' ':
                        row = 2
                        column = 1
                        return row, column
                    else:
                        if board[2][0] != ' ':
                            row = 1
                            column = 0
                            return row, column

    if count_freeSpace <= 6:
        return pick_random_move(board)
    return pick_random_move(board)

                # 6 free spaces left
                # if count_freeSpace == 6:
                #
                # if count_freeSpace == 5:
                #
                # if count_freeSpace == 4:
                #
                # if count_freeSpace == 3:
                #
                # if count_freeSpace == 2:
                #
                # if count_freeSpace == 1:

            # game ends

    # if board[row][column] != ' ':
    #     return lia_s_agent(board)
    #
    # return row, column



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
        return False


def main(args):
    variances = []
    nr_games_to_play = [10, 100, 1000, 10000]
    for game_size in nr_games_to_play:
        samples = []
        gameRatio = play_games(args, game_size, 0)
        for sample in range(5):
            varRatio = play_games(args, game_size, 0)
            samples.append(varRatio)
        variance = np.var(samples)
        variances.append(variance)

        print("The variance of {} games size is: {}".format (game_size, variance))
    plt.loglog(nr_games_to_play, variances)
    plt.title("manu_is_drunk={}".format(args.manu_is_drunk))
    try:
        plt.show()
    except UserError:
        print('trying to save to file')
        plt.savefig("/tmp/variance.png")



def play_games(args, nr_games_to_play, gameShow):
    # nr_games_to_play = [10, 100, 1000, 10000]
    leaderboard = {
        'Lia':0,
        'Manu': 0,
        'Draw': 0
    }

    for game_nr in  tqdm.tqdm(range(nr_games_to_play)):
        if game_nr < gameShow:
            print("======= GAME nr {} STARTED =======".format(game_nr))
        who_plays = random.randint(0, 1)
        turn = 0
        board = [
            [' ', ' ', ' ', ],
            [' ', ' ', ' ', ],
            [' ', ' ', ' ', ],
        ]
        while True:
            if game_nr < gameShow:
                print('turn', turn)

            if who_plays == 0:
                row, column = lia_s_agent(board)
                if game_nr < gameShow:
                    print('Lia picked',  row, column)

                if board[row][column] != ' ':
                    print('Lia cheated!')
                    break
                board[row][column] = 'O'
                who_plays = 1

            elif who_plays == 1:
                if args.manu_is_drunk:
                    row, column = pick_random_move(board)
                else:
                    row, column = manu_s_agent(board)

                if game_nr < gameShow:
                    print('Manu picked', row, column)
                # this check if a new place is being overwritten
                if board[row][column] != ' ':
                    print('Manu cheated!')
                    break
                board[row][column] = 'X'
                who_plays = 0

            # end of the turn
            if game_nr < gameShow:
                for row in board:
                    print(row)
                print()
            turn += 1

            # checking who is the winner now
            winner = check_winner(board)
            if winner == 'X':
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
            else:
                if turn == 9:
                    if game_nr < gameShow:
                        print("It's a Draw")
                    leaderboard['Draw'] += 1
                    break

    total_wins = float(leaderboard['Lia'] + leaderboard['Manu'])
    winningRatio = float(leaderboard['Lia'])/total_wins
    return winningRatio

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--manu_is_drunk', '-M', dest='manu_is_drunk', action='store_true', help='check whether manu should play randomly')
    args = parser.parse_args()
    main(args)
    print(args)
