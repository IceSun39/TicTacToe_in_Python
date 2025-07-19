import tkinter as tk
import random
from enum import Enum


# Стани клітинки гри
class CellState(Enum):
    EMPTY = " "
    X = "X"
    O = "O"


# GUI для гри Тік-Так-Тое
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x500")
        self.root.minsize(400, 500)

        # Ігрові дані
        self.board = [[CellState.EMPTY] * 3 for _ in range(3)]
        self.buttons = [[None] * 3 for _ in range(3)]
        self.current_player = CellState.X
        self.game_mode = tk.StringVar(value="2 Players")
        self.scores = {CellState.X: 0, CellState.O: 0, 'Draw': 0}
        self.is_game_over = False

        # Основний контейнер
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # UI
        self.create_mode_selector()
        self.create_board()
        self.create_status_label()
        self.create_score_label()
        self.create_control_buttons()

        self.game_mode.trace_add('write', self.on_mode_change)
        self.root.bind('<Configure>', self.on_resize)

    def create_mode_selector(self):
        frame = tk.Frame(self.main_frame)
        frame.pack(pady=10)
        tk.Radiobutton(frame, text="2 Players", variable=self.game_mode, value="2 Players").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame, text="Vs Bot", variable=self.game_mode, value="Vs Bot").pack(side=tk.LEFT, padx=5)

    def create_board(self):
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)
            for j in range(3):
                btn = tk.Button(self.board_frame, text="", font=("Helvetica", 40),
                                command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j, sticky='nsew', padx=5, pady=5)
                self.buttons[i][j] = btn

    def create_status_label(self):
        self.status_label = tk.Label(self.main_frame, text="Player X's turn", font=("Helvetica", 16))
        self.status_label.pack(pady=5)

    def create_score_label(self):
        self.score_label = tk.Label(self.main_frame, text=self.get_score_text(), font=("Helvetica", 14))
        self.score_label.pack(pady=5)

    def create_control_buttons(self):
        frame = tk.Frame(self.main_frame)
        frame.pack(pady=5)
        tk.Button(frame, text="Restart", command=self.restart_game).pack()

    def get_score_text(self):
        return f"X: {self.scores[CellState.X]}  O: {self.scores[CellState.O]}  Draws: {self.scores['Draw']}"

    def on_resize(self, event):
        if not self.buttons[0][0]: 
            return
        size = int(min(event.width, event.height) / 12)
        for row in self.buttons:
            for btn in row:
                btn.config(font=("Helvetica", size))
        
        # Ensure symbols don't disappear during resize
        self.sync_buttons_with_board()

    def on_mode_change(self, *args):
        self.scores = {CellState.X: 0, CellState.O: 0, 'Draw': 0}
        self.score_label.config(text=self.get_score_text())
        self.restart_game()

    def make_move(self, r, c):
        if self.board[r][c] != CellState.EMPTY or self.is_game_over:
            return

        # Make the move
        self.board[r][c] = self.current_player
        self.buttons[r][c].config(text=self.current_player.value, state=tk.DISABLED)

        # Check for win
        if self.check_win(r, c):
            self.scores[self.current_player] += 1
            self.status_label.config(text=f"{self.current_player.value} wins!")
            self.score_label.config(text=self.get_score_text())
            self.disable_buttons()
            self.is_game_over = True
            return

        # Check for draw
        if self.check_draw():
            self.scores['Draw'] += 1
            self.status_label.config(text="Draw!")
            self.score_label.config(text=self.get_score_text())
            self.disable_buttons()
            self.is_game_over = True
            return

        # Switch players
        self.current_player = CellState.O if self.current_player == CellState.X else CellState.X
        self.status_label.config(text=f"Player {self.current_player.value}'s turn")

        # Handle bot move if needed
        if self.game_mode.get() == "Vs Bot" and self.current_player == CellState.O and not self.is_game_over:
            # Disable all buttons temporarily to prevent user clicks during bot's turn
            self.disable_buttons()
            self.root.after(300, self.bot_move)

    def bot_move(self):
        if self.is_game_over:
            return
            
        move = self.find_best_move()
        if move:
            r, c = move
            # Make sure the cell is still empty before bot makes the move
            if self.board[r][c] == CellState.EMPTY:
                self.board[r][c] = self.current_player
                self.buttons[r][c].config(text=self.current_player.value, state=tk.DISABLED)

                # Check for bot win
                if self.check_win(r, c):
                    self.scores[self.current_player] += 1
                    self.status_label.config(text=f"{self.current_player.value} wins!")
                    self.score_label.config(text=self.get_score_text())
                    self.disable_buttons()
                    self.is_game_over = True
                    return

                # Check for draw
                if self.check_draw():
                    self.scores['Draw'] += 1
                    self.status_label.config(text="Draw!")
                    self.score_label.config(text=self.get_score_text())
                    self.disable_buttons()
                    self.is_game_over = True
                    return

                # Switch back to human player
                self.current_player = CellState.X
                self.status_label.config(text=f"Player {self.current_player.value}'s turn")

        # Re-enable buttons for human player (only empty cells)
        if not self.is_game_over:
            self.enable_empty_buttons()

    def enable_empty_buttons(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == CellState.EMPTY:
                    self.buttons[i][j].config(state=tk.NORMAL)
                else:
                    # Ensure buttons with symbols remain disabled and show correct text
                    self.buttons[i][j].config(text=self.board[i][j].value, state=tk.DISABLED)

    def find_best_move(self):
        for sym in (CellState.O, CellState.X):
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == CellState.EMPTY:
                        self.board[i][j] = sym
                        if self.check_win(i, j):
                            self.board[i][j] = CellState.EMPTY
                            return (i, j)
                        self.board[i][j] = CellState.EMPTY
        if self.board[1][1] == CellState.EMPTY: return (1, 1)
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)];
        random.shuffle(corners)
        for i, j in corners:
            if self.board[i][j] == CellState.EMPTY: return (i, j)
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)];
        random.shuffle(sides)
        for i, j in sides:
            if self.board[i][j] == CellState.EMPTY: return (i, j)
        return None

    # Перевірка виграшу
    def check_win(self, r, c):
        # FIX: Спочатку отримуємо символ гравця
        s = self.board[r][c]

        # FIX: Якщо клітинка порожня, перемоги бути не може.
        # Це ключове виправлення, яке усуває баг.
        if s == CellState.EMPTY:
            return False

        # Решта логіки залишається такою ж
        return any([
            all(self.board[r][i] == s for i in range(3)),
            all(self.board[i][c] == s for i in range(3)),
            (r == c and all(self.board[i][i] == s for i in range(3))),
            (r + c == 2 and all(self.board[i][2 - i] == s for i in range(3)))
        ])

    def check_draw(self):
        return all(self.board[i][j] != CellState.EMPTY for i in range(3) for j in range(3))

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row: btn.config(state=tk.DISABLED)

    def sync_buttons_with_board(self):
        """Synchronize button display with the actual board state to prevent disappearing symbols."""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == CellState.EMPTY:
                    self.buttons[i][j].config(text="", state=tk.NORMAL if not self.is_game_over else tk.DISABLED)
                else:
                    self.buttons[i][j].config(text=self.board[i][j].value, state=tk.DISABLED)

    def restart_game(self):
        self.is_game_over = False
        self.board = [[CellState.EMPTY] * 3 for _ in range(3)]
        self.current_player = CellState.X
        self.status_label.config(text="Player X's turn")
        
        # Reset all buttons with proper state and text
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL)


# Запуск програми
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
