from enum import Enum
import random
from time import sleep


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
    return all(cell != CellState.EMPTY for row in board for cell in row)

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

def get_bot_move(bot_state, player_state):
    for i in range(3):
        for j in range(3):
            if board[i][j].is_empty():
                board[i][j] = bot_state
                if check_win((i, j)):
                    board[i][j] = CellState.EMPTY
                    return (i, j)
                board[i][j] = CellState.EMPTY

    for i in range(3):
        for j in range(3):
            if board[i][j].is_empty():
                board[i][j] = player_state
                if check_win((i, j)):
                    board[i][j] = CellState.EMPTY
                    return (i, j)
                board[i][j] = CellState.EMPTY

    if board[1][1].is_empty():
        return (1, 1)

    corners = [(0,0), (2,0), (0,2), (2,2)]
    random.shuffle(corners)
    for i, j in corners:
        if board[i][j].is_empty():
            return (i, j)

    available = [(i, j) for i in range(3) for j in range(3) if board[i][j].is_empty()]
    return random.choice(available)

def game_with_player(players, states, player):
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

def game_with_bot(player_state, bot_state):
    is_player_move = True
    if player_state == CellState.O:
        is_player_move = False

    while True:

        if is_player_move:
            print_board(board)
            pos = input("Make a move: ").strip().upper()

            if pos_is_correct(pos):
                pos = make_normal_pos(pos)
                add_el(pos, player_state)
                is_player_move = not is_player_move

            else:
                print("Invalid move!")

        else:
            print_board(board)
            print("Bot is thinking...")
            sleep(3)
            pos = get_bot_move(bot_state, player_state)
            add_el(pos, bot_state)
            is_player_move = not is_player_move

        if check_win(pos) and is_player_move:
            print_board(board)
            print("Bot wins!")
            break

        if check_win(pos) and not is_player_move:
            print_board(board)
            print("Player wins!")
            break

        if is_draw(board):
            print_board(board)
            print("Draw!")
            break


def main():
    bot_enable = False
    while True:
        mode = int(input("Choose mode: 1 - PvP, 2 - PvBot "))
        if mode == 1:
            bot_enable = False
            break
        elif mode == 2:
            bot_enable = True
            break
        else:
            print("Invalid mode!")

    if not bot_enable:
        players = ["Player 1", "Player 2"]
        states = [CellState.X, CellState.O]
        while True:
            clear_board(board)
            player = 0

            game_with_player(players, states, player)

            if not play_again():
                break
    else:
        while True:
            clear_board(board)
            player_state = input("Choose state: X or O ")

            if player_state == "X":
                player_state = CellState.X
                bot_state = CellState.O
                game_with_bot(player_state, bot_state)
                if not play_again():
                    break
            elif player_state == "O":
                player_state = CellState.O
                bot_state = CellState.X
                game_with_bot(player_state, bot_state)
                if not play_again():
                    break
            else:
                print("Invalid state!")



main()