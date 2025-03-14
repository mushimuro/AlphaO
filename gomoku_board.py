import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from renju_rule import *

BOARD_SIZE = 15
CELL_SIZE = 40
STONE_SIZE = 15

class GomokuBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 1
        
        # TODO : make the size to be flexible : if window becomes smaller, the board scales down too
        self.setFixedSize(BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
        

        #################################################################
        # TODO ??? self.setFixedSize(self.sizeHint())
        # TODO : using image background, need to work on making exact placements
        # self.board_image = QPixmap(os.path.join(os.path.dirname(__file__), "board_img.png"))
        #################################################################
    

    def paintEvent(self, event):
        """Draws the board grid and stones."""
        painter = QPainter(self)
        # antialiasing to make lines smoother
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        #################################################################
        # TODO : using image backgounrd
        # scaled_board = self.board_image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
        # painter.drawPixmap(0, 0, scaled_board)
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
        # row = BOARD_SIZE - 1 - int(y // CELL_SIZE)

        # checking valid space  // 여기에서 빈자리인지 확인도 되니 굳이 렌주룰 파일에서 또 확인 안해도 괜찮은지?
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == 0:
            # 6+ stones check
            overline_check = False
            if self.current_player == 1:
                print("black stone")
                overline_check = is_overline(self.board, row, col)
            # if not is_double_four(self.board, row,col):
            print(overline_check)
            if not is_samsam(self.board, row, col, self.current_player) and not overline_check:
            # if True:
                self.board[row][col] = self.current_player
                self.update()
                rule_check = pre_check(self.board, row, col, self.current_player)
                # check for win
                if rule_check == "win":
                    print("WIN!!!")
                    # TODO: make this to create event (pop-up screen -> "play again" & "back to main")
                elif rule_check == "invalid move":
                    print("Invalid move")
                
                self.current_player = -1 if self.current_player == 1 else 1
                self.update()
            else:
                print("Invalid move")
            # self.update()


    # creates new board
    def clearBoard(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]  
        self.current_player = "black"  
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GomokuBoard()
    window.setWindowTitle("AlphO")
    window.show()
    sys.exit(app.exec())