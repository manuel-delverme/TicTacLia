import random

def manu_s_agent(board):
    row = random.randint(0, 3)
    column = random.randint(0, 3)
    
    if board[row][column] != ' ':
        return manu_s_agent(board)
    return row, column


def lia_s_agent(board):
    row = random.randint(0, 3)
    column = random.randint(0, 3)
    if board[row][column] != ' ':
        return lia_s_agent(board)
    return row, column

def check_winner(board):
    # TODO: Lia's stuff
    return 'X'
    # return 'O'    
    # return None

board = [
[' ',' ',' ',],
[' ',' ',' ',],
[' ',' ',' ',],
]
# import numpy as np

nr_games_to_play = 3
for game_nr in range(nr_games_to_play):
    print("======= GAME nr {} STARTED =======".format(game_nr))
    turn = random.randint(0, 2)
    while True:
        print('turn', turn)
        if turn % 2 == 0:
            row, column = lia_s_agent(board)
            print('Lia picked', row, column)

            if board[row][column] != ' ':
                print('Lia cheated!')
                break
            board[row][column] = 'O'

        elif turn % 2 == 1:
            row, column = manu_s_agent(board)
            print('Manu picked', row, column)
            if board[row][column] != ' ':
                print('Manu cheated!')
                break
            board[row][column] = 'X'

        # end of the turn

        winner = check_winner(board)
        if winner == 'X':
            print("Manu wins a kiss from Lia")
            break
        elif winner == 'O':
            print("Lia wins ten kisses from Manu")
            break
        else:
            print("nobody won yet!")


        turn += 1

        for row in board:
            print(row)
        print()
