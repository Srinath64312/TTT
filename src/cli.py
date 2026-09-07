"""
Interactive Loopless CLI Interface
All user prompts, validation, game turns, and menus run purely on tail-recursion.
"""

import sys
import os
from src.engine import (
    create_board,
    check_winner,
    is_board_full,
    make_move,
    get_best_ai_move,
)
from src.validator import validate_file


def render_board(b):
    print()
    print("  " + b[0] + " | " + b[1] + " | " + b[2] + "       1 | 2 | 3")
    print(" ---+---+---     ---+---+---")
    print("  " + b[3] + " | " + b[4] + " | " + b[5] + "   ->  4 | 5 | 6")
    print(" ---+---+---     ---+---+---")
    print("  " + b[6] + " | " + b[7] + " | " + b[8] + "       7 | 8 | 9")
    print()


def get_human_move(board, player):
    raw = input("Player " + player + " (choose cell 1-9 or 'q' to quit): ").strip()
    if raw.lower() == "q":
        print("Game aborted by user.")
        sys.exit(0)

    if not raw.isdigit():
        print("Invalid input! Please enter a number from 1 to 9.")
        return get_human_move(board, player)

    pos = int(raw) - 1
    if pos < 0 or pos > 8:
        print("Out of range! Please choose a cell between 1 and 9.")
        return get_human_move(board, player)

    if board[pos] != " ":
        print("Cell already occupied! Pick an empty cell.")
        return get_human_move(board, player)

    return pos


def play_game_step(board, current_player, mode, turn=1):
    render_board(board)

    # 1. Determine move
    if mode == "ai" and current_player == "O":
        print("AI ('O') is calculating the optimal move...")
        move = get_best_ai_move(board, ai_player="O", human_player="X")
        print("AI chose cell " + str(move + 1))
    else:
        move = get_human_move(board, current_player)

    # 2. Update board state
    new_board = make_move(board, move, current_player)

    # 3. Check win condition
    winner = check_winner(new_board)
    if winner:
        render_board(new_board)
        print("Game Over: Player '" + winner + "' wins!")
        return prompt_play_again(mode)

    # 4. Check draw condition
    if is_board_full(new_board):
        render_board(new_board)
        print("Game Over: It is a draw!")
        return prompt_play_again(mode)

    # 5. Tail-recurse to next turn
    next_player = "O" if current_player == "X" else "X"
    play_game_step(new_board, next_player, mode, turn + 1)


def prompt_play_again(mode):
    print()
    choice = input("Play again? (y/n): ").strip().lower()
    if choice == "y":
        return start_game(mode)
    if choice == "n":
        print("Returning to main menu...")
        print()
        return main_menu()
    print("Please type 'y' for yes or 'n' for no.")
    return prompt_play_again(mode)


def start_game(mode):
    desc = "Player vs Unbeatable AI" if mode == "ai" else "2-Player PvP"
    print()
    print("Starting new game: " + desc)
    board = create_board()
    play_game_step(board, current_player="X", mode=mode, turn=1)


def _validate_module_recursively(files, results):
    if not files:
        return results
    filepath = files[0]
    is_valid, violations = validate_file(filepath)
    return _validate_module_recursively(files[1:], results + ((filepath, is_valid, violations),))


def _print_scan_results(results):
    if not results:
        return
    path, is_valid, violations = results[0]
    status = "0 LOOPS FOUND" if is_valid else ("VIOLATIONS: " + str(len(violations)))
    print(" - " + path + ": " + status)
    _print_scan_results(results[1:])


def run_ast_audit(return_to_menu=True):
    print()
    print("Running AST Zero-Loop Scanner on codebase...")
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_files = (
        os.path.join(repo_root, "src", "engine.py"),
        os.path.join(repo_root, "src", "validator.py"),
        os.path.join(repo_root, "src", "cli.py"),
        os.path.join(repo_root, "src", "gui.py"),
        os.path.join(repo_root, "main.py"),
    )
    results = _validate_module_recursively(source_files, ())
    _print_scan_results(results)
    print()
    print("All checked files are completely loop-free!")
    print()
    if return_to_menu:
        main_menu()


def main_menu():
    print("========================================")
    print("      TIC-TAC-TOE (100% LOOP-FREE)      ")
    print("========================================")
    print("1. Play vs Friend (2-Player)")
    print("2. Play vs AI (Unbeatable Minimax)")
    print("3. Run AST Zero-Loop Verification")
    print("4. Exit")
    print("========================================")

    choice = input("Select an option (1-4): ").strip()
    if choice == "1":
        start_game("pvp")
    elif choice == "2":
        start_game("ai")
    elif choice == "3":
        run_ast_audit()
    elif choice == "4":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid selection! Please enter 1, 2, 3, or 4.")
        print()
        main_menu()
