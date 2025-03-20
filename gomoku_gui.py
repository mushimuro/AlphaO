import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import gomoku_board

# TODO : PvC, PvP 정하는 최상단 페이지 만들기

class Main(QDialog):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget(self)

        self.main_page = QWidget()
        self.game_page = QWidget()

        self.init_main_page()
        self.init_game_page()

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.game_page)

        # main_layout = QVBoxLayout(QFormLayout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        self.setWindowTitle("AlphaO")

        # window size
        self.resize(800, 600)


    # main page
    def init_main_page(self):
        main_layout = QFormLayout()
        
        # page layouts
        layout1 = QVBoxLayout()
        color_layout = QHBoxLayout()
        start_button_layout = QVBoxLayout()

        # widgets
        label_widget = QLabel("Main menu")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_widget.setStyleSheet("font-size: 24px; font-weight: bold;")
    
        start_button_widget = QPushButton("click to start")
        start_button_layout.addWidget(start_button_widget)
        start_button_widget.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.game_page))

        # choose level difficulty
        level_widget = QComboBox()
        level_widget.addItems(["Choose difficulty", "Level 1", "Level 2", "Level 3"])
        # choose white/black stone
        # TODO : 컴퓨터랑 사람이랑 턴제로 하는데, 사람이 색 선택시... function 만들기
        radio_white, radio_black = QRadioButton("White"), QRadioButton("Black")
        color_layout.addWidget(radio_white)
        color_layout.addWidget(radio_black)    
    
        # ordering of layouts/widgets (top -> down)
        layout1.addWidget(label_widget)
        layout1.addWidget(level_widget)
        layout1.addWidget(start_button_widget)
        main_layout.addRow(layout1)  
        main_layout.addRow(color_layout)
        main_layout.addRow(start_button_layout)

        # default settings
        self.main_page.setLayout(main_layout)


    # game page   
    def init_game_page(self):
        main_layout = QFormLayout()
        
        # page layouts
        layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        board_layout = QHBoxLayout()
        board_layout.addStretch()

        # widgets
        label_widget = QLabel("ALPHAO!")
        surrender_button_widget = QPushButton("surrender")
        place_button_widget = QPushButton("place")
        self.gomoku_board = gomoku_board.GomokuBoard(parent=self)
        
        # widget customize & functions
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_widget.setStyleSheet("font-size: 24px; font-weight: bold;")
        surrender_button_widget.clicked.connect(lambda: self.handle_game_over("Black" if self.gomoku_board.current_player == -1 else "White"))
        self.gomoku_board.game_over_signal.connect(self.handle_game_over)
    
        # sub-layout ordering
        layout.addWidget(label_widget)
        buttons_layout.addWidget(surrender_button_widget)
        buttons_layout.addWidget(place_button_widget)
        board_layout.addWidget(self.gomoku_board)
        board_layout.addStretch()

        # main-layout ordering
        main_layout.addRow(layout)  
        main_layout.addRow(board_layout)
        main_layout.addRow(buttons_layout)

        # default settings
        self.game_page.setLayout(main_layout)


    
    def handle_game_over(self, winner_color):
        print(winner_color)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(f"{winner_color} color wins!")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        button = msg_box.exec()

        if button == QMessageBox.StandardButton.Ok:
            self.stacked_widget.setCurrentWidget(self.main_page)
            self.gomoku_board.clearBoard()


    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())