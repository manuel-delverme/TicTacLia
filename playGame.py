"""Tic Tac Toe Game between two lovers: Manu and Lia"""


import random

# def choose_indexBoard(row, column, board):
#     """Choose where to mark the board
#     for when we will play it ourlself"""
#    return None




def manu_s_agent(board):
    row = random.randint(0, 2)
    column = random.randint(0, 2)
    if board[row][column] != ' ':
        return manu_s_agent(board)
    return row, column


def lia_s_agent(board):
    row = random.randint(0, 2)
    column = random.randint(0, 2)
    if board[row][column] != ' ':
        return lia_s_agent(board)
    return row, column


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


nr_games_to_play = 3
for game_nr in range(nr_games_to_play):
    print("======= GAME nr {} STARTED =======".format(game_nr))
    turn = random.randint(0, 2)
    board = [
        [' ', ' ', ' ', ],
        [' ', ' ', ' ', ],
        [' ', ' ', ' ', ],
    ]

    while True:
        print('turn', turn)
        if turn % 2 == 0:
            row, column = lia_s_agent(board)
            print('Lia picked',  row, column)

            # not sure what this does
            if board[row][column] != ' ':
                print('Lia cheated!')
                break
            board[row][column] = 'O'

        elif turn % 2 == 1:
            row, column = manu_s_agent(board)
            print('Manu picked', row, column)
            # not sure what this does
            if board[row][column] != ' ':
                print('Manu cheated!')
                break
            board[row][column] = 'X'
        # end of the turn

        # checking who is the winner now
        winner = check_winner(board)
        if winner == 'X':
            print("Manu wins a kiss from Lia")
            break
        elif winner == 'O':
            print("Lia wins ten kisses from Manu")
            break
        # check if game is a draw, and exit loop
        else:
            if turn == 9:
                print("It's a Draw")
                break

        turn += 1

        for row in board:
            print(row)
        print()
