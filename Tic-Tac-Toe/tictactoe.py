import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid action: cell is already filled")

    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    for line in (
        board
        + list(zip(*board))
        + [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]
    ):
        if line == [X, X, X]:
            return X
        if line == [O, O, O]:
            return O
    return None


def terminal(board):
    return winner(board) is not None or all(
        cell is not EMPTY for row in board for cell in row
    )


def utility(board):
    win = winner(board)
    if win == X:
        return 1
    if win == O:
        return -1
    return 0


def minimax(board):
    if terminal(board):
        return None

    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    current_player = player(board)
    if current_player == X:
        best_value = -math.inf
        best_action = None
        for action in actions(board):
            action_value = min_value(result(board, action))
            if action_value > best_value:
                best_value = action_value
                best_action = action
        return best_action
    else:
        best_value = math.inf
        best_action = None
        for action in actions(board):
            action_value = max_value(result(board, action))
            if action_value < best_value:
                best_value = action_value
                best_action = action
        return best_action
