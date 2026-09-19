"""
五子棋 UI 组件模块
包含按钮、信息面板、动画等可复用组件
"""

import pygame


class Button:
    """可交互按钮组件"""

    def __init__(self, x, y, width, height, text, callback, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = font
        self.hovered = False
        self.enabled = True
        self.normal_color = (255, 255, 255)
        self.hover_color = (200, 200, 255)
        self.disabled_color = (180, 180, 180)
        self.border_color = (0, 0, 0)

    def draw(self, surface):
        if not self.enabled:
            color = self.disabled_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.normal_color

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)

        if self.font:
            text_surf = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False


class InfoPanel:
    """右侧信息面板"""

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw(self, surface, game_state, fonts, score, elapsed_time, move_count):
        pygame.draw.rect(surface, (240, 240, 240), self.rect)
        pygame.draw.line(surface, (0, 0, 0), 
                        (self.rect.x, self.rect.y),
                        (self.rect.x, self.rect.y + self.rect.height), 2)

        title_font, normal_font, small_font = fonts
        x = self.rect.x + 15
        y = self.rect.y + 15

        title = title_font.render("游戏信息", True, (0, 0, 0))
        surface.blit(title, (x, y))
        y += 40

        pygame.draw.line(surface, (150, 150, 150), (x, y), (x + 250, y), 1)
        y += 15

        mode_text = "人机对战" if game_state.get('mode') == 'pvai' else "双人对战"
        difficulty = game_state.get('difficulty', 'medium')
        diff_text = {'easy': '简单', 'medium': '中等', 'hard': '困难'}.get(difficulty, '中等')
        info_lines = [
            f"模式: {mode_text}",
            f"难度: {diff_text}" if game_state.get('mode') == 'pvai' else "",
            f"回合: 第{move_count}手",
            f"用时: {elapsed_time}",
        ]
        for line in info_lines:
            if line:
                text = normal_font.render(line, True, (50, 50, 50))
                surface.blit(text, (x, y))
                y += 28

        y += 10
        pygame.draw.line(surface, (150, 150, 150), (x, y), (x + 250, y), 1)
        y += 15

        score_title = normal_font.render("比分", True, (0, 0, 0))
        surface.blit(score_title, (x, y))
        y += 30

        black_score = normal_font.render(f"黑棋: {score.get(1, 0)} 胜", True, (0, 0, 0))
        surface.blit(black_score, (x, y))
        y += 25

        white_score = normal_font.render(f"白棋: {score.get(2, 0)} 胜", True, (100, 100, 100))
        surface.blit(white_score, (x, y))
        y += 35

        pygame.draw.line(surface, (150, 150, 150), (x, y), (x + 250, y), 1)
        y += 15

        hint_text = small_font.render("快捷键: Z-悔棋 H-提示 R-重来", True, (100, 100, 100))
        surface.blit(hint_text, (x, y))

        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        for button in self.buttons:
            if button.handle_event(event):
                return True
        return False


class PieceAnimation:
    """棋子落子动画"""

    def __init__(self, row, col, player, start_time):
        self.row = row
        self.col = col
        self.player = player
        self.start_time = start_time
        self.duration = 200
        self.scale = 0.0

    def update(self, current_time):
        elapsed = current_time - self.start_time
        if elapsed < self.duration:
            self.scale = elapsed / self.duration
            return True
        else:
            self.scale = 1.0
            return False

    def draw(self, surface, cell_size, margin):
        if self.scale <= 0:
            return
        center_x = margin + self.col * cell_size
        center_y = margin + self.row * cell_size
        radius = (cell_size // 2 - 2) * self.scale
        color = (0, 0, 0) if self.player == 1 else (255, 255, 255)
        border_color = (255, 255, 255) if self.player == 1 else (0, 0, 0)
        pygame.draw.circle(surface, color, (center_x, center_y), int(radius))
        if radius > 2:
            pygame.draw.circle(surface, border_color, (center_x, center_y), int(radius), 2)


class LastMoveMarker:
    """最后落子标记"""

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def draw(self, surface, cell_size, margin):
        center_x = margin + self.col * cell_size
        center_y = margin + self.row * cell_size
        size = 5
        points = [
            (center_x, center_y - size - 2),
            (center_x + size + 2, center_y),
            (center_x, center_y + size + 2),
            (center_x - size - 2, center_y),
        ]
        pygame.draw.polygon(surface, (255, 0, 0), points)


class WinningLineAnimation:
    """获胜连线动画"""

    def __init__(self, line, start_time):
        self.line = line
        self.start_time = start_time
        self.duration = 500
        self.progress = 0.0

    def update(self, current_time):
        elapsed = current_time - self.start_time
        if elapsed < self.duration:
            self.progress = min(1.0, elapsed / self.duration)
            return True
        self.progress = 1.0
        return False

    def draw(self, surface, cell_size, margin):
        if len(self.line) < 2 or self.progress <= 0:
            return
        start = (margin + self.line[0][1] * cell_size,
                margin + self.line[0][0] * cell_size)
        end_x = start[0] + (margin + self.line[-1][1] * cell_size - start[0]) * self.progress
        end_y = start[1] + (margin + self.line[-1][0] * cell_size - start[1]) * self.progress
        pygame.draw.line(surface, (255, 0, 0), start, (int(end_x), int(end_y)), 4)


class HoverPreview:
    """鼠标悬停预览"""

    def __init__(self):
        self.row = -1
        self.col = -1
        self.visible = False
        self.current_player = 1

    def update(self, mouse_pos, board, cell_size, margin, board_size, current_player, game_over):
        if game_over:
            self.visible = False
            return
        x, y = mouse_pos
        col = round((x - margin) / cell_size)
        row = round((y - margin) / cell_size)
        if (0 <= row < board_size and 0 <= col < board_size and
                board.grid[row][col] == 0):
            self.row = row
            self.col = col
            self.visible = True
            self.current_player = current_player
        else:
            self.visible = False

    def draw(self, surface, cell_size, margin):
        if not self.visible:
            return
        center_x = margin + self.col * cell_size
        center_y = margin + self.row * cell_size
        radius = cell_size // 2 - 2
        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        if self.current_player == 1:
            color = (0, 0, 0, 80)
        else:
            color = (255, 255, 255, 80)
        pygame.draw.circle(s, color, (radius, radius), radius)
        surface.blit(s, (center_x - radius, center_y - radius))
