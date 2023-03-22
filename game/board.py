import chess
import numpy as np


class Board(object):

    def __init__(self, board):
        self.board = board

    def serialize(self):
        bstate = np.zeros(64, np.uint8)
        for i in range(64):
            pp = self.board.piece_at(i)
            if pp is not None:
                # print(i, pp.symbol())
                bstate[i] = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6,
                             "p": 9, "n": 10, "b": 11, "r": 12, "q": 13, "k": 14}[pp.symbol()]

        if self.board.has_queenside_castling_rights(chess.WHITE):
            bstate[0] = 7
        elif self.board.has_kingside_castling_rights(chess.WHITE):
            bstate[7] = 7
        elif self.board.has_queenside_castling_rights(chess.BLACK):
            bstate[56] = 8 + 7
        elif self.board.has_kingside_castling_rights(chess.BLACK):
            bstate[63] = 8 + 7

        if self.board.ep_square is not None:
            bstate[self.board.ep_square] = 8

        bstate = bstate.reshape(8, 8)
        neural_network_state = np.zeros((5, 8, 8), np.uint8)
        
        neural_network_state[0] = (bstate >> 3) & 1
        neural_network_state[1] = (bstate >> 2) & 1
        neural_network_state[2] = (bstate >> 1) & 1
        neural_network_state[3] = (bstate >> 0) & 1
        neural_network_state[4] = (self.board.turn * 1.0)

        return neural_network_state
