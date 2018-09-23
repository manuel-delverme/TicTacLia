"""Tic Tac Toe Game between two lovers: input()"""
import random

def manu_s_agent(board):
    row = random.randint(0, 2)
    column = random.randint(0, 2)
    if board[row][column] != ' ':
        return manu_s_agent(board)
    return row, column


def manu_input(board):
    print("Please chose a row index, between 0 and 2:")
    row = input() # must be 0, 1 or 2
    print("Please chose a column index, between 0 and 2:")
    column = input() # must be 0, 1, or 2
    if board[row][column] != ' ':
        return manu_input(board)
    return row, column

def lia_s_agent(board):

    # row = random.randint(0, 2)
    # column = random.randint(0, 2)
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
                row = random.randint(0, 2)
                column = random.randint(0, 2)
                return row, column

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


nr_games_to_play = 10000
leaderboard = {
    'Lia':0,
    'Manu': 0,
    'Draw': 0
}

for game_nr in range(nr_games_to_play):
    if game_nr < 100:
        print("======= GAME nr {} STARTED =======".format(game_nr))
    who_plays = random.randint(0, 1)
    turn = 0
    board = [
        [' ', ' ', ' ', ],
        [' ', ' ', ' ', ],
        [' ', ' ', ' ', ],
    ]
    while True:
        if game_nr < 100:
            print('turn', turn)
        if who_plays == 0:
            row, column = lia_s_agent(board)
            if game_nr < 100:
                print('Lia picked',  row, column)

            # if board[row][column] != ' ':
            #     print('Lia cheated!')
            #     break
            board[row][column] = 'O'
            who_plays = 1

        elif who_plays == 1:
            row, column = manu_s_agent(board)
            if game_nr < 100:
                print('Manu picked', row, column)

            # this check if a new place is being overwritten
            # if board[row][column] != ' ':
            #     print('Manu cheated!')
            #     break
            board[row][column] = 'X'
            who_plays = 0

        # end of the turn
        if game_nr < 100:
            for row in board:
                print(row)
            print()
        turn += 1

        # checking who is the winner now
        winner = check_winner(board)
        if winner == 'X':
            if game_nr < 100:
                print("Manu wins a kiss from Lia")
            leaderboard['Manu'] += 1
            break
        elif winner == 'O':
            if game_nr < 100:
                print("Lia wins ten kisses from Manu")
            leaderboard['Lia'] += 1
            break
        # check if game is draw, and exit loop
        else:
            if turn == 9:
                if game_nr < 100:
                    print("It's a Draw")
                leaderboard['Draw'] += 1
                break

total_wins = float(leaderboard['Lia'] + leaderboard['Manu'])
print("winning ratio", float(leaderboard['Lia'])/total_wins, leaderboard)
