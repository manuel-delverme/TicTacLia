import random
import functools


def pick_random_move(board):
    row = random.randint(0, 2)
    column = random.randint(0, 2)

    if board[row][column] != ' ':
        return pick_random_move(board)
    return row, column


def manu_input(board):
    print("Please chose a row index, between 0 and 2:")
    row = input()  # must be 0, 1 or 2
    print("Please chose a column index, between 0 and 2:")
    column = input()  # must be 0, 1, or 2
    if board[row][column] != ' ':
        return manu_input(board)
    return row, column


def get_opponent(player):
    """Returns the opposite sign playes by the current agent"""
    if player == 'X':
        return 'O'
    return 'X'


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


def who_is_the_winner(winner, game_nr, gameShow):
    if winner == 'X':
        if game_nr < gameShow:
            print("Manu wins ten kiss from Lia")
        return 'Manu'
    elif winner == 'O':
        if game_nr < gameShow:
            print("Lia wins ten kisses from Manu")
        return 'Lia'
    # check if game is draw, and exit loop
    elif winner == "It's a Draw":
        if game_nr < gameShow:
            print("It's a Draw")
        return 'Draw'
