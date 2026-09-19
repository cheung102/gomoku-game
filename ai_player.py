"""
五子棋 AI 模块
支持简单、中等、困难三种难度
困难模式使用 Minimax + Alpha-Beta 剪枝算法
"""

import random


class GomokuAI:
    """五子棋 AI 玩家"""

    def __init__(self, player=2, difficulty='medium'):
        self.player = player
        self.opponent = 1 if player == 2 else 2
        self.difficulty = difficulty
        self.search_depth = {'easy': 1, 'medium': 2, 'hard': 3}.get(difficulty, 2)
        self.node_count = 0

    def get_move(self, board):
        if self.difficulty == 'easy':
            return self._easy_move(board)
        elif self.difficulty == 'medium':
            return self._medium_move(board)
        else:
            return self._hard_move(board)

    def get_hint_positions(self, board, num_hints=3):
        candidates = self._get_candidate_moves(board)
        if not candidates:
            return [(7, 7)]
        scored_moves = []
        for row, col in candidates:
            board.make_move(row, col, self.player)
            score = self._evaluate_board(board)
            board.undo_move()
            scored_moves.append(((row, col), score))
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        return [move for move, score in scored_moves[:num_hints]]

    # ==================== 简单难度 ====================

    def _easy_move(self, board):
        win_move = self._find_winning_move(board, self.player)
        if win_move:
            return win_move
        block_move = self._find_winning_move(board, self.opponent)
        if block_move:
            return block_move
        candidates = self._get_candidate_moves(board)
        if candidates:
            return random.choice(candidates)
        return (7, 7)

    # ==================== 中等难度 ====================

    def _medium_move(self, board):
        win_move = self._find_winning_move(board, self.player)
        if win_move:
            return win_move
        block_move = self._find_winning_move(board, self.opponent)
        if block_move:
            return block_move
        best_score = -float('inf')
        best_move = None
        candidates = self._get_candidate_moves(board)
        for row, col in candidates:
            score = self._evaluate_position(board, row, col)
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move if best_move else (7, 7)

    # ==================== 困难难度 ====================

    def _hard_move(self, board):
        self.node_count = 0
        candidates = self._get_candidate_moves(board)
        if not candidates:
            return (7, 7)
        if len(candidates) == 1:
            return candidates[0]
        best_score = -float('inf')
        best_move = candidates[0]
        candidates = self._pre_sort_moves(board, candidates)
        for row, col in candidates:
            board.make_move(row, col, self.player)
            score = self._minimax(board, self.search_depth - 1,
                                 -float('inf'), float('inf'), False)
            board.undo_move()
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move

    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        self.node_count += 1
        if board.check_win(self.player):
            return 100000 + depth
        if board.check_win(self.opponent):
            return -100000 - depth
        if depth == 0 or board.is_full():
            return self._evaluate_board(board)
        candidate_moves = self._get_candidate_moves(board)
        if len(candidate_moves) > 10:
            candidate_moves = self._pre_sort_moves(board, candidate_moves)[:10]
        if is_maximizing:
            max_eval = -float('inf')
            for row, col in candidate_moves:
                board.make_move(row, col, self.player)
                eval_score = self._minimax(board, depth - 1, alpha, beta, False)
                board.undo_move()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in candidate_moves:
                board.make_move(row, col, self.opponent)
                eval_score = self._minimax(board, depth - 1, alpha, beta, True)
                board.undo_move()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    # ==================== 辅助方法 ====================

    def _find_winning_move(self, board, player):
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == 0:
                    board.grid[row][col] = player
                    if board.check_win(player):
                        board.grid[row][col] = 0
                        return (row, col)
                    board.grid[row][col] = 0
        return None

    def _get_candidate_moves(self, board):
        candidates = set()
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] != 0:
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            r, c = row + dr, col + dc
                            if (0 <= r < board.size and
                                0 <= c < board.size and
                                board.grid[r][c] == 0):
                                candidates.add((r, c))
        return list(candidates) if candidates else [(7, 7)]

    def _pre_sort_moves(self, board, candidates):
        scored = []
        for row, col in candidates:
            score = self._quick_evaluate(board, row, col, self.player)
            score += self._quick_evaluate(board, row, col, self.opponent) * 0.9
            scored.append(((row, col), score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [move for move, score in scored]

    def _quick_evaluate(self, board, row, col, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            for i in range(1, 5):
                r, c = row + dr * i, col + dc * i
                if (0 <= r < board.size and
                    0 <= c < board.size and
                    board.grid[r][c] == player):
                    count += 1
                else:
                    break
            if count >= 4:
                score += 10000
            elif count == 3:
                score += 1000
            elif count == 2:
                score += 100
            elif count == 1:
                score += 10
        return score

    def _evaluate_position(self, board, row, col):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
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
                if count >= 4:
                    score += 10000
                elif count == 3 and empty > 0:
                    score += 1000
                elif count == 2 and empty > 0:
                    score += 100
                elif count == 1 and empty > 0:
                    score += 10
        center = board.size // 2
        distance = abs(row - center) + abs(col - center)
        score += max(0, 15 - distance)
        return score

    def _evaluate_board(self, board):
        score = 0
        score += self._evaluate_all_positions(board, self.player)
        score -= self._evaluate_all_positions(board, self.opponent) * 0.9
        return score

    def _evaluate_all_positions(self, board, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(board.size):
            for col in range(board.size):
                if board.grid[row][col] == player:
                    for dr, dc in directions:
                        count = 1
                        for i in range(1, 5):
                            r, c = row + dr * i, col + dc * i
                            if (0 <= r < board.size and
                                0 <= c < board.size and
                                board.grid[r][c] == player):
                                count += 1
                            else:
                                break
                        if count >= 5:
                            score += 100000
                        elif count == 4:
                            score += 10000
                        elif count == 3:
                            score += 1000
                        elif count == 2:
                            score += 100
                        elif count == 1:
                            score += 10
        return score
