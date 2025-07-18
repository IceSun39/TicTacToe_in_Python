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
    if len(pos) == 2 and pos[0] in rows.keys() and pow[1] in columns:
        return True
    else:
        return False

def add_el(pos, state):
    board[pos[0]][pos[1]] = state

def make_normal_pos(pos):
    return rows[pos[0]], int(pos[1])

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
    for i in range(3):
        if state != board[i][i]:
            return False
    return True


