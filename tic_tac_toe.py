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


def _print_board(board):
    for index, row in enumerate(board):
        print(" | ".join(row))
        if index < 2:
            print("--+---+--")


def main():
    board = _new_board()
    player = "X"

    while True:
        _print_board(board)
        try:
            row = int(input(f"Player {player}, enter row (0-2): "))
            col = int(input(f"Player {player}, enter column (0-2): "))
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

        player = "O" if player == "X" else "X"


if __name__ == "__main__":
    main()
