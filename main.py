import chess
import chess.svg
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.modified = False
        self.setGeometry(100, 100, 1100, 1100)
        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1080, 1080)

        self.board = chess.Board()
        self.chessboardSvg = chess.svg.board(self.board).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def paintEvent(self, event):
        if self.modified:
            self.chessboardSvg = chess.svg.board(self.board).encode("UTF-8")
            self.widgetSvg.load(self.chessboardSvg)
            self.widgetSvg.load(self.chessboardSvg)
            self.modified = False

    def keyPressEvent(self, event):
        gey = event.key()
        if gey == Qt.Key_D:
            sys.exit()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    while True:
        text = input("Next move \n")
        print(list(window.board.legal_moves))

        if (text):
            move = chess.Move.from_uci(text)
            window.board.push(move)
            window.modified = True
            window.update()
