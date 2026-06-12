import pytest

from tic_tac_toe import format_board, next_player, parse_move


def test_format_board():
    board = [
        ["X", "O", "X"],
        [" ", "X", " "],
        ["O", " ", "O"],
    ]

    assert format_board(board) == "X | O | X\n--+---+--\n  | X |  \n--+---+--\nO |   | O"


def test_parse_move_accepts_space_separated_input():
    assert parse_move("1 2") == (1, 2)


def test_parse_move_accepts_comma_separated_input():
    assert parse_move("0,2") == (0, 2)


def test_parse_move_rejects_missing_column():
    with pytest.raises(ValueError, match="row and column"):
        parse_move("1")


def test_parse_move_rejects_non_numeric_input():
    with pytest.raises(ValueError, match="row and column"):
        parse_move("top left")


def test_parse_move_rejects_out_of_range_input():
    with pytest.raises(ValueError, match="between 0 and 2"):
        parse_move("0 3")


def test_next_player_switches_turns():
    assert next_player("X") == "O"
    assert next_player("O") == "X"
