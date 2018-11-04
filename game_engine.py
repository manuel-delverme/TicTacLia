import random
import tqdm
import utils


class TicTacToeGame(object):
    def __init__(self, args, crash_on_cheat=True):
        self.args = args
        self.crash_on_cheats = crash_on_cheat

    def play_games(
            self,
            nr_games_to_play,
            player1,
            player2,
            gameShow=0,
    ):
        leaderboard = {
            'Lia': 0,
            'Manu': 0,
            'Draw': 0
        }
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
                    row, column = player1(frozen_board)
                    if game_nr < gameShow:
                        print('Lia picked', row, column)

                    if board[row][column] != ' ':
                        print('Lia cheated!')
                        break
                    board[row][column] = 'O'
                    who_plays = 1

                elif who_plays == 1:
                    if self.args is not None and self.args.manu_is_drunk:
                        row, column = utils.pick_random_move(frozen_board)
                    else:
                        row, column = player2(frozen_board)

                    if game_nr < gameShow:
                        print('Manu picked', row, column)
                    # this check if a new place is being overwritten
                    if board[row][column] != ' ':
                        if self.crash_on_cheats:
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
                winner = utils.check_winner(frozen_board)
                if winner == 'X':
                    # for idx, b in enumerate(board_seq):
                    #     print(idx)
                    #     for row in b:
                    #         print(row)
                    #     print()
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
                elif winner == "It's a Draw":
                    if game_nr < gameShow:
                        print("It's a Draw")
                    leaderboard['Draw'] += 1
                    break

        print(leaderboard)
        total_wins = float(leaderboard['Lia'] + leaderboard['Manu'])
        winningRatio = float(leaderboard['Lia']) / total_wins
        return winningRatio

