import random

BOARD_SIZE = 15


def heuristic_evaluation(state, move):
    """
    기본 휴리스틱 평가 함수:
    - move 위치의 8방향 인접 셀 중, 현재 플레이어의 돌이 몇 개 있는지 셉니다.
    """
    r, c = move
    score = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            if state.board[nr][nc] == state.current_player:
                score += 1
    return score


def threat_blocking_score(state, move):
    """
    상대 돌이 연속으로 3개 이상 있는 경우 또는 2개이고 open 상태인 경우,
    해당 move가 위협을 차단할 가능성이 있으므로 높은 보너스 점수를 부여합니다.

    4가지 주요 방향(수평, 수직, 두 대각선)마다 검사하여 각 방향의 bonus를 합산합니다.
    """
    opponent = -state.current_player
    r, c = move
    bonus = 0
    # 4방향: 수평, 수직, 두 대각선
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count_pos = 0
        nr, nc = r + dr, c + dc
        # positive direction: 연속된 상대 돌 개수
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and state.board[nr][nc] == opponent:
            count_pos += 1
            nr += dr
            nc += dc
        # positive direction open 여부: while문 종료 후 nr,nc 범위 내이고 빈 칸이면 open
        open_pos = (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and state.board[nr][nc] == 0)

        count_neg = 0
        nr, nc = r - dr, c - dc
        # negative direction: 연속된 상대 돌 개수
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and state.board[nr][nc] == opponent:
            count_neg += 1
            nr -= dr
            nc -= dc
        open_neg = (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and state.board[nr][nc] == 0)

        total = count_pos + count_neg
        # 만약 총 연속 상대 돌이 3개 이상이면 큰 보너스 추가
        if total >= 3:
            bonus += 10000
        # 2개이고 한쪽 이상이 open이면 약한 위협으로 간주하여 보너스 추가
        elif total == 2 and (open_pos or open_neg):
            bonus += 5000
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
