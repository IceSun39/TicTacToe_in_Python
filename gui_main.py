import tkinter as tk
from tkinter import messagebox, simpledialog
from enum import Enum
import random
import threading
import time


# Стан клітинки на полі
class CellState(Enum):
    EMPTY = " "
    X = "X"
    O = "O"

    def is_empty(self):
        return self == CellState.EMPTY


class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Хрестики-нулики / Tic-Tac-Toe")
        self.root.geometry("400x500")
        self.root.minsize(350, 450)
        self.root.resizable(True, True)
        
        # Ігрове поле 3x3 заповнене порожніми клітинками
        self.board = [[CellState.EMPTY, CellState.EMPTY, CellState.EMPTY] for _ in range(3)]
        
        # Змінні для гри
        self.current_player = CellState.X
        self.game_mode = None  # "pvp" або "bot"
        self.player_state = CellState.X
        self.bot_state = CellState.O
        self.game_active = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Хрестики-нулики", 
                              font=("Arial", 20, "bold"), bg="#2c3e50", fg="white", 
                              pady=8)
        title_label.pack(fill=tk.X, pady=5)
        
        # Фрейм для вибору режиму
        mode_frame = tk.Frame(self.root, bg="#ecf0f1")
        mode_frame.pack(pady=10)
        
        tk.Label(mode_frame, text="Оберіть режим гри:", 
                font=("Arial", 14), bg="#ecf0f1").pack(pady=5)
        
        # Кнопки вибору режиму
        btn_frame = tk.Frame(mode_frame, bg="#ecf0f1")
        btn_frame.pack(pady=5)
        
        self.pvp_btn = tk.Button(btn_frame, text="Гравець vs Гравець", 
                               command=self.start_pvp_game,
                               bg="#3498db", fg="white", font=("Arial", 10),
                               width=15, height=2)
        self.pvp_btn.pack(side=tk.LEFT, padx=5)
        
        self.bot_btn = tk.Button(btn_frame, text="Гравець vs Бот", 
                               command=self.start_bot_game,
                               bg="#e74c3c", fg="white", font=("Arial", 10),
                               width=15, height=2)
        self.bot_btn.pack(side=tk.LEFT, padx=5)
        
        # Інформаційна панель
        self.info_label = tk.Label(self.root, text="Оберіть режим гри", 
                                  font=("Arial", 12, "bold"), bg="#95a5a6", fg="white",
                                  pady=6)
        self.info_label.pack(fill=tk.X, pady=5)
        
        # Ігрове поле
        self.game_frame = tk.Frame(self.root, bg="#34495e")
        self.game_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.game_frame, text="", 
                              font=("Arial", 24, "bold"),
                              width=4, height=2,
                              bg="#bdc3c7", fg="#2c3e50",
                              command=lambda r=i, c=j: self.on_cell_click(r, c),
                              state=tk.DISABLED)
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
        
        # Фрейм для кнопок керування
        control_frame = tk.Frame(self.root, bg="#ecf0f1")
        control_frame.pack(pady=10)
        
        # Кнопка нової гри
        self.new_game_btn = tk.Button(control_frame, text="Нова гра", 
                                    command=self.new_game,
                                    bg="#27ae60", fg="white", 
                                    font=("Arial", 12, "bold"),
                                    width=12, height=2)
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка рестарт
        self.restart_btn = tk.Button(control_frame, text="Рестарт", 
                                   command=self.restart_game,
                                   bg="#f39c12", fg="white", 
                                   font=("Arial", 12, "bold"),
                                   width=12, height=2,
                                   state=tk.DISABLED)
        self.restart_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка виходу
        exit_btn = tk.Button(self.root, text="Вихід", 
                           command=self.root.quit,
                           bg="#95a5a6", fg="white", 
                           font=("Arial", 10),
                           width=10)
        exit_btn.pack(pady=5)
        
    def start_pvp_game(self):
        self.game_mode = "pvp"
        self.current_player = CellState.X
        self.game_active = True
        self.enable_board()
        self.restart_btn.config(state=tk.NORMAL)
        self.update_info("Гра 'Гравець vs Гравець' - Хід гравця X")
        
    def start_bot_game(self):
        # Діалог вибору символу для гравця
        choice = messagebox.askyesnocancel("Вибір символу", 
                                         "Хочете грати за X?\n\nТак - X (ви ходите першими)\nНі - O (бот ходить перший)")
        if choice is None:  # Скасування
            return
            
        self.game_mode = "bot"
        if choice:  # Гравець обрав X
            self.player_state = CellState.X
            self.bot_state = CellState.O
            self.current_player = CellState.X
            self.update_info("Гра проти бота - Ваш хід (X)")
        else:  # Гравець обрав O
            self.player_state = CellState.O
            self.bot_state = CellState.X
            self.current_player = CellState.X
            self.update_info("Гра проти бота - Хід бота (X)")
            
        self.game_active = True
        self.enable_board()
        self.restart_btn.config(state=tk.NORMAL)
        
        # Якщо бот ходить першим
        if self.current_player == self.bot_state:
            self.root.after(1000, self.make_bot_move)
        
    def enable_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.NORMAL)
                
    def disable_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)
                
    def on_cell_click(self, row, col):
        if not self.game_active or not self.board[row][col].is_empty():
            return
            
        # В режимі з ботом перевіряємо, чи хід гравця
        if self.game_mode == "bot" and self.current_player != self.player_state:
            return
            
        self.make_move(row, col, self.current_player)
        
    def make_move(self, row, col, state):
        # Зробити хід
        self.board[row][col] = state
        self.buttons[row][col].config(text=state.value, 
                                    bg="#e8f5e8" if state == CellState.X else "#ffe8e8",
                                    state=tk.DISABLED)
        
        # Перевірити перемогу
        if self.check_win((row, col)):
            if self.game_mode == "pvp":
                winner = "Гравець X" if state == CellState.X else "Гравець O"
                messagebox.showinfo("Перемога!", f"{winner} переміг!")
            else:
                if state == self.player_state:
                    messagebox.showinfo("Перемога!", "Ви перемогли!")
                else:
                    messagebox.showinfo("Поразка", "Бот переміг!")
            self.game_active = False
            self.disable_board()
            return
            
        # Перевірити нічию
        if self.is_draw():
            messagebox.showinfo("Нічия", "Гра завершена внічию!")
            self.game_active = False
            self.disable_board()
            return
            
        # Змінити поточного гравця
        self.current_player = CellState.O if self.current_player == CellState.X else CellState.X
        
        # Оновити інформацію
        if self.game_mode == "pvp":
            self.update_info(f"Хід гравця {self.current_player.value}")
        else:
            if self.current_player == self.player_state:
                self.update_info("Ваш хід")
            else:
                self.update_info("Хід бота...")
                self.root.after(1500, self.make_bot_move)
                
    def make_bot_move(self):
        if not self.game_active:
            return
            
        row, col = self.get_bot_move()
        self.make_move(row, col, self.bot_state)
        
    def update_info(self, text):
        self.info_label.config(text=text)
        
    def new_game(self):
        # Очистити поле
        self.board = [[CellState.EMPTY, CellState.EMPTY, CellState.EMPTY] for _ in range(3)]
        
        # Очистити кнопки
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="#bdc3c7", state=tk.DISABLED)
                
        # Скинути стан гри
        self.game_active = False
        self.current_player = CellState.X
        self.game_mode = None
        self.restart_btn.config(state=tk.DISABLED)
        self.update_info("Оберіть режим гри")
        
    def restart_game(self):
        if not self.game_mode:
            return
            
        # Очистити поле
        self.board = [[CellState.EMPTY, CellState.EMPTY, CellState.EMPTY] for _ in range(3)]
        
        # Очистити кнопки
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="#bdc3c7", state=tk.NORMAL)
                
        # Перезапустити гру в тому ж режимі
        if self.game_mode == "pvp":
            self.current_player = CellState.X
            self.game_active = True
            self.update_info("Гра 'Гравець vs Гравець' - Хід гравця X")
        elif self.game_mode == "bot":
            self.current_player = CellState.X
            self.game_active = True
            if self.player_state == CellState.X:
                self.update_info("Гра проти бота - Ваш хід (X)")
            else:
                self.update_info("Гра проти бота - Хід бота (X)")
                self.root.after(1000, self.make_bot_move)
        
    # Логіка гри (з оригінального коду)
    def check_win(self, pos):
        return self.is_row_winning(pos) or self.is_column_winning(pos) or self.is_diagonal_winning(pos)
        
    def is_row_winning(self, pos):
        state = self.board[pos[0]][pos[1]]
        for i in range(3):
            if state != self.board[pos[0]][i]:
                return False
        return True
        
    def is_column_winning(self, pos):
        state = self.board[pos[0]][pos[1]]
        for i in range(3):
            if state != self.board[i][pos[1]]:
                return False
        return True
        
    def is_diagonal_winning(self, pos):
        state = self.board[pos[0]][pos[1]]
        if pos[0] == pos[1]:  # головна діагональ
            if all(self.board[i][i] == state for i in range(3)):
                return True
        if pos[0] + pos[1] == 2:  # побічна діагональ
            if all(self.board[i][2 - i] == state for i in range(3)):
                return True
        return False
        
    def is_draw(self):
        return all(cell != CellState.EMPTY for row in self.board for cell in row)
        
    def get_bot_move(self):
        # Спроба виграти
        for i in range(3):
            for j in range(3):
                if self.board[i][j].is_empty():
                    self.board[i][j] = self.bot_state
                    if self.check_win((i, j)):
                        self.board[i][j] = CellState.EMPTY
                        return (i, j)
                    self.board[i][j] = CellState.EMPTY

        # Спроба заблокувати
        for i in range(3):
            for j in range(3):
                if self.board[i][j].is_empty():
                    self.board[i][j] = self.player_state
                    if self.check_win((i, j)):
                        self.board[i][j] = CellState.EMPTY
                        return (i, j)
                    self.board[i][j] = CellState.EMPTY

        # Центр
        if self.board[1][1].is_empty():
            return (1, 1)

        # Кути
        corners = [(0, 0), (2, 0), (0, 2), (2, 2)]
        random.shuffle(corners)
        for i, j in corners:
            if self.board[i][j].is_empty():
                return (i, j)

        # Будь-яка вільна
        available = [(i, j) for i in range(3) for j in range(3) if self.board[i][j].is_empty()]
        return random.choice(available)
        
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run()