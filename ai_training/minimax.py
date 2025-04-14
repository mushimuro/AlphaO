import numpy as np
from typing import Tuple, List, Optional
from renju_rule import is_double_three, is_double_four, is_overline, check_if_win
import copy

class Minimax:
    def __init__(self, depth: int = 3):
        """
        Gomoku AI를 초기화한다.
        Args:
            depth (int): 미니맥스 탐색 트리의 깊이 (기본값: 3)
        """
        self.depth = depth
        # Renju 규칙 모듈에 맞춰, 8방향 중 4방향과 그 반대쪽에 해당하는 방향 벡터 설정
        self.list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
        self.list_dy = [0, 0, -1, 1, -1, 1, -1, 1]

    def evaluate_window(self, window: List[int], color: int) -> int:
        """
        5칸짜리 윈도우를 평가하여 점수를 반환한다.
    
        Args:
            window: 1(흑), -1(백), 0(빈 칸)을 포함하는 길이 5의 리스트.
            color: 평가할 플레이어의 색 (1: 흑, -1: 백).
    
        Returns:
            해당 윈도우에 대한 누적 점수.
        
        휴리스틱 평가 항목에 따른 배점 예시:
            'forbidden': -100000         # 현재 플레이어가 금수(특히 흑)에 둘 때
            'five': 100000               # 돌 5개 연속 (승리)
            'open_four_defense': 49000    # 상대가 open four를 형성할 경우 (방어)
            'open_four_attack': 24000     # 내가 돌을 놓아서 open four를 만들면 (공격)
            'closed_four': 10000          # 양쪽이 막힌 4 (closed four)
            'opponent_open_three': 4000   # 상대가 open three를 형성할 경우 (강한 위협)
            'opponent_three': 1000        # 상대가 3을 형성할 경우 (약한 위협)
            'open_three_attack': 400      # 내가 돌을 놓아서 open three를 만들면
            'three_attack': 100           # 내가 돌 3개 연속으로 연결하면 (공격)
            'one': 10                    # 돌 1개일 때의 기본 점수
            'adjacent_bonus': 1           # 인접 돌 보너스
            'center_control': 500         # 보드 중앙 장악 보너스
        """
        # 휴리스틱 점수 사전 (필요한 항목만 사용)
        pattern_scores = {
            'forbidden': -100000,
            'five': 100000,
            'open_four_defense': 49000,
            'open_four_attack': 24000,
            'closed_four': 10000,
            'opponent_open_three': 4000,
            'opponent_three': 1000,
            'open_three_attack': 400,
            'three_attack': 100,
            'one': 10,
            'adjacent_bonus': 1,
            'center_control': 500,
        }

        opponent = -color
        score = 0

        # 윈도우에 내 돌과 상대 돌이 모두 존재하면 명확한 패턴이 아니므로 0점 처리
        if color in window and opponent in window:
            return 0

        count_self = window.count(color)
        count_empty = window.count(0)
        count_opp = window.count(opponent)

        if count_self > 0:
            # 내 돌만 있는 경우 (공격 패턴)
            if count_self == 5:
                score += pattern_scores['five']
            elif count_self == 4 and count_empty == 1:
                # 여기에서는 open four 공격으로 가정 (양쪽 막힘인 경우 closed_four도 적용할 수 있음)
                score += pattern_scores['open_four_attack']
            elif count_self == 3 and count_empty == 2:
                # open three 공격
                score += pattern_scores['open_three_attack']
            elif count_self == 2 and count_empty == 3:
                score += pattern_scores['three_attack']
            elif count_self == 1 and count_empty == 4:
                score += pattern_scores['one']
            # (추가로 인접 돌 보너스나 중앙 제어 보너스를 적용할 수 있으나, window 단위에서는 위치 정보가 부족하므로 생략)
        elif count_opp > 0:
            # 상대 돌만 있는 경우 (방어 패턴)
            if count_opp == 4 and count_empty == 1:
                score -= pattern_scores['open_four_defense']
            elif count_opp == 3 and count_empty == 2:
                score -= pattern_scores['opponent_open_three']
            elif count_opp == 2 and count_empty == 3:
                score -= pattern_scores['opponent_three']

        return score


    def evaluate_board(self, board: List[List[int]], color: int) -> int:
        """
        전체 보드 상태를 평가한다.
        Args:
            board: 현재 게임 보드 (15x15 2차원 리스트)
            color: 평가할 플레이어의 색 (1: 흑, -1: 백)
        Returns:
            보드의 총 점수
        """
        score = 0
        
        # 4가지 기본 방향(가로, 세로, 두 대각선) * 각 방향 양쪽(8방향)
        for direction in range(4):
            for i in range(2):
                idx = direction * 2 + i
                dx, dy = self.list_dx[idx], self.list_dy[idx]
                
                # 보드를 스캔하면서 모든 위치에서 연속된 5칸을 평가
                for row in range(15):
                    for col in range(15):
                        window = []
                        for k in range(5):
                            new_row = row + k * dy
                            new_col = col + k * dx
                            if 0 <= new_row < 15 and 0 <= new_col < 15:
                                window.append(board[new_row][new_col])
                            else:
                                break
                        if len(window) == 5:
                            score += self.evaluate_window(window, color)
        
        return score

    def get_valid_moves(self, board: List[List[int]], color: int) -> List[Tuple[int, int]]:
        """
        현재 보드에서 유효한 수(빈 칸 중, 인접에 돌이 존재하는 칸)를 반환한다.
        흑돌(1)의 경우, Renju 규칙에 따른 금수를 배제한다.
        Args:
            board: 현재 게임 보드 (2차원 리스트)
            color: 현재 플레이어의 색 (1: 흑, -1: 백)
        Returns:
            유효한 수의 좌표 리스트 [(row, col), ...]
        """
        valid_moves = []
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0:
                    has_neighbor = False
                    # 인접 돌(거리 1~2) 존재 여부 확인
                    for direction in range(4):
                        for side in range(2):
                            idx = direction * 2 + side
                            for dist in range(1, 3):
                                ni = i + self.list_dy[idx] * dist
                                nj = j + self.list_dx[idx] * dist
                                if 0 <= ni < 15 and 0 <= nj < 15 and board[ni][nj] != 0:
                                    has_neighbor = True
                                    break
                            if has_neighbor:
                                break
                        if has_neighbor:
                            break
                    if has_neighbor:
                        # 흑돌이라면 금수 체크
                        if color == 1:
                            if (is_double_three(board, i, j, color) or 
                                is_double_four(board, i, j) or 
                                is_overline(board, i, j)):
                                continue
                        valid_moves.append((i, j))
        return valid_moves

    def minimax(self,
                board: List[List[int]],
                depth: int,
                alpha: float,
                beta: float,
                maximizing_player: bool,
                color: int) -> Tuple[int, Optional[Tuple[int, int]]]:
        """
        알파-베타 가지치기를 적용한 미니맥스 알고리즘.
        Args:
            board: 현재 보드 상태 (2차원 리스트)
            depth: 탐색 깊이
            alpha, beta: 가지치기용 경계값
            maximizing_player: 최대화(내가 두는 턴)면 True, 아니면 False
            color: Minimax의 기준이 되는 플레이어(예: 흑)
        Returns:
            (최종 점수, 최적의 좌표) 튜플, 좌표는 (row, col)
        """
        # 1) 깊이가 0이면 점수 리턴
        if depth == 0:
            return self.evaluate_board(board, color), None

        # 2) 유효한 수 찾기
        valid_moves = self.get_valid_moves(board, color if maximizing_player else -color)
        if not valid_moves:
            # 둘 곳이 없다면 현재 보드 평가값 반환
            return self.evaluate_board(board, color), None

        # 3) 최대화 / 최소화 분기
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for (r, c) in valid_moves:
                # 현재 플레이어(color) 돌 두기
                board[r][c] = color
                # 놓은 직후 승리 여부 확인
                if check_if_win(board, r, c, color):
                    board[r][c] = 0
                    return (100000, (r, c))  # 큰 점수로 즉시 반환
                
                eval_score, _ = self.minimax(board,
                                             depth - 1,
                                             alpha, beta,
                                             maximizing_player=False,
                                             color=color)
                board[r][c] = 0  # Undo move

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for (r, c) in valid_moves:
                # 상대 플레이어(-color) 돌 두기
                board[r][c] = -color
                if check_if_win(board, r, c, -color):
                    board[r][c] = 0
                    return (-100000, (r, c))  # 작은 점수로 즉시 반환

                eval_score, _ = self.minimax(board,
                                             depth - 1,
                                             alpha, beta,
                                             maximizing_player=True,
                                             color=color)
                board[r][c] = 0  # Undo move

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self,
                      board: List[List[int]],
                      color: int) -> Optional[Tuple[int, int]]:
        """
        현재 보드 상태에서 최적의 수를 구하여 반환한다.
        Args:
            board: 게임 보드(2차원 리스트)
            color: 현재 플레이어의 색 (1: 흑, -1: 백)
        Returns:
            (row, col) 형태의 최적의 수 혹은 None
        """
        best_score, best_move = self.minimax(
            board,
            self.depth,
            alpha=float('-inf'),
            beta=float('inf'),
            maximizing_player=True,
            color=color
        )

        # 혹시 선택된 수가 흑 금수에 걸리면 다른 유효 수 하나 골라 반환(원하면 제거 가능)
        if best_move:
            row, col = best_move
            if color == 1:
                if (is_double_three(board, row, col, color) or
                    is_double_four(board, row, col) or
                    is_overline(board, row, col)):
                    valid_moves = self.get_valid_moves(board, color)
                    if valid_moves:
                        return valid_moves[0]
                    return None

        return best_move
