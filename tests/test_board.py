import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(15)
    
    def test_initial_board(self):
        """测试棋盘初始化"""
        self.assertEqual(self.board.size, 15)
        for row in range(15):
            for col in range(15):
                self.assertEqual(self.board.grid[row][col], 0)
    
    def test_valid_move(self):
        """测试有效落子"""
        self.assertTrue(self.board.make_move(7, 7, 1))
        self.assertEqual(self.board.grid[7][7], 1)
    
    def test_invalid_move_out_of_bounds(self):
        """测试越界落子"""
        self.assertFalse(self.board.make_move(15, 7, 1))
        self.assertFalse(self.board.make_move(-1, 7, 1))
        self.assertFalse(self.board.make_move(7, 15, 1))
        self.assertFalse(self.board.make_move(7, -1, 1))
    
    def test_invalid_move_occupied(self):
        """测试已有棋子的位置落子"""
        self.assertTrue(self.board.make_move(7, 7, 1))
        self.assertFalse(self.board.make_move(7, 7, 2))
    
    def test_check_win_horizontal(self):
        """测试水平方向胜利"""
        # 放置5个水平棋子
        for i in range(5):
            self.board.make_move(7, 7 + i, 1)
        self.assertTrue(self.board.check_win(1))
    
    def test_check_win_vertical(self):
        """测试垂直方向胜利"""
        # 放置5个垂直棋子
        for i in range(5):
            self.board.make_move(7 + i, 7, 1)
        self.assertTrue(self.board.check_win(1))
    
    def test_check_win_diagonal(self):
        """测试对角线方向胜利"""
        # 放置5个对角线棋子
        for i in range(5):
            self.board.make_move(7 + i, 7 + i, 1)
        self.assertTrue(self.board.check_win(1))
    
    def test_check_win_anti_diagonal(self):
        """测试反对角线方向胜利"""
        # 放置5个反对角线棋子
        for i in range(5):
            self.board.make_move(7 + i, 7 - i, 1)
        self.assertTrue(self.board.check_win(1))
    
    def test_no_win_incomplete(self):
        """测试未完成五子连珠"""
        # 放置4个棋子
        for i in range(4):
            self.board.make_move(7, 7 + i, 1)
        self.assertFalse(self.board.check_win(1))
    
    def test_win_only_own_pieces(self):
        """测试只能用自己的棋子赢"""
        # 放置对方棋子
        for i in range(4):
            self.board.make_move(7, 7 + i, 2)
        # 自己放一个棋子
        self.board.make_move(7, 11, 1)
        self.assertFalse(self.board.check_win(1))
    
    def test_is_full(self):
        """测试棋盘已满"""
        # 填满整个棋盘
        for row in range(15):
            for col in range(15):
                self.board.make_move(row, col, 1)
        self.assertTrue(self.board.is_full())
    
    def test_is_not_full(self):
        """测试棋盘未满"""
        self.board.make_move(7, 7, 1)
        self.assertFalse(self.board.is_full())

    def test_undo_move(self):
        """测试悔棋"""
        self.board.make_move(7, 7, 1)
        self.board.make_move(7, 8, 2)
        result = self.board.undo_move()
        self.assertEqual(result, (7, 8, 2))
        self.assertEqual(self.board.grid[7][8], 0)
        self.assertEqual(len(self.board.move_history), 1)

    def test_undo_move_empty_history(self):
        """测试空历史悔棋"""
        result = self.board.undo_move()
        self.assertIsNone(result)

    def test_get_winning_line_horizontal(self):
        """测试获取水平获胜线"""
        for i in range(5):
            self.board.make_move(7, 7 + i, 1)
        line = self.board.get_winning_line(1)
        self.assertIsNotNone(line)
        self.assertEqual(len(line), 5)
        self.assertEqual(line[0], (7, 7))
        self.assertEqual(line[-1], (7, 11))

    def test_get_winning_line_vertical(self):
        """测试获取垂直获胜线"""
        for i in range(5):
            self.board.make_move(7 + i, 7, 1)
        line = self.board.get_winning_line(1)
        self.assertIsNotNone(line)
        self.assertEqual(len(line), 5)

    def test_get_winning_line_none(self):
        """测试无获胜线"""
        self.board.make_move(7, 7, 1)
        line = self.board.get_winning_line(1)
        self.assertIsNone(line)

    def test_move_history(self):
        """测试落子历史记录"""
        self.board.make_move(7, 7, 1)
        self.board.make_move(7, 8, 2)
        self.assertEqual(len(self.board.move_history), 2)
        self.assertEqual(self.board.move_history[0], (7, 7, 1))
        self.assertEqual(self.board.move_history[1], (7, 8, 2))


if __name__ == '__main__':
    unittest.main()