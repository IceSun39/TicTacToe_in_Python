from enum import Enum
import random
from time import sleep
import sys

# Стан клітинки на полі
class CellState(Enum):
    EMPTY = " "
    X = "X"
    O = "O"

    def is_empty(self):
        return self == CellState.EMPTY


# Ігрове поле 3x3 заповнене порожніми клітинками
board = [[CellState.EMPTY, CellState.EMPTY, CellState.EMPTY] for _ in range(3)]

# Координати для взаємозв'язку букв з рядками
columns = ['1', '2', '3']
rows = {'A': 0, 'B': 1, 'C': 2}


# Вивід ігрового поля у зручному форматі
def print_board(board):
    print("  " + "   ".join(columns))
    for key, row in zip(rows.keys(), board):
        print(key, " | ".join(cell.value for cell in row))


# Перевірка чи введена позиція є коректною та вільною
def pos_is_correct(pos):
    if len(pos) == 2 and pos[0] in list(rows.keys()) and pos[1] in columns and board[rows[pos[0]]][int(pos[1]) - 1] == CellState.EMPTY:
        return True
    else:
        return False


# Додає символ гравця на вказану позицію
def add_el(pos, state):
    board[pos[0]][pos[1]] = state


# Преобразовує позицію з формату "A1" у координати матриці
def make_normal_pos(pos):
    return rows[pos[0]], int(pos[1]) - 1


# Перевірка чи весь рядок однаковий
def is_row_winning(board, state):
    for i in range(3):
        if board[i][0] == state and board[i][1] == state and board[i][2] == state:
            return True
    return False

# Перевірка чи весь стовпець однаковий
def is_column_winning(board, state):
    for i in range(3):
        if board[0][i] == state and board[1][i] == state and board[2][i] == state:
            return True
    return False


# Перевірка діагоналей (головної і побічної)
def is_diagonal_winning(board, state):
    # головна діагональ
    if all(board[i][i] == state for i in range(3)):
        return True
    # побічна діагональ
    if all(board[i][2 - i] == state for i in range(3)):
        return True
    return False

# Перевірка перемоги по будь-якому напрямку
def check_win(board, state):
    return is_row_winning(board, state) or is_column_winning(board, state) or is_diagonal_winning(board, state)

# Перевірка чи всі клітинки заповнені (нічия)
def is_draw(board):
    return all(cell != CellState.EMPTY for row in board for cell in row)

# Оцінка ходу для алгоритму minmax
def evaluate(board, bot_state):
    # Визначаємо символ гравця
    player_state = CellState.X if bot_state == CellState.O else CellState.O

    # Перевіряємо перемоги
    if check_win(board, bot_state):
        return 1
    elif check_win(board, player_state):
        return -1
    elif is_draw(board):
        return 0

    # Якщо гра не завершена
    return None

# Очистити поле (встановити все як EMPTY)
def clear_board(board):
    for i in range(3):
        for j in range(3):
            board[i][j] = CellState.EMPTY

# Запит чи гравець хоче зіграти ще раз
def play_again():
    clear_board(board)
    answer = input("Do you want to play again? (y/n) ")
    return answer.lower() == "y"

# Логіка бота
def minmax(board, depth, is_maximising, bot_state, player_state):
     res = evaluate(board, bot_state)
     if res is not None:
         return res

     if is_maximising:
         best_score = -sys.maxsize - 1
         for i in range(3):
             for j in range(3):
                 if board[i][j].is_empty():
                     new_board = [row[:] for row in board]
                     new_board[i][j] = bot_state
                     score = minmax(new_board, depth + 1, not is_maximising, bot_state, player_state)
                     best_score = max(best_score, score)
         return best_score
     else:
        best_score = sys.maxsize
        for i in range(3):
            for j in range(3):
                if board[i][j].is_empty():
                    new_board = [row[:] for row in board]
                    new_board[i][j] = player_state
                    score = minmax(new_board, depth + 1, not is_maximising, bot_state, player_state)
                    best_score = min(best_score, score)
        return best_score


def get_bot_move(board, bot_state, player_state):
    best_score = -sys.maxsize
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j].is_empty():
                new_board = [row[:] for row in board]
                new_board[i][j] = bot_state
                score = minmax(new_board, 0, False, bot_state, player_state)
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

# Гра гравець проти гравця
def game_with_player(players, states, player):
    while True:
        print_board(board)
        pos = input(players[player] + " move: ").strip().upper()
        state = states[player]

        if pos_is_correct(pos):
            pos = make_normal_pos(pos)
            add_el(pos, state)

            if check_win(board, state):
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


# Гра гравець проти бота
def game_with_bot(player_state, bot_state):
    is_player_move = True if player_state == CellState.X else False

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
            sleep(1)
            pos = get_bot_move(board, bot_state, player_state)
            add_el(pos, bot_state)
            is_player_move = not is_player_move

        # Перевірка перемоги
        if check_win(board, bot_state) and is_player_move:
            print_board(board)
            print("Bot wins!")
            break
        if check_win(board, player_state) and not is_player_move:
            print_board(board)
            print("Player wins!")
            break

        # Нічия
        if is_draw(board):
            print_board(board)
            print("Draw!")
            break


# Головна функція — вибір режиму та запуск відповідної гри
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
        # Гра 1 на 1
        players = ["Player 1", "Player 2"]
        states = [CellState.X, CellState.O]
        while True:
            clear_board(board)
            player = 0
            game_with_player(players, states, player)
            if not play_again():
                break
    else:
        # Гра з ботом
        while True:
            clear_board(board)
            player_state = input("Choose state: X or O ").strip().upper()

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
