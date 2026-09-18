#!/usr/bin/env python3
"""
五子棋游戏演示脚本
演示游戏的基本功能
"""

from game import Board, Gomoku

def demo_board():
    """演示棋盘功能"""
    print("=== 棋盘功能演示 ===")
    board = Board(15)
    
    # 放置一些棋子
    moves = [
        (7, 7, 1),   # 黑棋
        (7, 8, 2),   # 白棋
        (8, 7, 1),   # 黑棋
        (8, 8, 2),   # 白棋
        (9, 7, 1),   # 黑棋
    ]
    
    for row, col, player in moves:
        board.make_move(row, col, player)
        player_name = "黑棋" if player == 1 else "白棋"
        print(f"{player_name} 落子 ({row}, {col})")
    
    print("\n当前棋盘状态:")
    board.display()
    
    # 检查是否有赢家
    if board.check_win(1):
        print("\n黑棋获胜！")
    elif board.check_win(2):
        print("\n白棋获胜！")
    else:
        print("\n暂无赢家")

def demo_game():
    """演示游戏流程"""
    print("\n=== 游戏流程演示 ===")
    game = Gomoku()
    
    # 模拟几步棋
    moves = [
        (7, 7),  # 黑棋
        (7, 8),  # 白棋
        (8, 7),  # 黑棋
        (8, 8),  # 白棋
        (9, 7),  # 黑棋
        (9, 8),  # 白棋
        (10, 7), # 黑棋
        (10, 8), # 白棋
        (11, 7), # 黑棋 - 黑棋连成五子
    ]
    
    for i, (row, col) in enumerate(moves):
        player_name = "黑棋" if game.current_player == 1 else "白棋"
        print(f"第{i+1}步: {player_name} 落子 ({row}, {col})")
        
        # 落子
        game.board.make_move(row, col, game.current_player)
        
        # 检查胜利
        if game.board.check_win(game.current_player):
            print(f"\n{player_name} 获胜！")
            game.game_over = True
            game.winner = game.current_player
            break
        
        # 切换玩家
        game.switch_player()
    
    print("\n最终棋盘状态:")
    game.board.display()

if __name__ == "__main__":
    demo_board()
    demo_game()