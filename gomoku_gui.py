# gomoku_gui.py
import sys
from PyQt6.QtWidgets import QApplication, QDialog, QStackedWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QRadioButton, QMessageBox
from PyQt6.QtCore import Qt
from gomoku_board import GomokuBoard

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget(self)
        self.main_page = self.init_main_page()
        self.game_page = self.init_game_page()
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.game_page)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
        self.setWindowTitle("AlphaO")
        self.resize(800, 600)

    def init_main_page(self):
        main_page = QDialog()
        main_layout = QFormLayout()
        label_widget = QLabel("Main Menu")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_widget.setStyleSheet("font-size: 24px; font-weight: bold;")
        start_button = QPushButton("Click to Start")
        start_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.game_page))
        level_widget = QComboBox()
        level_widget.addItems(["Choose model", "Minimax", "MCTS", "DL"])
        radio_white = QRadioButton("White")
        radio_black = QRadioButton("Black")
        color_layout = QHBoxLayout()
        color_layout.addWidget(radio_white)
        color_layout.addWidget(radio_black)
        main_layout.addRow(label_widget)
        main_layout.addRow(level_widget)
        main_layout.addRow(start_button)
        main_layout.addRow(color_layout)
        main_page.setLayout(main_layout)
        return main_page

    def init_game_page(self):
        game_page = QDialog()
        main_layout = QFormLayout()
        label_widget = QLabel("ALPHAO!")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_widget.setStyleSheet("font-size: 24px; font-weight: bold;")
        surrender_button = QPushButton("Surrender")
        place_button = QPushButton("Place")  # 버튼 클릭 시 별도 동작을 넣을 수 있음
        self.gomoku_board = GomokuBoard(parent=self)
        surrender_button.clicked.connect(lambda: self.handle_game_over("Black" if self.gomoku_board.current_player == -1 else "White"))
        board_layout = QHBoxLayout()
        board_layout.addWidget(self.gomoku_board)
        board_layout.addStretch()
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(surrender_button)
        buttons_layout.addWidget(place_button)
        main_layout.addRow(label_widget)
        main_layout.addRow(board_layout)
        main_layout.addRow(buttons_layout)
        game_page.setLayout(main_layout)
        return game_page

    def handle_game_over(self, winner_color):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(f"{winner_color} wins!")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.gomoku_board.clearBoard()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())