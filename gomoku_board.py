import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from renju_rule import *

# default size for board and stone
BOARD_SIZE = 15
CELL_SIZE = 40
STONE_SIZE = 15

class GomokuBoard(QWidget):
    game_over_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 1
        self.parent_widget = parent
        
        # TODO : make the size to be flexible : if window becomes smaller, the board scales down too
        self.setFixedSize(BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
        

        #################################################################
        # TODO ??? self.setFixedSize(self.sizeHint())
        # TODO : using image background, need to work on making exact placements
        # self.board_image = QPixmap(os.path.join(os.path.dirname(__file__), "board_img.png"))
        self.background_img = QPixmap(os.path.join(os.path.dirname(__file__), "white_background.png"))
        #################################################################
    

    def paintEvent(self, event):
        """Draws the board grid and stones."""
        painter = QPainter(self)
        # antialiasing to make lines smoother
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # painter.setBackground(Qt.GlobalColor.white)

        #################################################################
        # TODO : using image backgounrd
        # scaled_board = self.board_image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
        scaled_board = self.background_img.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
        painter.drawPixmap(0, 0, scaled_board)
        #################################################################

        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        for i in range(BOARD_SIZE):
            painter.drawLine(i * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2,
                             i * CELL_SIZE + CELL_SIZE // 2, (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2)
            painter.drawLine(CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2,
                             (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)

        # draw stones
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != 0:   # ensures blank space
                    if self.board[row][col] == 1:  
                        painter.setBrush(QBrush(Qt.GlobalColor.black))  
                    else:  
                        painter.setBrush(QBrush(Qt.GlobalColor.white)) 
                    x = col * CELL_SIZE + CELL_SIZE // 2
                    y = row * CELL_SIZE + CELL_SIZE // 2
                    painter.drawEllipse(QPoint(x, y), STONE_SIZE, STONE_SIZE)

    # placing stones
    def mousePressEvent(self, event):
        x, y = event.position().x(), event.position().y()
        col = int(x // CELL_SIZE)   # x-value
        row = int(y // CELL_SIZE)   # y-value

        # checking if open spot to place
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == 0:
            # 6+ stones check
            overline_check = False
            double_four_check = False
            double_four_check = False
            if self.current_player == 1:
                overline_check = is_overline(self.board, row, col)
                double_four_check = is_double_four(self.board, row,col)
                double_four_check = is_double_four(self.board, row,col)

            if not is_double_three(self.board, row, col, self.current_player) and not overline_check and not double_four_check:
            # TODO : if not is_double_four(self.board, row,col):
            if not is_double_three(self.board, row, col, self.current_player) and not overline_check and not double_four_check:
            # if True:
                self.board[row][col] = self.current_player
                self.update()
                rule_check = pre_check(self.board, row, col, self.current_player)
                # check for win
                if rule_check == "win":
                    winner_color = "Black" if self.current_player == 1 else "White"
                    self.game_over_signal.emit(winner_color)
                # check for invalid move
                elif rule_check == "invalid move":
                    print("Invalid move")
                else:
                    self.current_player = -1 if self.current_player == 1 else 1
                    self.update()
            else:
                print("Invalid move")
            # self.update()


    # creates new board when a game ends
    def clearBoard(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]  
        self.current_player = 1  
        self.update()


    # pop up screen when someone wins / redirects to main page when clicking "ok"
    def show_win_popup(self, winner_color):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(f"{winner_color} color wins!")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        button = msg_box.exec()

        if button == QMessageBox.StandardButton.Ok:
            if self.parent_widget:
                self.parent_widget.stacked_widget.setCurrentWidget(self.parent_widget.main_page)
                self.clearBoard()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GomokuBoard()
    window.setWindowTitle("AlphO")
    window.show()
    sys.exit(app.exec())
