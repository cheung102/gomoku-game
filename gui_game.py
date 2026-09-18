import pygame
import sys

# 初始化pygame
pygame.init()

# 常量定义
BOARD_SIZE = 15  # 15x15棋盘
WINDOW_SIZE = 600  # 窗口大小
CELL_SIZE = WINDOW_SIZE // (BOARD_SIZE + 1)  # 格子大小，留边距
MARGIN = CELL_SIZE  # 边距

# 颜色定义
BG_COLOR = (220, 179, 92)  # 棋盘背景色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

class Board:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
    
    def is_valid_move(self, row, col):
        return (0 <= row < self.size and 
                0 <= col < self.size and 
                self.grid[row][col] == 0)
    
    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.grid[row][col] = player
            return True
        return False
    
    def check_win(self, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == player:
                    for dr, dc in directions:
                        count = 1
                        for i in range(1, 5):
                            r, c = row + dr * i, col + dc * i
                            if (0 <= r < self.size and 
                                0 <= c < self.size and 
                                self.grid[r][c] == player):
                                count += 1
                            else:
                                break
                        if count >= 5:
                            return True
        return False
    
    def is_full(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    return False
        return True

class GomokuGUI:
    def __init__(self):
        self.board = Board()
        self.current_player = 1  # 1: 黑棋, 2: 白棋
        self.game_over = False
        self.winner = None
        
        # 创建窗口
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("五子棋游戏")
        
        # 字体
        self.font = pygame.font.SysFont('SimHei', 24)
        self.small_font = pygame.font.SysFont('SimHei', 18)
    
    def draw_board(self):
        # 填充背景色
        self.screen.fill(BG_COLOR)
        
        # 绘制网格线
        for i in range(BOARD_SIZE):
            # 横线
            pygame.draw.line(self.screen, BLACK, 
                           (MARGIN, MARGIN + i * CELL_SIZE),
                           (MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, MARGIN + i * CELL_SIZE), 1)
            # 竖线
            pygame.draw.line(self.screen, BLACK,
                           (MARGIN + i * CELL_SIZE, MARGIN),
                           (MARGIN + i * CELL_SIZE, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE), 1)
        
        # 绘制坐标
        for i in range(BOARD_SIZE):
            # 列号
            text = self.small_font.render(str(i), True, BLACK)
            self.screen.blit(text, (MARGIN + i * CELL_SIZE - 5, 5))
            # 行号
            text = self.small_font.render(str(i), True, BLACK)
            self.screen.blit(text, (5, MARGIN + i * CELL_SIZE - 8))
    
    def draw_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board.grid[row][col] != 0:
                    color = BLACK if self.board.grid[row][col] == 1 else WHITE
                    center = (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
                    radius = CELL_SIZE // 2 - 2
                    pygame.draw.circle(self.screen, color, center, radius)
                    # 黑棋画白边，白棋画黑边
                    border_color = WHITE if self.board.grid[row][col] == 1 else BLACK
                    pygame.draw.circle(self.screen, border_color, center, radius, 2)
    
    def draw_status(self):
        # 绘制状态信息
        if self.game_over:
            if self.winner:
                winner_name = "黑棋" if self.winner == 1 else "白棋"
                status_text = f"游戏结束！{winner_name}获胜！"
            else:
                status_text = "游戏结束！平局！"
        else:
            player_name = "黑棋" if self.current_player == 1 else "白棋"
            status_text = f"当前回合：{player_name}"
        
        text = self.font.render(status_text, True, BLACK)
        self.screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, WINDOW_SIZE - 30))
    
    def get_grid_pos(self, mouse_pos):
        x, y = mouse_pos
        row = (y - MARGIN) // CELL_SIZE
        col = (x - MARGIN) // CELL_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = self.get_grid_pos(event.pos)
                    if pos:
                        row, col = pos
                        if self.board.make_move(row, col, self.current_player):
                            if self.board.check_win(self.current_player):
                                self.game_over = True
                                self.winner = self.current_player
                            elif self.board.is_full():
                                self.game_over = True
                            else:
                                self.current_player = 2 if self.current_player == 1 else 1
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 按R键重新开始
                        self.__init__()
            
            self.draw_board()
            self.draw_pieces()
            self.draw_status()
            
            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    game = GomokuGUI()
    game.run()