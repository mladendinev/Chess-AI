import numpy as np
from dataclasses import dataclass

@dataclass
class State(object):
    raw_state: str
    ep_state: bool
    has_white_queenside_castling_right: bool
    has_white_kingside_castling_right: bool
    has_black_queenside_castling_right: bool
    has_black_kingside_castling_right: bool