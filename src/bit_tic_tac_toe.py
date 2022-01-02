# Reid Goodbar
# Tic Tac Toe using bit string to store and play, allows for single player and multi-player tic tac toe
# board is an int with each space being two bits, top left is the first two bits and the bottom right is the 17th and 18th bits
# move: flag for whose move it is, 1 for player 1 and 2 for player 2

import random

# game: plays the game, alternates back and forth between player 1 and player 2
def game():
    results = {}
    for i in range(1000):
        print("New Game")
        board = 0
        move = 1
        print_board(board)
        while not game_over(board):
            print("X Move") if move == 1 else print("O Move")
            if move == 1:
                board = input_move(board, move)
                # board = random_move(board, move)
                # board = computer_move(board, move)
            else:
                board = computer_move(board, move)
                # board = random_move(board, move)
                # board = input_move(board, move)
            move = move % 2 + 1
            print_board(board)
        winner_move = game_over(board)

        if winner_move in results:
            results[winner_move] += 1
        else:
            results[winner_move] = 1

        if winner_move == 3:
            print("Its a Tie")
        else:
            print("Winner is: ")
            print("X") if winner_move == 1 else print("O")
        print("--------------------------------------------")

    for key, value in results.items():
        print("% d : % d" % (key, value))


# input_move: takes in users move, determines if valid move
def input_move(board, move):
    inpt = int(input("Your Move: "))
    if inpt > 8 or inpt < 0 or (board >> (2 * inpt) & 3):
        print("illegal move")
        board = input_move(board, move)
    else:
        board = board | (move << 2 * inpt)
    return board


# random_move: computer performs a valid random move
def random_move(board, move):
    rndm = random.randint(0, 9)
    if rndm > 8 or rndm < 0 or (board >> (2 * rndm) & 3):
        board = random_move(board, move)
    else:
        board = board | (move << 2 * rndm)
    return board


searched = {}
# computer_move: computer finds best move to play
def computer_move(board, move):
    global searched
    computer_move_search(board, move)
    move_delta = -1
    winning_move = random_move(board, move)
    for i in searched:
        move_count = 0
        other_count = 0
        if move in searched[i]:
            move_count = searched[i][move]
        if move % 2 + 1 in searched[i]:
            other_count = searched[i][move % 2 + 1]
        if (move_count - other_count) > move_delta:
            move_delta = move_count - other_count
            winning_move = i
    print(searched)
    board = board | (move << 2 * winning_move)
    searched = {}
    return board


# computer_move_search: computer fills results array with all possible moves
def computer_move_search(board, move):
    for i in range(9):
        if (board >> i * 2 & 3) == 0:
            board = board | (move << 2 * i)
            game_res = game_over(board)
            global searched

            if i not in searched:
                searched[i] = {}

            if game_res not in [1, 2, 3]:
                computer_move_search(board, move % 2 + 1)
            else:
                sub_search = searched[i]
                if game_res in sub_search:
                    sub_search[game_res] += 1
                else:
                    sub_search[game_res] = 1


# print_board: prints the board from the bit string
def print_board(board):
    for i in range(0, 3):
        row_str = ""
        for j in range(0, 3):
            sq = board >> (6 * i + 2 * j) & 3
            if sq == 1:
                row_str += "X"
            elif sq == 2:
                row_str += "O"
            else:
                row_str += "-"
        print(row_str)


# check_rows: determines if any row is complete
def check_rows(board):
    for j in [1, 2]:
        for i in range(0, 3):
            if (
                ((board >> 6 * i & 3) == j)
                and ((board >> 2 + (6 * i) & 3) == j)
                and ((board >> 4 + (6 * i) & 3) == j)
            ):
                return j


# check_cols: determines if any col is complete
def check_cols(board):
    for j in [1, 2]:
        for i in range(0, 3):
            if (
                ((board >> 2 * i & 3) == j)
                and ((board >> 6 + (2 * i) & 3) == j)
                and ((board >> 12 + (2 * i) & 3) == j)
            ):
                return j


# check_diag: determines if any diag is complete:
def check_diag(board):
    for i in [1, 2]:
        if (
            ((board & 3) == i) and ((board >> 8 & 3) == i) and ((board >> 16 & 3) == i)
        ) or (
            ((board >> 4 & 3) == i)
            and ((board >> 8 & 3) == i)
            and ((board >> 12 & 3) == i)
        ):
            return i


# check_tie: determines if board is in tie state
def check_tie(board):
    for i in range(0, 9):
        if board >> 2 * i & 3 == 0:
            return None
    return 3


# game_over: determines if a bit string represents a game over
def game_over(board):
    return (
        check_rows(board) or check_cols(board) or check_diag(board) or check_tie(board)
    )


if __name__ == "__main__":
    game()
