import copy
import random
from renju_rule import pre_check, three, open_three, four, open_four, board, ban, is_invalid

BOARD_SIZE = 15
list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
list_dy = [0, 0, -1, 1, -1, 1, -1, 1]

def heuristic_evaluation(state, move):
    """
    기본 휴리스틱 평가 함수:
    - move 위치의 8방향 인접 셀 중, 현재 플레이어의 돌이 몇 개 있는지 셉니다.
    """
    y, x = move
    bonus = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 0 <= ny < BOARD_SIZE and 0 <= nx < BOARD_SIZE:
            if state.board[ny][nx] == state.current_player:
                bonus += 1
    return bonus



def threat_blocking_score(state, move):
    """
    상대 돌이 연속으로 3개 이상 있는 경우 또는 2개이고 open 상태인 경우,
    해당 move가 위협을 차단할 가능성이 있으므로 높은 보너스 점수를 부여합니다.

    4가지 주요 방향(수평, 수직, 두 대각선)마다 검사하여 각 방향의 bonus를 합산합니다.
    """
    # 중요도 순서
    # current_player 가 흑돌에 금수 위치(-100,000)
    # 내가 돌을 놓으면 5 (100,000)
    # 상대가 4, open4 (49,000)
    # 내가 돌을 놓으면 open4 (24,000)
    # 내가 돌을 놓으면 4 (10,000)
    # 상대가 open3 (4,000)
    # 상대가 3 (1,000)
    # 내가 돌을 놓으면 open3 (400)
    # 내가 돌을 놓으면 3 (100)
    # 인접 8방에 돌이 있으면 (1) -> heuristic_evaluation

    copy_board = copy.deepcopy(board)
    current_player = state.cureent_player
    opponent = -current_player
    y, x = move
    bonus = 0

    # 금수?
    if current_player == 1 and (y,x) in ban: return -100000

    # 나한테 유리한지 판단
    # 좌우, 상하, 양대각선을 받아서 체크
    copy_board[y][x] = current_player
    for direction in range(4):
        open_pattern_found = False
        for i in range(2):
            idx = direction * 2 + i
            yy, xx = list_dy[idx], list_dx[idx]
            ny, nx = y, x

            # 한쪽 방향 탐색
            line = [1]  # 시작점 돌(이미 놓은 돌)
            empty_cnt = 0
            stone_cnt = 0

            while True:
                ny += yy
                nx += xx

                if is_invalid(ny, nx):
                    break

                if copy_board[ny][nx] == 0:
                    line.append(0)
                    empty_cnt += 1
                elif copy_board[ny][nx] == 1:
                    line.append(1)
                    stone_cnt += 1
                else:  # 백돌이면 중단
                    break

                if empty_cnt >= 2 or stone_cnt > 2:
                    break

            # 반대 방향 탐색
            ny, nx = y, x
            empty_cnt = 0
            stone_cnt = 0

            while True:
                ny -= yy
                nx -= xx

                if is_invalid(ny, nx):
                    break

                if copy_board[ny][nx] == 0:
                    line.insert(0, 0)
                    empty_cnt += 1
                elif copy_board[ny][nx] == 1:
                    line.insert(0, 1)
                    stone_cnt += 1
                else:
                    break

                if empty_cnt >= 2 or stone_cnt > 2:
                    break
        # 내가 5, open4, 4, open3, 3 인지 판단
        if pre_check(copy_board, y, x, current_player) == "win" : return 100000
        if open_four(y, x, current_player): bonus += 24000
        if four(y, x, current_player): bonus += 10000
        if open_three(y, x, current_player): bonus += 400
        if three(y, x, current_player): bonus += 100
    copy_board[y][x] = 0

    # 위험도 판단
    # 좌우, 상하, 양대각선을 받아서 체크
    for direction in range(4):
        open_pattern_found = False
        for i in range(2):
            idx = direction * 2 + i
            yy, xx = list_dy[idx], list_dx[idx]
            ny, nx = y, x

            # 한쪽 방향 탐색
            line = [1]  # 시작점 돌(이미 놓은 돌)
            empty_cnt = 0
            stone_cnt = 0

            while True:
                ny += yy
                nx += xx

                if is_invalid(ny, nx):
                    break

                if copy_board[ny][nx] == 0:
                    line.append(0)
                    empty_cnt += 1
                elif copy_board[ny][nx] == 1:
                    line.append(1)
                    stone_cnt += 1
                else:  # 백돌이면 중단
                    break

                if empty_cnt >= 2 or stone_cnt > 2:
                    break

            # 반대 방향 탐색
            ny, nx = y, x
            empty_cnt = 0
            stone_cnt = 0

            while True:
                ny -= yy
                nx -= xx

                if is_invalid(ny, nx):
                    break

                if copy_board[ny][nx] == 0:
                    line.insert(0, 0)
                    empty_cnt += 1
                elif copy_board[ny][nx] == 1:
                    line.insert(0, 1)
                    stone_cnt += 1
                else:
                    break

                if empty_cnt >= 2 or stone_cnt > 2:
                    break
        # 상대가 4, open4, 3, open3 면 가중치 업데이트
        if four(y,x, opponent) or open_four(y,x, opponent): bonus += 49000
        if open_three(y, x, opponent): bonus += 4000
        if three(y, x, opponent): bonus += 1000

    return bonus



def heuristic_policy(state):
    """
    휴리스틱 정책:
    - state의 유효한 후보 수(valid moves) 각각에 대해,
      기본 휴리스틱 점수와 위협 차단 점수(threat_blocking_score)를 합산합니다.
    - 최고 점수를 가진 후보들 중 하나를 랜덤하게 선택합니다.
    - 모든 후보의 점수가 0이면 단순 랜덤 선택합니다.
    """
    moves = state.get_valid_moves()
    if not moves:
        return None
    scores = []
    for move in moves:
        base_score = heuristic_evaluation(state, move)
        block_score = threat_blocking_score(state, move)
        total_score = base_score + block_score
        scores.append(total_score)
    max_score = max(scores)
    best_moves = [move for move, score in zip(moves, scores) if score == max_score]
    if best_moves:
        return random.choice(best_moves)
    return random.choice(moves)
