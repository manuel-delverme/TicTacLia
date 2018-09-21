import playGame
import itertools
import tqdm

def wound_i_win(board, row, column):
    if board[row][column] != ' ':
        return False

    board[row][column] = 'O'
    answer = playGame.check_winner(board)
    board[row][column] = ' '
    return answer

def choose_move(board):
    for row in range(3):
        for column in range(3):
            if wound_i_win(board, row, column):
                return row, column
    return -1

def main():
    # import ipdb; ipdb.set_trace()
    policy = {}
    boards = itertools.product(' XO', repeat=9)
    for board_string in tqdm.tqdm(boards):
        if ' ' not in board_string:
            continue

        board = [list(board_string[:3]), list(board_string[3:6]), list(board_string[6:])]
        if playGame.check_winner(board) != False:
            continue

        n_x = board_string.count('X')
        n_o = board_string.count('O')
        if n_x - n_o not in (0, 1):
            continue

        policy[''.join(board_string)] = choose_move(board)
        # print(''.join(board_string))

    with open('policy.txt', 'w') as fout:
        for k,v in policy.items():
            fout.write(str(k) + ":" + str(v) + "\n")

if __name__ == "__main__":
    main()
