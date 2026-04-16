# chess.py

SIZE = 3  # 棋盘大小为3x3

def check_win(board, player):
    """检查是否获胜
    Args:
        board: 棋盘状态
        player: 'X' 或 'O'
    Returns:
        bool: 是否获胜
    """
    # 检查行
    for row in board:
        if row.count(player) == SIZE:
            return True

    # 检查列
    for col in range(SIZE):
        if [board[row][col] for row in range(SIZE)].count(player) == SIZE:
            return True

    # 检查主对角线
    if [board[i][i] for i in range(SIZE)].count(player) == SIZE:
        return True

    # 检查副对角线
    if [board[i][SIZE - 1 - i] for i in range(SIZE)].count(player) == SIZE:
        return True

    return False

def check_draw(board):
    """检查是否平局"""
    return all(cell != " " for row in board for cell in row)

def check_turn(board):
    """检查当前轮到谁下棋
    Returns:
        'X' 或 'O': 当前应该下棋的一方
    """
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    # 黑棋X先行
    return "X" if x_count == o_count else "O"

def evaluate(board):
    """评估当前棋盘状态的分数
    Returns:
        int: 分数(10表示AI胜，-10表示玩家胜，0表示平局或未结束)
    """
    if check_win(board, 'X'):
        return 10
    elif check_win(board, 'O'):
        return -10
    return 0

def get_empty_cells(board):
    """获取所有空位置
    Returns:
        list: 空位置的坐标列表 [(row, col), ...]
    """
    return [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == ' ']

def minimax(board, depth, is_maximizing):
    """极小化极大算法
    Args:
        board: 当前棋盘状态
        depth: 当前搜索深度
        is_maximizing: 是否是极大化玩家
    Returns:
        int: 最优分数
    """
    score = evaluate(board)

    # 如果有一方胜利，返回分数
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth

    # 如果平局，返回0
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'X'
            score = minimax(board, depth + 1, False)
            board[i][j] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'O'
            score = minimax(board, depth + 1, True)
            board[i][j] = ' '
            best_score = min(score, best_score)
        return best_score

def computer_move(board):
    """AI下棋
    Args:
        board: 当前棋盘状态
    Returns:
        tuple: (row, col) 最优落子位置
    """
    # 如果是空棋盘，直接下在中间
    if board == [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]:
        return 1, 1

    current_piece = check_turn(board)  # 获取当前应该下的棋子
    is_maximizing = current_piece == 'X'  # 如果是X则为极大化玩家

    best_score = float('-inf') if is_maximizing else float('inf')
    best_move = (-1, -1)

    for i, j in get_empty_cells(board):
        board[i][j] = current_piece
        score = minimax(board, 0, not is_maximizing)
        board[i][j] = ' '

        if is_maximizing:
            if score > best_score:
                best_score = score
                best_move = (i, j)
        else:
            if score < best_score:
                best_score = score
                best_move = (i, j)

    return best_move

def computer_move_for(board, piece):
    """根据传入的棋子（piece）计算AI最佳落子位置
    Args:
        board: 当前棋盘状态
        piece: "X" 或 "O"，表示AI将使用的棋子
    Returns:
        (row, col): 最优落子位置
    """
    is_maximizing = (piece == 'X')
    best_score = float('-inf') if is_maximizing else float('inf')
    best_move = (-1, -1)

    for i, j in get_empty_cells(board):
        board[i][j] = piece
        score_val = minimax(board, 0, not is_maximizing)
        board[i][j] = " "

        if is_maximizing:
            if score_val > best_score:
                best_score = score_val
                best_move = (i, j)
        else:
            if score_val < best_score:
                best_score = score_val
                best_move = (i, j)

    return best_move

def is_valid_move(board, row, col):
    """检查移动是否有效
    Args:
        board: 当前棋盘状态
        row: 行坐标
        col: 列坐标
    Returns:
        bool: 移动是否有效
    """
    if row < 0 or row >= SIZE or col < 0 or col >= SIZE:
        return False
    return board[row][col] == " "
