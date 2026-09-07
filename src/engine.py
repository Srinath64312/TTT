"""
Loopless Game Engine and Multi-Level Minimax AI.
Zero for-loops, zero while-loops, zero comprehensions, zero generator expressions.
Pure recursion and immutable transitions.
"""

import random

EMPTY_BOARD = (" ", " ", " ", " ", " ", " ", " ", " ", " ")


def create_board():
    return EMPTY_BOARD


def check_winner(b):
    if b[0] == b[1] == b[2] != " ": return b[0]
    if b[3] == b[4] == b[5] != " ": return b[3]
    if b[6] == b[7] == b[8] != " ": return b[6]
    if b[0] == b[3] == b[6] != " ": return b[0]
    if b[1] == b[4] == b[7] != " ": return b[1]
    if b[2] == b[5] == b[8] != " ": return b[2]
    if b[0] == b[4] == b[8] != " ": return b[0]
    if b[2] == b[4] == b[6] != " ": return b[2]
    return None


def is_board_full(board, index=0):
    if index == 9: return True
    if board[index] == " ": return False
    return is_board_full(board, index + 1)


def is_game_over(board):
    if check_winner(board) is not None: return True
    return is_board_full(board)


def count_empty_cells(board, index=0):
    if index == 9: return 0
    val = 1 if board[index] == " " else 0
    return val + count_empty_cells(board, index + 1)


def get_available_moves(board, index=0):
    if index == 9: return ()
    tail = get_available_moves(board, index + 1)
    if board[index] == " ":
        return (index,) + tail
    return tail


def make_move(board, pos, player):
    if pos < 0 or pos > 8 or board[pos] != " ":
        raise ValueError("Invalid move position: " + str(pos))
    return board[:pos] + (player,) + board[pos + 1:]


def _evaluate_moves_recursive(board, depth, is_maximizing, ai_player, human_player, moves, best_val, best_move):
    if not moves:
        return best_val, best_move

    pos = moves[0]
    curr_player = ai_player if is_maximizing else human_player
    next_board = make_move(board, pos, curr_player)
    score, _ = minimax(next_board, depth + 1, not is_maximizing, ai_player, human_player)

    if is_maximizing:
        if score > best_val:
            new_best_val, new_best_move = score, pos
        else:
            new_best_val, new_best_move = best_val, best_move
    else:
        if score < best_val:
            new_best_val, new_best_move = score, pos
        else:
            new_best_val, new_best_move = best_val, best_move

    return _evaluate_moves_recursive(
        board, depth, is_maximizing, ai_player, human_player,
        moves[1:], new_best_val, new_best_move
    )


def minimax(board, depth, is_maximizing, ai_player="O", human_player="X"):
    winner = check_winner(board)
    if winner == ai_player: return 10 - depth, None
    if winner == human_player: return depth - 10, None
    if is_board_full(board): return 0, None

    moves = get_available_moves(board)
    if not moves: return 0, None

    initial_val = -1000 if is_maximizing else 1000
    return _evaluate_moves_recursive(
        board, depth, is_maximizing, ai_player, human_player,
        moves, initial_val, moves[0]
    )


def get_best_ai_move(board, ai_player="O", human_player="X"):
    _, move = minimax(board, 0, is_maximizing=True, ai_player=ai_player, human_player=human_player)
    return move


def _find_immediate_win_recursive(board, moves, player):
    if not moves:
        return None
    pos = moves[0]
    next_board = make_move(board, pos, player)
    if check_winner(next_board) == player:
        return pos
    return _find_immediate_win_recursive(board, moves[1:], player)


def get_ai_move(board, difficulty="impossible", ai_player="O", human_player="X"):
    moves = get_available_moves(board)
    if not moves:
        return None

    diff = difficulty.lower()
    if diff in ("easy", "rookie", "east_blue"):
        if random.random() < 0.75:
            return random.choice(moves)
        return get_best_ai_move(board, ai_player=ai_player, human_player=human_player)

    elif diff in ("medium", "grand_line"):
        win_move = _find_immediate_win_recursive(board, moves, ai_player)
        if win_move is not None:
            return win_move
        block_move = _find_immediate_win_recursive(board, moves, human_player)
        if block_move is not None:
            return block_move
        if random.random() < 0.40:
            return random.choice(moves)
        return get_best_ai_move(board, ai_player=ai_player, human_player=human_player)

    elif diff in ("hard", "new_world"):
        if random.random() < 0.12:
            return random.choice(moves)
        return get_best_ai_move(board, ai_player=ai_player, human_player=human_player)

    else:
        return get_best_ai_move(board, ai_player=ai_player, human_player=human_player)
