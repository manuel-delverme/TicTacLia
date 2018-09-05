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
    # for 'X' now
    # vertical matches
    if board [0][0] == "X" and board[1][0] == "X" and board[2][0] == "X":
        return 'X'
    if board[0][1] == "X" and board[1][1] == "X" and board[2][1] == "X":
        return 'X'
    if board[0][2] == "X" and board[1][2] == "X" and board[2][2] == "X":
        return 'X'
    # horizontal matches
    if board [0][0] == "X" and board[0][1] == "X" and board[0][2] == "X":
        return 'X'
    if board [1][0] == "X" and board[1][1] == "X" and board[1][2] == "X":
        return 'X'
    if board [2][0] == "X" and board[2][1] == "X" and board[2][1] == "X":
        return 'X'

    # for diagonal matches
    if board [0][0] == "X" and board[1][1] == "X" and board[2][2] == "X":
        return 'X'
    if board [0][2] == "X" and board[1][1] == "X" and board[2][0] == "X":
        return 'X'

    # for 'O' now
    # vertical matches
    if board[0][0] == "O" and board[1][0] == "O" and board[2][0] == "O":
        return 'X'
    if board[0][1] == "O" and board[1][1] == "O" and board[2][1] == "O":
        return 'X'
    if board[0][2] == "O" and board[1][2] == "O" and board[2][2] == "O":
        return 'X'

    # horizontal matches
    if board[0][0] == "O" and board[0][1] == "O" and board[0][2] == "O":
        return 'X'
    if board[1][0] == "O" and board[1][1] == "O" and board[1][2] == "O":
        return 'X'
    if board[2][0] == "O" and board[2][1] == "O" and board[2][1] == "O":
        return 'X'

    # for diagonal matches
    if board[0][0] == "O" and board[1][1] == "O" and board[2][2] == "O":
        return 'X'
    if board[0][2] == "O" and board[1][1] == "O" and board[2][0] == "O":
        return 'O'
    else:
        return None

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
