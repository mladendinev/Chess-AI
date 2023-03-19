def min_max(pos, depth, max_player):
    if max_depth == 0 and pos.is_leaf():
        # TODO: change this to heuristic
        return 0
    if max_player:
        value = float('-inf')
        for move in pos.legal_moves():
            value = max(value, min_max(move, depth - 1, False))

        return value
    else:
        value = float("+inf")
        for move in pos.legal_moves():
            value = min(value, min_max(move, depth - 1, True))
