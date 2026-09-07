"""
Loopless Desktop GUI (Tkinter)
Event-driven graphical interface with recursive button initialization and updates.
Zero loops used.
"""

import tkinter as tk
from tkinter import messagebox
from src.engine import (
    create_board,
    check_winner,
    is_board_full,
    make_move,
    get_best_ai_move,
)


class LooplessTicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Loopless Tic-Tac-Toe")
        self.root.resizable(False, False)

        self.board = create_board()
        self.current_player = "X"
        self.mode = "ai"
        self.game_active = True

        self.status_var = tk.StringVar(value="Player X's Turn (vs AI)")
        self.mode_var = tk.StringVar(value="Mode: Human vs AI")

        self._setup_ui()

    def _setup_ui(self):
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack()

        tk.Label(
            top_frame,
            textvariable=self.status_var,
            font=("Helvetica", 14, "bold"),
            fg="#1A73E8",
        ).pack()

        self.grid_frame = tk.Frame(self.root, padx=10, pady=10)
        self.grid_frame.pack()

        self.buttons = ()
        self._build_grid_buttons(0)

        bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        bottom_frame.pack()

        tk.Button(
            bottom_frame,
            text="Toggle Mode",
            command=self.toggle_mode,
            font=("Helvetica", 10),
            padx=5,
            pady=3,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            bottom_frame,
            text="New Game",
            command=self.reset_game,
            font=("Helvetica", 10, "bold"),
            bg="#E8EAED",
            padx=5,
            pady=3,
        ).pack(side=tk.LEFT, padx=5)

    def _build_grid_buttons(self, idx):
        if idx == 9:
            return

        row = idx // 3
        col = idx % 3
        btn = tk.Button(
            self.grid_frame,
            text=" ",
            font=("Helvetica", 24, "bold"),
            width=4,
            height=2,
            command=lambda pos=idx: self.on_cell_clicked(pos),
            bg="#F8F9FA",
            relief="groove",
        )
        btn.grid(row=row, column=col, padx=4, pady=4)
        self.buttons = self.buttons + (btn,)

        self._build_grid_buttons(idx + 1)

    def _sync_button_display(self, idx=0):
        if idx == 9:
            return
        symbol = self.board[idx]
        btn = self.buttons[idx]
        btn.config(text=symbol)
        if symbol == "X":
            btn.config(fg="#D93025")
        elif symbol == "O":
            btn.config(fg="#1A73E8")
        else:
            btn.config(fg="#202124")
        self._sync_button_display(idx + 1)

    def on_cell_clicked(self, pos):
        if not self.game_active or self.board[pos] != " ":
            return

        self.board = make_move(self.board, pos, self.current_player)
        self._sync_button_display()

        if self._check_game_end():
            return

        if self.mode == "pvp":
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_var.set("Player " + self.current_player + "'s Turn")
        elif self.mode == "ai":
            self.current_player = "O"
            self.status_var.set("AI is thinking...")
            self.root.after(200, self._execute_ai_turn)

    def _execute_ai_turn(self):
        if not self.game_active:
            return
        ai_pos = get_best_ai_move(self.board, ai_player="O", human_player="X")
        if ai_pos is not None:
            self.board = make_move(self.board, ai_pos, "O")
            self._sync_button_display()

        if self._check_game_end():
            return

        self.current_player = "X"
        self.status_var.set("Player X's Turn")

    def _check_game_end(self):
        winner = check_winner(self.board)
        if winner:
            self.game_active = False
            msg = "Player '" + winner + "' wins!"
            self.status_var.set(msg)
            messagebox.showinfo("Game Over", msg)
            return True
        if is_board_full(self.board):
            self.game_active = False
            msg = "It's a draw!"
            self.status_var.set(msg)
            messagebox.showinfo("Game Over", msg)
            return True
        return False

    def toggle_mode(self):
        self.mode = "pvp" if self.mode == "ai" else "ai"
        mode_label = "Human vs Human" if self.mode == "pvp" else "Human vs AI"
        messagebox.showinfo("Mode Changed", "Switched to " + mode_label)
        self.reset_game()

    def reset_game(self):
        self.board = create_board()
        self.current_player = "X"
        self.game_active = True
        mode_desc = "vs AI" if self.mode == "ai" else "2-Player"
        self.status_var.set("Player X's Turn (" + mode_desc + ")")
        self._sync_button_display()


def launch_gui():
    root = tk.Tk()
    app = LooplessTicTacToeGUI(root)
    root.mainloop()
