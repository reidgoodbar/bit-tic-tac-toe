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

    moves = computer_move_search(board, move, move, 0)
    print(moves)
    winning_move = moves.index(max(moves))
    # Why random move?
    # winning_move = random_move(board, move)

    # for i, val in searched.items():
    #     move_count = 0
    #     other_count = 0
    #     if move in val:
    #         move_count = val[move]
    #     if move % 2 + 1 in val:
    #         other_count = val[move % 2 + 1]
    #     if (move_count - other_count) > move_delta:
    #         move_delta = move_count - other_count
    #         winning_move = i

    # print(searched)
    board = board | (move << 2 * winning_move)
    # searched = {}
    return board


def computer_move_search(board, move, curr_move, depth):
    """
        computer_move_search: computer fills results array with all possible moves
    """
    print("---------------")
    print(curr_move)
    res = [0] * 9
    original_board = board
    for i in range(9):
        if ((board >> (i * 2)) & 3) == 0:
            board = board | (curr_move << 2 * i)
            print_board(board)
            game_res = game_over(board)
            if game_res not in [1, 2, 3]:
                if move == curr_move:
                    res[i] = min(
                        computer_move_search(board, move, (curr_move % 2 + 1), depth)
                    )
                else:
                    res[i] = max(
                        computer_move_search(board, move, (curr_move % 2 + 1), depth)
                    )
            elif game_res == move:
                res[i] = 10
            elif game_res == move % 2 + 1:
                res[i] = -10
            else:
                res[i] = 0
            board = original_board
    print(res)
    print("---------------")
    return res


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
