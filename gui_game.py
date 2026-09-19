"""
五子棋游戏 - GUI 版本
支持双人对战和人机对战
集成悔棋、提示、难度选择、胜负统计等功能
"""

import pygame
import sys
import os

from game import Board
from ai_player import GomokuAI
from ui_components import (
    Button, InfoPanel, PieceAnimation, LastMoveMarker,
    WinningLineAnimation, HoverPreview
)

# 初始化 pygame
pygame.init()
pygame.mixer.init()

# 常量定义
BOARD_SIZE = 15
BOARD_PIXELS = 600
PANEL_WIDTH = 300
WINDOW_WIDTH = BOARD_PIXELS + PANEL_WIDTH
WINDOW_HEIGHT = 650
MARGIN = 30
CELL_SIZE = (BOARD_PIXELS - 2 * MARGIN) // (BOARD_SIZE - 1)

# 颜色定义
BG_COLOR = (220, 179, 92)
BOARD_COLOR = (210, 170, 80)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
GRAY = (128, 128, 128)
GREEN = (50, 150, 50)
PANEL_BG = (245, 245, 240)

# 游戏状态
STATE_MENU = 0
STATE_DIFFICULTY = 1
STATE_PVP = 2
STATE_PVAI = 3
STATE_GAME_OVER = 4


