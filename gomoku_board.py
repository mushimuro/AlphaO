# gomoku_board.py
import sys, os, copy
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtGui import QPainter, QPen, QBrush, QPixmap, QFont
from PyQt6.QtCore import QPoint, Qt, QTimer
from renju_rule import pre_check, is_overline, is_double_three, is_double_four  # 필요한 함수 임포트
from mcts_agent import MCTSAgent, GomokuState

BOARD_SIZE = 15
CELL_SIZE = 40
STONE_SIZE = 15


class GomokuBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 1  # 1: 흑, -1: 백
        self.parent_widget = parent

        self.setFixedSize(BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)

        # 배경 이미지 설정 (이미지 파일이 있는 경우)
        self.background_img = QPixmap(os.path.join(os.path.dirname(__file__), "white_background.png"))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 배경 그리기
        scaled_board = self.background_img.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
        painter.drawPixmap(0, 0, scaled_board)

        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        for i in range(BOARD_SIZE):
            painter.drawLine(i * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2,
                             i * CELL_SIZE + CELL_SIZE // 2, (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2)
            painter.drawLine(CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2,
                             (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)

        # 돌 그리기
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != 0:
                    if self.board[row][col] == 1:
                        painter.setBrush(QBrush(Qt.GlobalColor.black))
                    else:
                        painter.setBrush(QBrush(Qt.GlobalColor.white))
                    x = col * CELL_SIZE + CELL_SIZE // 2
                    y = row * CELL_SIZE + CELL_SIZE // 2
                    painter.drawEllipse(QPoint(x, y), STONE_SIZE, STONE_SIZE)

    def mousePressEvent(self, event):
        x, y = event.position().x(), event.position().y()
        col = int(x // CELL_SIZE)
        row = int(y // CELL_SIZE)

        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == 0:
            overline_check = False
            if self.current_player == 1:
                overline_check = is_overline(self.board, row, col)
            if (not is_double_three(self.board, row, col, self.current_player) and
                    not overline_check and
                    not is_double_four(self.board, row, col)):
                self.board[row][col] = self.current_player
                self.update()
                rule_check = pre_check(self.board, row, col, self.current_player)
                if rule_check == "win":
                    winner_color = "Black" if self.current_player == 1 else "White"
                    self.game_over(winner_color)
                    return
                else:
                    self.current_player = -self.current_player
                    self.update()
                    # 사람이 두고 난 후, AI 턴이면 자동으로 ai_move() 호출
                    if self.current_player == -1:
                        QTimer.singleShot(500, self.ai_move)
            else:
                print("Invalid move")

    def ai_move(self):
        # 현재 보드 상태와 현재 플레이어 정보를 사용하여 AI가 돌 두기
        current_state = GomokuState(copy.deepcopy(self.board), self.current_player)
        agent = MCTSAgent(iterations=500)
        move = agent.select_move(current_state)
        if move is not None:
            r, c = move
            self.board[r][c] = self.current_player
            self.update()
            if pre_check(self.board, r, c, self.current_player) == "win":
                winner_color = "Black" if self.current_player == 1 else "White"
                self.game_over(winner_color)
                return
            else:
                self.current_player = -self.current_player
                self.update()
                # 만약 AI 턴 후에도 AI가 계속 두어야 한다면 (예: 두 명의 AI 대결), 여기서 다시 호출
                # if self.current_player == -1:
                #     QTimer.singleShot(500, self.ai_move)

    def game_over(self, winner_color):
        # 게임 종료 시 팝업 띄우고 보드를 초기화
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(f"{winner_color} wins!")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        self.clearBoard()

    def clearBoard(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 1
        self.update()


# 단독 실행 테스트
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = GomokuBoard()
    window.setWindowTitle("Gomoku AI Test")
    window.show()
    sys.exit(app.exec())
