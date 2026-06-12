import pytest

from tic_tac_toe import check_winner, make_move


def test_row_win():
    board = [
        ["X", "X", "X"],
        ["O", " ", "O"],
        [" ", " ", " "],
    ]

    assert check_winner(board) == "X"


def test_column_win():
    board = [
        ["O", "X", " "],
        ["O", "X", " "],
        ["O", " ", "X"],
    ]

    assert check_winner(board) == "O"


def test_diagonal_win():
    board = [
        ["X", "O", " "],
        ["O", "X", " "],
        [" ", " ", "X"],
    ]

    assert check_winner(board) == "X"


def test_draw():
    board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "X"],
    ]

    assert check_winner(board) == "Draw"


def test_invalid_move():
    board = [[" " for _ in range(3)] for _ in range(3)]

    with pytest.raises(ValueError, match="row and col"):
        make_move(board, 3, 0, "X")


def test_invalid_player():
    board = [[" " for _ in range(3)] for _ in range(3)]

    with pytest.raises(ValueError, match="player"):
        make_move(board, 0, 0, "A")


def test_occupied_cell():
    board = [[" " for _ in range(3)] for _ in range(3)]
    make_move(board, 1, 1, "X")

    with pytest.raises(ValueError, match="occupied"):
        make_move(board, 1, 1, "O")
