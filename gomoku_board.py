import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

BOARD_SIZE = 15
CELL_SIZE = 40
STONE_SIZE = 15

class GomokuBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = "black"
        
        # TODO : make the size to be flexible : if window becomes smaller, the board scales down too
        self.setFixedSize(BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
        # TODO ??? self.setFixedSize(self.sizeHint())

        #################################################################
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

        # draw board   // left top corner : (0,0), right bottom corner : (14,14)
        #              // so... no need for coordinate changing logic?
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
                if self.board[row][col]:   # ensures blank space
                    if self.board[row][col] == "black":  
                        painter.setBrush(QBrush(Qt.GlobalColor.black))  
                    else:  
                        painter.setBrush(QBrush(Qt.GlobalColor.white)) 
                    x = col * CELL_SIZE + CELL_SIZE // 2
                    y = row * CELL_SIZE + CELL_SIZE // 2
                    painter.drawEllipse(QPoint(x, y), STONE_SIZE, STONE_SIZE)

    # placing stones
    def mousePressEvent(self, event):
        x, y = event.position().x(), event.position().y()
        col = int(x // CELL_SIZE)
        row = int(y // CELL_SIZE)
        # row = BOARD_SIZE - 1 - int(y // CELL_SIZE)

        # checking valid space  // 여기에서 빈자리인지 확인도 되니 굳이 렌주룰 파일에서 또 확인 안해도 괜찮은지?
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] is None:
            self.board[row][col] = self.current_player
            # print(col, row)   # printing coordinate
            # switch turns
            if self.current_player == "black":
                self.current_player = "white"
            else:
                self.current_player = "black"

            self.update()


    # creates new board
    def clearBoard(self):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]  
        self.current_player = "black"  
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GomokuBoard()
    window.setWindowTitle("AlphO")
    window.show()
    sys.exit(app.exec())