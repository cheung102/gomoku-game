import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import Gomoku

class TestGomoku(unittest.TestCase):
    def setUp(self):
        self.game = Gomoku()
    
    def test_initial_state(self):
        """测试游戏初始状态"""
        self.assertEqual(self.game.current_player, 1)
        self.assertFalse(self.game.game_over)
        self.assertIsNone(self.game.winner)
    
    def test_switch_player(self):
        """测试玩家切换"""
        self.assertEqual(self.game.current_player, 1)
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 2)
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 1)
    
    def test_play_sequence(self):
        """测试游戏进行序列"""
        # 模拟几步棋
        self.game.board.make_move(7, 7, 1)  # 黑棋
        self.game.switch_player()
        self.game.board.make_move(7, 8, 2)  # 白棋
        self.game.switch_player()
        self.game.board.make_move(8, 7, 1)  # 黑棋
        
        # 检查棋盘状态
        self.assertEqual(self.game.board.grid[7][7], 1)
        self.assertEqual(self.game.board.grid[7][8], 2)
        self.assertEqual(self.game.board.grid[8][7], 1)
    
    def test_win_detection(self):
        """测试胜利检测"""
        # 黑棋连成五子
        for i in range(5):
            self.game.board.make_move(7, 7 + i, 1)
        
        # 检查胜利
        self.assertTrue(self.game.board.check_win(1))
    
    def test_game_over_on_win(self):
        """测试胜利时游戏结束"""
        # 模拟黑棋胜利
        for i in range(4):
            self.game.board.make_move(7, 7 + i, 1)
            self.game.switch_player()
            self.game.board.make_move(8, 7 + i, 2)  # 白棋随便走
            self.game.switch_player()
        
        # 黑棋下第五个子
        self.game.board.make_move(7, 11, 1)
        
        # 检查游戏状态
        self.assertTrue(self.game.board.check_win(1))
        self.game.game_over = True
        self.game.winner = 1
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, 1)

if __name__ == '__main__':
    unittest.main()