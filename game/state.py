import numpy as np

CHESS_SET = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6, "p": 9, "n": 10, "b": 11, "r": 12, "q": 13, "k": 14}


class State(object):
    def __init__(self,
                 raw_state,
                 ep_state,
                 has_white_queenside_castling_right,
                 has_white_kingside_castling_right,
                 has_black_queenside_castling_right,
                 has_black_kingside_castling_right,
                 ):

        self.raw_state = raw_state
        self.ep_state = ep_state
        self.has_white_kingside_castling_right = has_white_kingside_castling_right
        self.has_white_queenside_castling_right = has_white_queenside_castling_right
        self.has_black_kingside_castling_right = has_black_kingside_castling_right
        self.has_black_queenside_castling_right = has_black_queenside_castling_right
        