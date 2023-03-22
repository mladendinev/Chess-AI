import chess
import chess.svg
import sys
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QApplication, QWidget
import random
import numpy as np


class MainWindow(QWidget):
    def __init__(self, human_color) -> None:
        super().__init__()

        self.human_color = human_color
        self.modified = False
        self.svg_xy = 10
        self.board_size = 512
        
        self.square_size = self.board_size / 8.0 
        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(self.svg_xy, self.svg_xy, 900, 880)

        self.board = chess.Board()
        self.chessboardSvg = chess.svg.board(self.board).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)
        self.last_click = None

    
    # @pyqtSlot(str)
    # def apply_move(self, uci):
    #     """
    #         BRIEF  Apply a move to the board
    #     """
    #     move = chess.Move.from_uci(uci)
    #     if move in self.legal_moves:
    #         self.push(move)
            
    #         print(self.fen())
    #         if not self.is_game_over():
    #             self.ReadyForNextMove.emit(self.fen())
    #         else:
    #             print("Game over!")
    #             self.GameOver.emit()
    #         sys.stdout.flush()

    def paintEvent(self, event):
        if self.modified:
            self.chessboardSvg = chess.svg.board(self.board).encode("UTF-8")
            self.widgetSvg.load(self.chessboardSvg)
            self.modified = False

    def keyPressEvent(self, event):
        gey = event.key()
        if gey == Qt.Key.Key_D.value:
            sys.exit()

    def LeftClickedBoard(self, event):
        """
            BRIEF  Check to see if they left-clicked on the chess board
        """
        topleft     = self.svg_xy
        bottomright = self.board_size + self.svg_xy
        return all([
            event.buttons() == Qt.MouseButton.LeftButton,
            topleft < event.pos().x() < bottomright,
            topleft < event.pos().y() < bottomright,
        ])

    @pyqtSlot(QWidget)
    def mousePressEvent(self, event):
        if self.LeftClickedBoard(event):
            this_click = self.GetClicked(event)
            
            if self.last_click:
                if self.last_click != this_click:
                    uci = self.last_click + this_click
                    # TODO: apply move
                    # self.apply_move(uci + self.get_promotion(uci))
                
            self.last_click = this_click
         
    def get_clicked(self, event):
        top_left = self.svg_xy 
        file_i = int((event.pos().x() - top_left)/self.square_size)
        rank_i = 7 - int((event.pos().y() - top_left)/self.square_size)
        print(chr(file_i + 97) + str(rank_i + 1))
        return chr(file_i + 97) + str(rank_i + 1)
    

    def get_player_turn_color(self):
        return "White" if self.board.turn else "Black"

    def get_player_turn_binary(self):
        return self.board.turn

    def play(self):
        while True:
            legal_moves = list(self.board.legal_moves)
            print(f"Player's turn: {self.get_player_turn_color()}")

            print("Possible moves", legal_moves)
            if (self.get_player_turn_binary() == human_color):
                try:
                    text = input(f"Enter next move in UCI format \n")
                    move = chess.Move.from_uci(text)
                    if move in self.board.legal_moves:
                        self.board.push(move)
                    else:
                        print("Illegal move")
                except Exception as ex:
                    print("Exception occurred\n", ex)
            else:
                # Replace the random move with the value from the evaluation function
                self.board.push(random.choice(legal_moves))
            self.modified = True
            self.update()


if __name__ == '__main__':
    app = QApplication([])
    human_color = np.random.choice([True, False])
    print("Your color is ", human_color)
    window = MainWindow(human_color=human_color)
    window.show()
    window.play()