class GomokuGUI:
    def __init__(self):
        self.board = Board()
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.game_state = STATE_MENU
        self.ai = None
        self.difficulty = 'medium'

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("五子棋游戏")

        self.font = self._load_chinese_font(24)
        self.large_font = self._load_chinese_font(36)
        self.small_font = self._load_chinese_font(18)
        self.title_font = self._load_chinese_font(28)

        self.sounds = {}
        self.load_sounds()

        self.animations = []
        self.winning_animation = None
        self.last_move_marker = None
        self.hover_preview = HoverPreview()
        self.hint_positions = []

        self.score = {1: 0, 2: 0}
        self.game_start_time = 0
        self.move_count = 0

        self._create_menu()

    def _load_chinese_font(self, size):
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/msyhbd.ttc",
        ]
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, size)
                except:
                    continue
        return pygame.font.Font(None, size)

    def load_sounds(self):
        sound_files = {
            'place': 'sounds/place.wav',
            'win': 'sounds/win.wav',
            'draw': 'sounds/draw.wav',
            'undo': 'sounds/undo.wav',
            'hint': 'sounds/hint.wav',
            'click': 'sounds/click.wav',
        }
        for name, file_path in sound_files.items():
            if os.path.exists(file_path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(file_path)
                except:
                    pass

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
            self.sounds[sound_name].play()

    def _create_menu(self):
        btn_width = 220
        btn_height = 50
        start_x = MARGIN + (BOARD_PIXELS - btn_width) // 2
        start_y = BOARD_PIXELS // 2 - 80

        self.menu_buttons = [
            Button(start_x, start_y, btn_width, btn_height,
                   "双人对战", self._start_pvp, self.font),
            Button(start_x, start_y + 70, btn_width, btn_height,
                   "人机对战", self._show_difficulty, self.font),
        ]

        diff_y = BOARD_PIXELS // 2 - 60
        self.difficulty_buttons = [
            Button(start_x, diff_y, btn_width, btn_height,
                   "简单", lambda: self._start_pvai('easy'), self.font),
            Button(start_x, diff_y + 70, btn_width, btn_height,
                   "中等", lambda: self._start_pvai('medium'), self.font),
            Button(start_x, diff_y + 140, btn_width, btn_height,
                   "困难", lambda: self._start_pvai('hard'), self.font),
            Button(start_x, diff_y + 210, btn_width, btn_height,
                   "返回", self._back_to_menu, self.font),
        ]

        panel_x = BOARD_PIXELS + 15
        panel_btn_y = WINDOW_HEIGHT - 180
        self.game_buttons = [
            Button(panel_x, panel_btn_y, 130, 40,
                   "悔棋 (Z)", self._undo_move, self.small_font),
            Button(panel_x + 140, panel_btn_y, 130, 40,
                   "提示 (H)", self._show_hint, self.small_font),
            Button(panel_x, panel_btn_y + 50, 130, 40,
                   "重玩 (R)", self._restart_game, self.small_font),
            Button(panel_x + 140, panel_btn_y + 50, 130, 40,
                   "菜单 (Esc)", self._back_to_menu, self.small_font),
        ]

        self.info_panel = InfoPanel(BOARD_PIXELS, 0, PANEL_WIDTH, WINDOW_HEIGHT)

    def _start_pvp(self):
        self.game_state = STATE_PVP
        self.ai = None
        self._reset_game()
        self.play_sound('click')

    def _show_difficulty(self):
        self.game_state = STATE_DIFFICULTY
        self.play_sound('click')

    def _start_pvai(self, difficulty):
        self.game_state = STATE_PVAI
        self.difficulty = difficulty
        self.ai = GomokuAI(player=2, difficulty=difficulty)
        self._reset_game()
        self.play_sound('click')

    def _back_to_menu(self):
        self.game_state = STATE_MENU
        self.play_sound('click')

    def _reset_game(self):
        self.board = Board()
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.animations = []
        self.winning_animation = None
        self.last_move_marker = None
        self.hint_positions = []
        self.move_count = 0
        self.game_start_time = pygame.time.get_ticks()

    def _restart_game(self):
        self._reset_game()
        self.play_sound('click')

    def _undo_move(self):
        if self.game_over or self.move_count == 0:
            return
        if self.game_state == STATE_PVAI:
            if len(self.board.move_history) >= 2:
                self.board.undo_move()
                self.board.undo_move()
                self.current_player = 1
                self.move_count -= 2
        else:
            self.board.undo_move()
            self.current_player = 2 if self.current_player == 1 else 1
            self.move_count -= 1
        self.hint_positions = []
        self.winning_animation = None
        if self.board.move_history:
            last = self.board.move_history[-1]
            self.last_move_marker = LastMoveMarker(last[0], last[1])
        else:
            self.last_move_marker = None
        self.play_sound('undo')

    def _show_hint(self):
        if self.game_over or self.ai is None:
            return
        if self.game_state == STATE_PVAI and self.current_player != 1:
            return
        self.hint_positions = self.ai.get_hint_positions(self.board, num_hints=3)
        self.play_sound('hint')

    def _make_move(self, row, col):
        if self.board.make_move(row, col, self.current_player):
            self.play_sound('place')
            self.move_count += 1
            current_time = pygame.time.get_ticks()
            animation = PieceAnimation(row, col, self.current_player, current_time)
            self.animations.append(animation)
            self.last_move_marker = LastMoveMarker(row, col)
            self.hint_positions = []

            if self.board.check_win(self.current_player):
                self.game_over = True
                self.winner = self.current_player
                self.score[self.current_player] += 1
                winning_line = self.board.get_winning_line(self.current_player)
                if winning_line:
                    self.winning_animation = WinningLineAnimation(winning_line, current_time)
                self.play_sound('win')
            elif self.board.is_full():
                self.game_over = True
                self.play_sound('draw')
            else:
                self.current_player = 2 if self.current_player == 1 else 1
            return True
        return False

    def _ai_move(self):
        if self.ai and not self.game_over:
            move = self.ai.get_move(self.board)
            if move:
                self._make_move(move[0], move[1])

    def get_grid_pos(self, mouse_pos):
        x, y = mouse_pos
        if x > BOARD_PIXELS:
            return None
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - MARGIN) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None

    def _get_elapsed_time(self):
        if self.game_start_time:
            elapsed = (pygame.time.get_ticks() - self.game_start_time) // 1000
            minutes = elapsed // 60
            seconds = elapsed % 60
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"

    def draw_menu(self):
        self.screen.fill(BOARD_COLOR)
        title = self.large_font.render("五子棋游戏", True, BLACK)
        self.screen.blit(title, (MARGIN + (BOARD_PIXELS - title.get_width()) // 2, 150))

        for btn in self.menu_buttons:
            btn.draw(self.screen)

        hint = self.small_font.render("选择游戏模式开始", True, GRAY)
        self.screen.blit(hint, (MARGIN + (BOARD_PIXELS - hint.get_width()) // 2, BOARD_PIXELS - 100))

    def draw_difficulty(self):
        self.screen.fill(BOARD_COLOR)
        title = self.large_font.render("选择难度", True, BLACK)
        self.screen.blit(title, (MARGIN + (BOARD_PIXELS - title.get_width()) // 2, 120))

        for btn in self.difficulty_buttons:
            btn.draw(self.screen)

    def draw_board(self):
        self.screen.fill(BOARD_COLOR)
        pygame.draw.rect(self.screen, BOARD_COLOR, (0, 0, BOARD_PIXELS, WINDOW_HEIGHT))

        for i in range(BOARD_SIZE):
            pygame.draw.line(self.screen, BLACK,
                           (MARGIN, MARGIN + i * CELL_SIZE),
                           (MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, MARGIN + i * CELL_SIZE), 1)
            pygame.draw.line(self.screen, BLACK,
                           (MARGIN + i * CELL_SIZE, MARGIN),
                           (MARGIN + i * CELL_SIZE, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE), 1)

        star_points = [(3, 3), (3, 7), (3, 11), (7, 3), (7, 7), (7, 11), (11, 3), (11, 7), (11, 11)]
        for r, c in star_points:
            center = (MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE)
            pygame.draw.circle(self.screen, BLACK, center, 4)

        for i in range(BOARD_SIZE):
            text = self.small_font.render(str(i), True, BLACK)
            self.screen.blit(text, (MARGIN + i * CELL_SIZE - 5, 5))
            text = self.small_font.render(str(i), True, BLACK)
            self.screen.blit(text, (5, MARGIN + i * CELL_SIZE - 8))

    def draw_pieces(self):
        animating_positions = {(anim.row, anim.col) for anim in self.animations}
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board.grid[row][col] != 0 and (row, col) not in animating_positions:
                    color = BLACK if self.board.grid[row][col] == 1 else WHITE
                    center = (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
                    radius = CELL_SIZE // 2 - 2
                    pygame.draw.circle(self.screen, color, center, radius)
                    border_color = WHITE if self.board.grid[row][col] == 1 else BLACK
                    pygame.draw.circle(self.screen, border_color, center, radius, 2)

    def draw_hints(self):
        if self.hint_positions:
            for i, (row, col) in enumerate(self.hint_positions):
                center = (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
                pygame.draw.circle(self.screen, GREEN, center, 10)
                text = self.small_font.render(str(i + 1), True, WHITE)
                text_rect = text.get_rect(center=center)
                self.screen.blit(text, text_rect)

    def draw_panel(self):
        game_state = {
            'mode': 'pvai' if self.game_state == STATE_PVAI else 'pvp',
            'difficulty': self.difficulty,
        }
        fonts = (self.font, self.small_font, self.small_font)
        self.info_panel.draw(self.screen, game_state, fonts,
                            self.score, self._get_elapsed_time(), self.move_count)

        for btn in self.game_buttons:
            btn.enabled = not self.game_over and self.move_count > 0
            if btn.text.startswith("提示"):
                btn.enabled = not self.game_over and self.ai is not None
            if btn.text.startswith("重玩") or btn.text.startswith("菜单"):
                btn.enabled = True
            btn.draw(self.screen)

        if self.game_over:
            if self.winner:
                winner_text = "黑棋获胜！" if self.winner == 1 else "白棋获胜！"
                if self.game_state == STATE_PVAI:
                    winner_text = "你赢了！" if self.winner == 1 else "AI获胜！"
            else:
                winner_text = "平局！"
            text = self.font.render(winner_text, True, RED)
            text_rect = text.get_rect(center=(BOARD_PIXELS + PANEL_WIDTH // 2, WINDOW_HEIGHT - 60))
            pygame.draw.rect(self.screen, PANEL_BG,
                           (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10))
            self.screen.blit(text, text_rect)

    def draw_status(self):
        if self.game_over:
            return
        if self.game_state == STATE_PVAI:
            if self.current_player == 1:
                status_text = "你的回合（黑棋）"
            else:
                status_text = "AI思考中..."
        else:
            player_name = "黑棋" if self.current_player == 1 else "白棋"
            status_text = f"当前回合：{player_name}"
        text = self.font.render(status_text, True, BLACK)
        self.screen.blit(text, (10, BOARD_PIXELS + 10))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state in (STATE_PVP, STATE_PVAI, STATE_GAME_OVER):
                            self.game_state = STATE_MENU
                        elif self.game_state == STATE_DIFFICULTY:
                            self.game_state = STATE_MENU
                    elif event.key == pygame.K_r:
                        if self.game_state in (STATE_PVP, STATE_PVAI):
                            self._restart_game()
                    elif event.key == pygame.K_z:
                        if self.game_state in (STATE_PVP, STATE_PVAI):
                            self._undo_move()
                    elif event.key == pygame.K_h:
                        if self.game_state in (STATE_PVP, STATE_PVAI):
                            self._show_hint()

                if self.game_state == STATE_MENU:
                    for btn in self.menu_buttons:
                        btn.handle_event(event)
                elif self.game_state == STATE_DIFFICULTY:
                    for btn in self.difficulty_buttons:
                        btn.handle_event(event)
                elif self.game_state in (STATE_PVP, STATE_PVAI):
                    for btn in self.game_buttons:
                        btn.handle_event(event)

                    if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                        pos = self.get_grid_pos(event.pos)
                        if pos:
                            row, col = pos
                            if self.game_state == STATE_PVAI and self.current_player == 2:
                                continue
                            self._make_move(row, col)

            if self.game_state == STATE_MENU:
                self.draw_menu()
            elif self.game_state == STATE_DIFFICULTY:
                self.draw_difficulty()
            elif self.game_state in (STATE_PVP, STATE_PVAI):
                self.draw_board()
                self.draw_hints()

                if self.last_move_marker and not self.game_over:
                    self.last_move_marker.draw(self.screen, CELL_SIZE, MARGIN)

                self.draw_pieces()

                current_time = pygame.time.get_ticks()
                completed_animations = []
                for animation in self.animations:
                    if not animation.update(current_time):
                        completed_animations.append(animation)
                    else:
                        animation.draw(self.screen, CELL_SIZE, MARGIN)
                for animation in completed_animations:
                    self.animations.remove(animation)

                if self.winning_animation:
                    self.winning_animation.update(current_time)
                    self.winning_animation.draw(self.screen, CELL_SIZE, MARGIN)

                self.hover_preview.update(mouse_pos, self.board, CELL_SIZE, MARGIN,
                                        BOARD_SIZE, self.current_player, self.game_over)
                if not self.game_over:
                    self.hover_preview.draw(self.screen, CELL_SIZE, MARGIN)

                self.draw_panel()
                self.draw_status()

                if (self.game_state == STATE_PVAI and
                    self.current_player == 2 and
                    not self.game_over and
                    not self.animations):
                    self._ai_move()

            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    game = GomokuGUI()
    game.run()
