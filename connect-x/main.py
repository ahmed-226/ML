import numpy as np
import random

def get_valid_moves(board, config):
    """Get list of valid column moves"""
    return [col for col in range(config.columns) if board[col] == 0]

def drop_piece(board, col, mark, config):
    """Simulate dropping a piece in a column"""
    board = board.copy()
    for row in range(config.rows-1, -1, -1):
        if board[row * config.columns + col] == 0:
            board[row * config.columns + col] = mark
            break
    return board

def check_winner(board, config):
    """Check if there's a winner on the board"""
    rows, cols, inarow = config.rows, config.columns, config.inarow
    grid = np.array(board).reshape(rows, cols)
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                continue
            directions = [(0,1), (1,0), (1,1), (1,-1)]
            for delta_row, delta_col in directions:
                count = 1
                for direction in [1, -1]:
                    r, c = row + direction * delta_row, col + direction * delta_col
                    while (0 <= r < rows and 0 <= c < cols and 
                           grid[r][c] == grid[row][col]):
                        count += 1
                        r += direction * delta_row
                        c += direction * delta_col
                if count >= inarow:
                    return grid[row][col]
    return 0

def evaluate_window(window, mark):
    """Evaluate a 4-piece window"""
    score = 0
    opp_mark = 1 if mark == 2 else 2
    if isinstance(window, np.ndarray):
        window = window.tolist()
    mark_count = window.count(mark)
    opp_count = window.count(opp_mark)
    empty_count = window.count(0)
    if mark_count == 4:
        score += 100
    elif mark_count == 3 and empty_count == 1:
        score += 10
    elif mark_count == 2 and empty_count == 2:
        score += 2
    if opp_count == 3 and empty_count == 1:
        score -= 80
    return score

def evaluate_position(board, mark, config):
    """Evaluate board position for the given mark"""
    rows, cols = config.rows, config.columns
    grid = np.array(board).reshape(rows, cols)
    score = 0
    for row in range(rows):
        for col in range(cols):
            if col + config.inarow <= cols:
                window = grid[row, col:col+config.inarow]
                score += evaluate_window(window, mark)
            if row + config.inarow <= rows:
                window = grid[row:row+config.inarow, col]
                score += evaluate_window(window, mark)
            if row + config.inarow <= rows and col + config.inarow <= cols:
                window = [grid[row+i, col+i] for i in range(config.inarow)]
                score += evaluate_window(window, mark)
            if row + config.inarow <= rows and col - config.inarow + 1 >= 0:
                window = [grid[row+i, col-i] for i in range(config.inarow)]
                score += evaluate_window(window, mark)
    return score

def minimax_agent(obs, config, depth=3):
    """Minimax agent with alpha-beta pruning"""
    def minimax(board, depth, alpha, beta, maximizing_player, mark):
        valid_moves = get_valid_moves(board, config)
        winner = check_winner(board, config)
        if winner == mark:
            return 100000
        elif winner != 0:
            return -100000
        elif len(valid_moves) == 0:
            return 0
        elif depth == 0:
            return evaluate_position(board, mark, config)
        if maximizing_player:
            max_eval = float('-inf')
            for col in valid_moves:
                new_board = drop_piece(board, col, mark, config)
                eval_score = minimax(new_board, depth-1, alpha, beta, False, mark)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opp_mark = 1 if mark == 2 else 2
            for col in valid_moves:
                new_board = drop_piece(board, col, opp_mark, config)
                eval_score = minimax(new_board, depth-1, alpha, beta, True, mark)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    valid_moves = get_valid_moves(obs.board, config)
    if not valid_moves:
        return 0
    best_move = valid_moves[0]
    best_score = float('-inf')
    for col in valid_moves:
        new_board = drop_piece(obs.board, col, obs.mark, config)
        score = minimax(new_board, depth-1, float('-inf'), float('inf'), False, obs.mark)
        if score > best_score:
            best_score = score
            best_move = col
    return best_move

def safe_agent(obs, config):
    """Safe agent that always returns a valid move"""
    valid_moves = get_valid_moves(obs.board, config)
    if not valid_moves:
        return 0
    center = config.columns // 2
    for offset in range(config.columns):
        for direction in [0, 1, -1]:
            col = center + direction * offset
            if 0 <= col < config.columns and col in valid_moves:
                return col
    return valid_moves[0]

def agent(obs, config):
    """
    ConnectX agent for Kaggle submission.
    Uses minimax with alpha-beta pruning, falls back to safe agent on error.
    """
    try:
        return minimax_agent(obs, config, depth=3)
    except Exception:
        return safe_agent(obs, config)