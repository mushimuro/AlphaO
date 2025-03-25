# mcts_agent.py
import copy
import math
import random
from renju_rule import pre_check  # renju_rule.py의 승리 판별 함수 사용

BOARD_SIZE = 15

class GomokuState:
    def __init__(self, board, current_player):
        # board: 15x15 2차원 리스트, current_player: 1 (흑) 또는 -1 (백)
        self.board = board
        self.current_player = current_player

    def get_valid_moves(self):
        moves_set = set()
        board_has_stone = False
        for r in range(15):
            for c in range(15):
                if self.board[r][c] != 0:
                    board_has_stone = True
                    # 돌이 있는 자리 주변 5칸 범위 내 모든 좌표를 추가 (경계 체크 포함)
                    for i in range(max(0, r - 5), min(15, r + 6)):
                        for j in range(max(0, c - 5), min(15, c + 6)):
                            # 돌이 없는 자리만 valid move로 추가
                            if self.board[i][j] == 0:
                                moves_set.add((i, j))
        # 보드에 돌이 하나도 없는 경우, 중앙 위치를 기본 valid move로 반환
        if not board_has_stone:
            return [(7, 7)]
        return list(moves_set)

    def play_move(self, move):
        # 현재 상태를 복사한 후, move를 적용하여 새로운 상태 반환
        new_board = copy.deepcopy(self.board)
        r, c = move
        new_board[r][c] = self.current_player
        return GomokuState(new_board, -self.current_player)

    def is_game_over(self):
        # 빈 칸이 없거나, 어느 한쪽이 승리한 경우 종료
        if not self.get_valid_moves():
            return True
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] != 0:
                    result = pre_check(self.board, r, c, self.board[r][c])
                    if result == "win":
                        return True
        return False

    def get_winner(self):
        # 승자가 있으면 1 또는 -1, 없으면 0 (무승부)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] != 0:
                    result = pre_check(self.board, r, c, self.board[r][c])
                    if result == "win":
                        return self.board[r][c]
        return 0

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state      # GomokuState 객체
        self.parent = parent
        self.move = move        # 이 노드에 도달하기 위해 사용된 move (row, col)
        self.children = []      # 자식 노드 리스트
        self.visits = 0
        self.wins = 0           # 시뮬레이션에서 이긴 횟수

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_valid_moves())

    def best_child(self, c_param=1.41):
        choices = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices.index(max(choices))]

class MCTSAgent:
    def __init__(self, iterations=10000):
        self.iterations = iterations

    def select_move(self, root_state):
        root_node = MCTSNode(root_state)

        for _ in range(self.iterations):
            node = root_node
            state = root_state

            # 1. Selection: 자식 노드를 UCB 기준으로 선택
            while node.children and node.is_fully_expanded():
                node = node.best_child()
                state = node.state

            # 2. Expansion: 아직 시도하지 않은 move가 있으면 확장
            valid_moves = state.get_valid_moves()
            if valid_moves:
                tried_moves = [child.move for child in node.children]
                untried = [move for move in valid_moves if move not in tried_moves]
                if untried:
                    move = random.choice(untried)
                    state = state.play_move(move)
                    new_node = MCTSNode(state, parent=node, move=move)
                    node.children.append(new_node)
                    node = new_node

            # 3. Simulation: state에서 게임 끝까지 랜덤 플레이 (플레이아웃)
            sim_state = state
            while not sim_state.is_game_over():
                moves = sim_state.get_valid_moves()
                if not moves:
                    break
                move = random.choice(moves)
                sim_state = sim_state.play_move(move)

            # 4. Backpropagation: 시뮬레이션 결과로 승패 정보 업데이트
            winner = sim_state.get_winner()
            while node is not None:
                node.visits += 1
                if winner != 0 and node.state.current_player == -winner:
                    node.wins += 1
                node = node.parent

        # 최종적으로 가장 많이 방문한 자식을 선택
        best_move_node = max(root_node.children, key=lambda child: child.visits)
        return best_move_node.move

# 단독 테스트용
if __name__ == '__main__':
    initial_board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    initial_state = GomokuState(initial_board, 1)
    agent = MCTSAgent(iterations=1000)
    move = agent.select_move(initial_state)
    print("MCTS 선택 수:", move)
