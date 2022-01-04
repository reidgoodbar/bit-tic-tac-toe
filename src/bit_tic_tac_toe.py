"""
    Reid Goodbar

    Tic Tac Toe using bit string to store and play, allows for single
    player and multi-player tic tac toe, board is an int with each space
    being two bits, top left is the first two bits and the bottom right
    is the 17th and 18th bits
    move: flag for whose move it is, 1 for player 1 and 2 for player 2
"""

import random


def game():
    """
        game: plays the game, alternates back and forth between player 1 and player 2
    """
    results = {}
    for _ in range(1000):
        print("New Game")
        board = 0
        move = 1
        print_board(board)
        while not game_over(board):
            if move == 1:
                print("X Move")
                board = input_move(board, move)
                # board = random_move(board, move)
                # board = computer_move(board, move)
            else:
                print("O Move")
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
            if winner_move == 1:
                print("X")
            else:
                print("O")
        print("--------------------------------------------")

    for key, value in results.items():
        print("% d : % d" % (key, value))


def input_move(board, move):
    """
        input_move: takes in users move, determines if valid move
    """
    inpt = int(input("Your Move: "))
    if inpt > 8 or inpt < 0 or (board >> (2 * inpt) & 3):
        print("illegal move")
        board = input_move(board, move)
    else:
        board = board | (move << 2 * inpt)
    return board


def random_move(board, move):
    """
        random_move: computer performs a valid random move
    """
    rndm = random.randint(0, 9)
    if rndm > 8 or rndm < 0 or (board >> (2 * rndm) & 3):
        board = random_move(board, move)
    else:
        board = board | (move << 2 * rndm)
    return board


def computer_move(board, move):
    """
        computer_move: computer finds best move to play
    """
    searched = {}
    computer_move_search(board, move, searched)
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


def computer_move_search(board, move, searched):
    """
        computer_move_search: computer fills results array with all possible moves
    """
    for i in range(9):
        if (board >> i * 2 & 3) == 0:
            board = board | (move << 2 * i)
            game_res = game_over(board)

            if i not in searched:
                searched[i] = {}

            if game_res not in [1, 2, 3]:
                computer_move_search(board, move % 2 + 1, searched)
            else:
                sub_search = searched[i]
                if game_res in sub_search:
                    sub_search[game_res] += 1
                else:
                    sub_search[game_res] = 1


def print_board(board):
    """
        print_board: prints the board from the bit string
    """
    for i in range(0, 3):
        row_str = ""
        for j in range(0, 3):
            square = board >> (6 * i + 2 * j) & 3
            if square == 1:
                row_str += "X"
            elif square == 2:
                row_str += "O"
            else:
                row_str += "-"
        print(row_str)


def check_rows(board):
    """
        check_rows: determines if any row is complete
    """
    for j in [1, 2]:
        for i in range(0, 3):
            if (
                ((board >> 6 * i & 3) == j)
                and ((board >> 2 + (6 * i) & 3) == j)
                and ((board >> 4 + (6 * i) & 3) == j)
            ):
                return j
    return None


def check_cols(board):
    """
        check_cols: determines if any col is complete
    """
    for j in [1, 2]:
        for i in range(0, 3):
            if (
                ((board >> 2 * i & 3) == j)
                and ((board >> 6 + (2 * i) & 3) == j)
                and ((board >> 12 + (2 * i) & 3) == j)
            ):
                return j
    return None


def check_diag(board):
    """
        check_diag: determines if any diag is complete
    """
    for i in [1, 2]:
        if ((board & 3) == i) and ((board >> 8 & 3) == i) and ((board >> 16 & 3) == i):
            return i

        if (
            ((board >> 4 & 3) == i)
            and ((board >> 8 & 3) == i)
            and ((board >> 12 & 3) == i)
        ):
            return i
    return None


def check_tie(board):
    """
        check_tie: determines if board is in tie state
    """
    for i in range(0, 9):
        if board >> 2 * i & 3 == 0:
            return None
    return 3


def game_over(board):
    """
        game_over: determines if a bit string represents a game over
    """
    return (
        check_rows(board) or check_cols(board) or check_diag(board) or check_tie(board)
    )


if __name__ == "__main__":
    game()
