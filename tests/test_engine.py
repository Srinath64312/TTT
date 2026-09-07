"""
Unit tests for Loopless Game Engine & AI.
"""

import unittest
from src.engine import (
    create_board,
    check_winner,
    is_board_full,
    is_game_over,
    count_empty_cells,
    get_available_moves,
    make_move,
    minimax,
    get_best_ai_move,
)


class TestLooplessEngine(unittest.TestCase):
    def test_create_board(self):
        board = create_board()
        self.assertEqual(len(board), 9)
        self.assertEqual(count_empty_cells(board), 9)
        self.assertFalse(is_board_full(board))
        self.assertIsNone(check_winner(board))

    def test_horizontal_wins(self):
        b1 = ("X", "X", "X", " ", " ", " ", " ", " ", " ")
        self.assertEqual(check_winner(b1), "X")
        b2 = (" ", " ", " ", "O", "O", "O", " ", " ", " ")
        self.assertEqual(check_winner(b2), "O")
        b3 = (" ", " ", " ", " ", " ", " ", "X", "X", "X")
        self.assertEqual(check_winner(b3), "X")

    def test_vertical_wins(self):
        b1 = ("X", " ", " ", "X", " ", " ", "X", " ", " ")
        self.assertEqual(check_winner(b1), "X")
        b2 = (" ", "O", " ", " ", "O", " ", " ", "O", " ")
        self.assertEqual(check_winner(b2), "O")
        b3 = (" ", " ", "X", " ", " ", "X", " ", " ", "X")
        self.assertEqual(check_winner(b3), "X")

    def test_diagonal_wins(self):
        b1 = ("X", " ", " ", " ", "X", " ", " ", " ", "X")
        self.assertEqual(check_winner(b1), "X")
        b2 = (" ", " ", "O", " ", "O", " ", "O", " ", " ")
        self.assertEqual(check_winner(b2), "O")

    def test_draw_condition(self):
        draw_board = ("X", "O", "X", "X", "O", "O", "O", "X", "X")
        self.assertTrue(is_board_full(draw_board))
        self.assertTrue(is_game_over(draw_board))
        self.assertIsNone(check_winner(draw_board))

    def test_make_move(self):
        b = create_board()
        b1 = make_move(b, 0, "X")
        self.assertEqual(b1[0], "X")
        self.assertEqual(b[0], " ")
        with self.assertRaises(ValueError):
            make_move(b1, 0, "O")

    def test_available_moves(self):
        b = ("X", " ", "O", " ", "X", " ", " ", " ", "O")
        moves = get_available_moves(b)
        self.assertEqual(moves, (1, 3, 5, 6, 7))

    def test_ai_blocks_immediate_loss(self):
        board = ("X", "X", " ", "O", " ", " ", " ", " ", " ")
        best_move = get_best_ai_move(board, ai_player="O", human_player="X")
        self.assertEqual(best_move, 2)

    def test_ai_takes_immediate_win(self):
        board = ("O", "O", " ", "X", "X", " ", " ", " ", " ")
        best_move = get_best_ai_move(board, ai_player="O", human_player="X")
        self.assertEqual(best_move, 2)


if __name__ == "__main__":
    unittest.main()
