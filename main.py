from enum import Enum

class CellState(Enum):
    EMPTY = " "
    X = "X"
    O = "O"

    def is_empty(self):
        return self == CellState.EMPTY

board = [[CellState.EMPTY, CellState.EMPTY, CellState.EMPTY] for _ in range(3)]

# Координати
columns = ['1', '2', '3']
rows = {'A': 0, 'B': 1, 'C': 2}

def print_board(board):
    print("  " + "   ".join(columns))
    for key, row in zip(rows.keys(), board):
        print(key, " | ".join(cell.value for cell in row))

def pos_is_correct(pos):
    if len(pos) == 2 and pos[0] in list(rows.keys()) and pos[1] in columns and board[rows[pos[0]]][int(pos[1]) - 1] == CellState.EMPTY:
        return True
    else:
        return False

def add_el(pos, state):
    board[pos[0]][pos[1]] = state

def make_normal_pos(pos):
    return rows[pos[0]], int(pos[1]) - 1

def is_row_winning(pos):
    state = board[pos[0]][pos[1]]
    for i in range(3):
        if state != board[pos[0]][i]:
            return False
    return True

def is_column_winning(pos):
    state = board[pos[0]][pos[1]]
    for i in range(3):
        if state != board[i][pos[1]]:
            return False
    return True

def is_diagonal_winning(pos):
    state = board[pos[0]][pos[1]]
    if pos[0] == pos[1]:  # головна діагональ
        if all(board[i][i] == state for i in range(3)):
            return True
    if pos[0] + pos[1] == 2:  # побічна діагональ
        if all(board[i][2 - i] == state for i in range(3)):
            return True
    return False

def check_win(pos):
    return is_row_winning(pos) or is_column_winning(pos) or is_diagonal_winning(pos)

def is_draw(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == CellState.EMPTY:
                return False
    return True

def clear_board(board):
    for i in range(3):
        for j in range(3):
            board[i][j] = CellState.EMPTY

def play_again():
    clear_board(board)
    answer = input("Do you want to play again? (y/n)")
    if answer == "y":
        return True
    else:
        return False

def main():
    players = ["Player 1", "Player 2"]
    states = [CellState.X, CellState.O]

    while True:
        clear_board(board)
        player = 0

        while True:
            print_board(board)
            pos = input(players[player] + " move: ").strip().upper()
            state = states[player]

            if pos_is_correct(pos):
                pos = make_normal_pos(pos)
                add_el(pos, state)

                if check_win(pos):
                    print_board(board)
                    print(players[player] + " wins!")
                    break

                if is_draw(board):
                    print_board(board)
                    print("Draw!")
                    break

                player = 1 - player

            else:
                print("Invalid move!")

        if not play_again():
            break

main()