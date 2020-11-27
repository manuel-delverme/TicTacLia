import random


def pick_random_move(board):
    row = random.randint(0, 2)
    column = random.randint(0, 2)

    if board[row][column] != ' ':
        return pick_random_move(board)
    return row, column
