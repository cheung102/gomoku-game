"""AI 模块单元测试"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import Board
from ai_player import GomokuAI


class TestGomokuAI(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_easy_ai_blocks_winning_move(self):
        ai = GomokuAI(player=2, difficulty='easy')
        for i in range(4):
            self.board.make_move(7, 7 + i, 1)
        move = ai.get_move(self.board)
        self.assertIn(move, [(7, 6), (7, 11)])

    def test_easy_ai_takes_winning_move(self):
        ai = GomokuAI(player=2, difficulty='easy')
        for i in range(4):
            self.board.make_move(7, 7 + i, 2)
        move = ai.get_move(self.board)
        self.assertIn(move, [(7, 6), (7, 11)])

    def test_medium_ai_blocks_winning_move(self):
        ai = GomokuAI(player=2, difficulty='medium')
        for i in range(4):
            self.board.make_move(7, 7 + i, 1)
        move = ai.get_move(self.board)
        self.assertIn(move, [(7, 6), (7, 11)])

    def test_medium_ai_takes_winning_move(self):
        ai = GomokuAI(player=2, difficulty='medium')
        for i in range(4):
            self.board.make_move(7, 7 + i, 2)
        move = ai.get_move(self.board)
        self.assertIn(move, [(7, 6), (7, 11)])

    def test_hard_ai_blocks_winning_move(self):
        ai = GomokuAI(player=2, difficulty='hard')
        for i in range(4):
            self.board.make_move(7, 7 + i, 1)
        move = ai.get_move(self.board)
        self.assertIn(move, [(7, 6), (7, 11)])

    def test_hard_ai_takes_winning_move(self):
        ai = GomokuAI(player=2, difficulty='hard')
        for i in range(4):
            self.board.make_move(7, 7 + i, 2)
        move = ai.get_move(self.board)
        self.assertIn(move, [(7, 6), (7, 11)])

    def test_ai_does_not_play_occupied(self):
        ai = GomokuAI(player=2, difficulty='medium')
        self.board.make_move(7, 7, 1)
        move = ai.get_move(self.board)
        self.assertNotEqual(move, (7, 7))

    def test_ai_returns_valid_position(self):
        for diff in ['easy', 'medium', 'hard']:
            ai = GomokuAI(player=2, difficulty=diff)
            move = ai.get_move(self.board)
            self.assertIsNotNone(move)
            self.assertTrue(self.board.is_valid_move(*move))

    def test_hint_positions(self):
        ai = GomokuAI(player=2, difficulty='medium')
        self.board.make_move(7, 7, 1)
        self.board.make_move(7, 8, 2)
        hints = ai.get_hint_positions(self.board, num_hints=3)
        self.assertLessEqual(len(hints), 3)
        self.assertGreater(len(hints), 0)
        for pos in hints:
            self.assertTrue(self.board.is_valid_move(*pos))

    def test_get_candidate_moves(self):
        ai = GomokuAI(player=2, difficulty='medium')
        self.board.make_move(7, 7, 1)
        candidates = ai._get_candidate_moves(self.board)
        self.assertIn((6, 6), candidates)
        self.assertIn((8, 8), candidates)
        self.assertNotIn((7, 7), candidates)

    def test_minimax_returns_score(self):
        ai = GomokuAI(player=2, difficulty='hard')
        self.board.make_move(7, 7, 1)
        self.board.make_move(7, 8, 2)
        score = ai._minimax(self.board, 1, -float('inf'), float('inf'), True)
        self.assertIsInstance(score, (int, float))

    def test_easy_vs_medium(self):
        easy_ai = GomokuAI(player=2, difficulty='easy')
        medium_ai = GomokuAI(player=2, difficulty='medium')
        easy_move = easy_ai.get_move(self.board)
        medium_move = medium_ai.get_move(self.board)
        self.assertIsNotNone(easy_move)
        self.assertIsNotNone(medium_move)


if __name__ == '__main__':
    unittest.main()
