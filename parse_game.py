import chess.pgn
import numpy as np

from game.board import Board

RESULT = {'1/2-1/2': 0, '0-1': -1, '1-0': 1}


def read_dataset(file):
    pgn = open(file)
    count = 0
    X_train, Y_train = [], []
    while True:
        game = chess.pgn.read_game(pgn)
        if not game:
            break
        board = game.board()
        result = game.headers["Result"]
        if result not in RESULT:
            continue

        end_result = RESULT[result]

        for move in game.mainline_moves():
            board.push(move)
            serialized_board = Board(board).serialize()
            X_train.append(serialized_board)
            Y_train.append(end_result)
        count += 1

        print(f"Game {count}, winner {board.outcome()}")

    return np.array(X_train), np.array(Y_train)


if __name__ == '__main__':
    X, Y = read_dataset("/Users/mladendinev/PycharmProjects/ChessAI/data/Nakamura.pgn")
    np.savez("data/dataset_6000.npz", X, Y)
