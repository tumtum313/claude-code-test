VALID_PLAYERS = {"X", "O"}


def check_winner(board):
    """Return the winning player, 'Draw', or None if the game is still active."""
    lines = []
    lines.extend(board)
    lines.extend([[board[row][col] for row in range(3)] for col in range(3)])
    lines.append([board[index][index] for index in range(3)])
    lines.append([board[index][2 - index] for index in range(3)])

    for line in lines:
        if line[0] in VALID_PLAYERS and line.count(line[0]) == 3:
            return line[0]

    if all(cell in VALID_PLAYERS for row in board for cell in row):
        return "Draw"

    return None


def make_move(board, row, col, player):
    """Place player's mark at row, col and return the updated board."""
    if player not in VALID_PLAYERS:
        raise ValueError("player must be 'X' or 'O'")

    if row not in range(3) or col not in range(3):
        raise ValueError("row and col must be between 0 and 2")

    if board[row][col] != " ":
        raise ValueError("cell is already occupied")

    board[row][col] = player
    return board


def _new_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def format_board(board):
    rows = []
    for index, row in enumerate(board):
        rows.append(" | ".join(row))
        if index < 2:
            rows.append("--+---+--")
    return "\n".join(rows)


def parse_move(text):
    parts = text.replace(",", " ").split()
    if len(parts) != 2:
        raise ValueError("enter row and column as two numbers from 0 to 2")

    try:
        row, col = (int(part) for part in parts)
    except ValueError as error:
        raise ValueError("enter row and column as two numbers from 0 to 2") from error

    if row not in range(3) or col not in range(3):
        raise ValueError("row and col must be between 0 and 2")

    return row, col


def next_player(player):
    return "O" if player == "X" else "X"


def _print_board(board):
    print(format_board(board))


def main():
    board = _new_board()
    player = "X"

    print("Tic-tac-toe")
    print("Enter moves as: row col, using numbers 0 through 2.")

    while True:
        _print_board(board)
        try:
            row, col = parse_move(input(f"Player {player}, enter move: "))
            make_move(board, row, col, player)
        except ValueError as error:
            print(error)
            continue

        result = check_winner(board)
        if result:
            _print_board(board)
            if result == "Draw":
                print("It's a draw!")
            else:
                print(f"Player {result} wins!")
            break

        player = next_player(player)


if __name__ == "__main__":
    main()
