import pygame
import sys
import os

# 初始化pygame
pygame.init()
pygame.mixer.init()

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

class PieceAnimation:
    def __init__(self, row, col, player, start_time):
        self.row = row
        self.col = col
        self.player = player
        self.start_time = start_time
        self.duration = 200  # 动画持续时间（毫秒）
        self.scale = 0.0  # 初始缩放
    
    def update(self, current_time):
        elapsed = current_time - self.start_time
        if elapsed < self.duration:
            # 缩放从0到1
            self.scale = elapsed / self.duration
            return True  # 动画仍在进行
        else:
            self.scale = 1.0
            return False  # 动画结束
    
    def draw(self, surface, cell_size, margin):
        if self.scale <= 0:
            return
        
        center_x = margin + self.col * cell_size
        center_y = margin + self.row * cell_size
        radius = (cell_size // 2 - 2) * self.scale
        
        color = BLACK if self.player == 1 else WHITE
        border_color = WHITE if self.player == 1 else BLACK
        
        # 绘制棋子
        pygame.draw.circle(surface, color, (center_x, center_y), int(radius))
        # 绘制边框
        if radius > 2:
            pygame.draw.circle(surface, border_color, (center_x, center_y), int(radius), 2)


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

class GomokuAI:
    """简单AI玩家"""
    def __init__(self, player=2):
        self.player = player  # AI执白棋
        self.opponent = 1 if player == 2 else 2
    
    def get_move(self, board):
        """获取AI落子位置"""
        # 1. 检查AI是否能赢
        win_move = self._find_winning_move(board, self.player)
        if win_move:
            return win_move
        
        # 2. 检查对手是否能赢，进行阻挡
        block_move = self._find_winning_move(board, self.opponent)
        if block_move:
            return block_move
        
        # 3. 寻找最佳进攻位置
        best_move = self._find_best_move(board)
        if best_move:
            return best_move
        
        # 4. 如果棋盘为空，下在中心
        center = board.size // 2
        if board.grid[center][center] == 0:
            return (center, center)
        
        # 5. 随机找一个空位
        return self._find_random_move(board)
    
    def _find_winning_move(self, board, player):
        """找到能形成五连的落子位置"""
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == 0:
                    # 尝试落子
                    board.grid[row][col] = player
                    if board.check_win(player):
                        board.grid[row][col] = 0
                        return (row, col)
                    board.grid[row][col] = 0
        return None
    
    def _find_best_move(self, board):
        """找到最佳进攻位置（基于评分）"""
        best_score = -1
        best_move = None
        
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == 0:
                    score = self._evaluate_position(board, row, col)
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        return best_move
    
    def _evaluate_position(self, board, row, col):
        """评估某个位置的价值"""
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            # 检查两个方向
            for direction in [1, -1]:
                count = 0
                empty = 0
                for i in range(1, 5):
                    r, c = row + dr * i * direction, col + dc * i * direction
                    if 0 <= r < board.size and 0 <= c < board.size:
                        if board.grid[r][c] == self.player:
                            count += 1
                        elif board.grid[r][c] == 0:
                            empty += 1
                            break
                        else:
                            break
                
                # 评分规则
                if count >= 4:
                    score += 10000  # 活四
                elif count == 3 and empty > 0:
                    score += 1000   # 活三
                elif count == 2 and empty > 0:
                    score += 100    # 活二
                elif count == 1 and empty > 0:
                    score += 10     # 活一
        
        # 中心位置加分
        center = board.size // 2
        distance = abs(row - center) + abs(col - center)
        score += max(0, 15 - distance)
        
        return score
    
    def _find_random_move(self, board):
        """随机找一个空位"""
        import random
        empty_positions = []
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == 0:
                    empty_positions.append((row, col))
        
        if empty_positions:
            return random.choice(empty_positions)
        return None


# 游戏状态常量
STATE_MENU = 0
STATE_PVP = 1
STATE_PVAI = 2


class GomokuGUI:
    def __init__(self):
        self.board = Board()
        self.current_player = 1  # 1: 黑棋, 2: 白棋
        self.game_over = False
        self.winner = None
        
        # 游戏状态
        self.game_state = STATE_MENU
        self.ai = None
        
        # 创建窗口
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("五子棋游戏")
        
        # 字体（使用 pygame 默认字体避免 SysFont bug）
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        
        # 音效
        self.sounds = {}
        self.load_sounds()
        
        # 动画
        self.animations = []  # 存储动画对象
        
        # 菜单按钮
        self.menu_buttons = []
        self._create_menu_buttons()
    
    def load_sounds(self):
        # 加载音效文件（如果存在）
        sound_files = {
            'place': 'sounds/place.wav',
            'win': 'sounds/win.wav',
            'draw': 'sounds/draw.wav'
        }
        
        for name, file_path in sound_files.items():
            if os.path.exists(file_path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(file_path)
                except:
                    print(f"警告：无法加载音效 {file_path}")
            else:
                print(f"提示：音效文件 {file_path} 不存在，将静音播放")
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def _create_menu_buttons(self):
        """创建菜单按钮"""
        button_width = 200
        button_height = 50
        start_x = (WINDOW_SIZE - button_width) // 2
        start_y = WINDOW_SIZE // 2 - 30
        
        self.menu_buttons = [
            {"rect": pygame.Rect(start_x, start_y, button_width, button_height),
             "text": "双人对战", "state": STATE_PVP},
            {"rect": pygame.Rect(start_x, start_y + 70, button_width, button_height),
             "text": "人机对战", "state": STATE_PVAI}
        ]
    
    def draw_menu(self):
        """绘制菜单界面"""
        self.screen.fill(BG_COLOR)
        
        # 标题
        title = self.large_font.render("五子棋游戏", True, BLACK)
        self.screen.blit(title, (WINDOW_SIZE // 2 - title.get_width() // 2, WINDOW_SIZE // 4))
        
        # 按钮
        for button in self.menu_buttons:
            # 按钮背景
            pygame.draw.rect(self.screen, WHITE, button["rect"])
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2)
            
            # 按钮文字
            text = self.font.render(button["text"], True, BLACK)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
        
        # 提示
        hint = self.small_font.render("选择游戏模式开始", True, GRAY)
        self.screen.blit(hint, (WINDOW_SIZE // 2 - hint.get_width() // 2, WINDOW_SIZE - 80))
    
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
        # 创建动画位置集合，用于跳过静态绘制
        animating_positions = {(anim.row, anim.col) for anim in self.animations}
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board.grid[row][col] != 0 and (row, col) not in animating_positions:
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
                if self.game_state == STATE_PVAI:
                    if self.winner == 1:
                        status_text = "游戏结束！你赢了！"
                    else:
                        status_text = "游戏结束！AI获胜！"
                else:
                    status_text = f"游戏结束！{winner_name}获胜！"
            else:
                status_text = "游戏结束！平局！"
        else:
            player_name = "黑棋" if self.current_player == 1 else "白棋"
            if self.game_state == STATE_PVAI:
                if self.current_player == 1:
                    status_text = "你的回合（黑棋）"
                else:
                    status_text = "AI思考中..."
            else:
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
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == STATE_MENU:
                        # 菜单点击处理
                        for button in self.menu_buttons:
                            if button["rect"].collidepoint(event.pos):
                                self.game_state = button["state"]
                                if self.game_state == STATE_PVAI:
                                    self.ai = GomokuAI(player=2)
                                break
                    elif not self.game_over:
                        # 游戏中点击处理
                        pos = self.get_grid_pos(event.pos)
                        if pos:
                            row, col = pos
                            # 人机模式下，只允许玩家在自己的回合落子
                            if self.game_state == STATE_PVAI and self.current_player == 2:
                                continue
                            
                            if self.board.make_move(row, col, self.current_player):
                                self.play_sound('place')
                                current_time = pygame.time.get_ticks()
                                animation = PieceAnimation(row, col, self.current_player, current_time)
                                self.animations.append(animation)
                                
                                if self.board.check_win(self.current_player):
                                    self.game_over = True
                                    self.winner = self.current_player
                                    self.play_sound('win')
                                elif self.board.is_full():
                                    self.game_over = True
                                    self.play_sound('draw')
                                else:
                                    self.current_player = 2 if self.current_player == 1 else 1
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 按R键重新开始
                        self.game_state = STATE_MENU
                        self.board = Board()
                        self.current_player = 1
                        self.game_over = False
                        self.winner = None
                        self.ai = None
                        self.animations = []
            
            # 绘制界面
            if self.game_state == STATE_MENU:
                self.draw_menu()
            else:
                self.draw_board()
                self.draw_pieces()
                
                # 更新和绘制动画
                current_time = pygame.time.get_ticks()
                completed_animations = []
                for animation in self.animations:
                    if not animation.update(current_time):
                        completed_animations.append(animation)
                    else:
                        animation.draw(self.screen, CELL_SIZE, MARGIN)
                
                for animation in completed_animations:
                    self.animations.remove(animation)
                
                self.draw_status()
                
                # AI回合
                if (self.game_state == STATE_PVAI and 
                    self.current_player == 2 and 
                    not self.game_over and 
                    not self.animations):
                    self._ai_move()
            
            pygame.display.flip()
            clock.tick(30)
    
    def _ai_move(self):
        """AI落子"""
        if self.ai:
            move = self.ai.get_move(self.board)
            if move:
                row, col = move
                if self.board.make_move(row, col, self.current_player):
                    self.play_sound('place')
                    current_time = pygame.time.get_ticks()
                    animation = PieceAnimation(row, col, self.current_player, current_time)
                    self.animations.append(animation)
                    
                    if self.board.check_win(self.current_player):
                        self.game_over = True
                        self.winner = self.current_player
                        self.play_sound('win')
                    elif self.board.is_full():
                        self.game_over = True
                        self.play_sound('draw')
                    else:
                        self.current_player = 2 if self.current_player == 1 else 1

if __name__ == "__main__":
    game = GomokuGUI()
    game.run()