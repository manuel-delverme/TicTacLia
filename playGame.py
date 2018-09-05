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


board = [
[' ',' ',' ',],
[' ',' ',' ',],
[' ',' ',' ',],
]
# import numpy as np

turn = random.randint(0, 2)
print("======= GAME STARTED =======")
for _ in range(9):
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
    elif winner == 'O':
        print("Lia wins ten kisses from Manu")
    else:
        print("nobody won yet!")

    
    turn += 1
    
    for row in board:
        print(row)
    print()
