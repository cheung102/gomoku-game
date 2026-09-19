class Board:
    def __init__(self, size=15):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.move_history = []

    def is_valid_move(self, row, col):
        return (0 <= row < self.size and
                0 <= col < self.size and
                self.grid[row][col] == 0)

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.grid[row][col] = player
            self.move_history.append((row, col, player))
            return True
        return False

    def undo_move(self):
        if self.move_history:
            row, col, player = self.move_history.pop()
            self.grid[row][col] = 0
            return (row, col, player)
        return None

    def get_winning_line(self, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == player:
                    for dr, dc in directions:
                        line = [(row, col)]
                        for i in range(1, 5):
                            r, c = row + dr * i, col + dc * i
                            if (0 <= r < self.size and
                                0 <= c < self.size and
                                self.grid[r][c] == player):
                                line.append((r, c))
                            else:
                                break
                        if len(line) >= 5:
                            return line[:5]
        return None

    def check_win(self, player):
        return self.get_winning_line(player) is not None

    def is_full(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return False
        return True
    
    def display(self):
        # 打印列号
        print("   ", end="")
        for col in range(self.size):
            print(f"{col:2d}", end=" ")
        print()
        
        for row in range(self.size):
            print(f"{row:2d} ", end="")
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    print(" .", end=" ")
                elif self.grid[row][col] == 1:
                    print(" X", end=" ")  # 黑棋
                else:
                    print(" O", end=" ")  # 白棋
            print()


class Gomoku:
    def __init__(self):
        self.board = Board()
        self.current_player = 1  # 1: 黑棋, 2: 白棋
        self.game_over = False
        self.winner = None
    
    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
    
    def play(self):
        print("五子棋游戏开始！")
        print("黑棋(X)先手，白棋(O)后手")
        print("输入格式：行 列 (例如：7 7)")
        print("输入 'quit' 退出游戏")
        print()
        
        self.board.display()
        
        while not self.game_over:
            player_name = "黑棋(X)" if self.current_player == 1 else "白棋(O)"
            move_input = input(f"\n{player_name} 请输入落子位置: ").strip()
            
            if move_input.lower() == 'quit':
                print("游戏结束！")
                break
            
            try:
                row, col = map(int, move_input.split())
                if self.board.make_move(row, col, self.current_player):
                    self.board.display()
                    
                    if self.board.check_win(self.current_player):
                        print(f"\n{player_name} 获胜！")
                        self.game_over = True
                        self.winner = self.current_player
                    elif self.board.is_full():
                        print("\n平局！棋盘已满。")
                        self.game_over = True
                    else:
                        self.switch_player()
                else:
                    print("无效落子位置，请重新输入。")
            except ValueError:
                print("输入格式错误，请输入两个数字（行 列），用空格分隔。")
        
        print("游戏结束，感谢游玩！")


if __name__ == "__main__":
    game = Gomoku()
    game.play()