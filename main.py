import chess
import chess.svg

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.setGeometry(100, 100, 1100, 1100)
        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1080, 1080)

        board = chess.Board("8/8/8/8/4N3/8/8/8 w - - 0 1")
        self.chessboardSvg = chess.svg.board(
            board,
            fill=dict.fromkeys(board.attacks(chess.E4), "#cc0000cc"),
            arrows=[chess.svg.Arrow(chess.E4, chess.F6)],
            squares=chess.SquareSet(chess.BB_DARK_SQUARES & chess.BB_FILE_B),
            size=350,
        ).encode("UTF-8")
        
        self.widgetSvg.load(self.chessboardSvg)

    
    
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()