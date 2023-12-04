import itertools
import random

from variables import ROW_COUNT, COLUMN_COUNT, PLAYER_PIECE, AI_PIECE, WINDOW_LENGTH, EMPTY
from functions import get_valid_locations, find_next_available_row, drop_piece

# Evaluating scores of connections
def evaluate_window(window, piece):

    score = 0
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 50
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10

    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 75
    elif window.count(opponent_piece) == 2 and window.count(EMPTY) == 2:
        score -= 25

    return score

# Getting scores for connections
def score_position(game_board, piece, directions=(1, 1, 1, 1)):

    score = 0

    # Prefer center column for increased probablity of win based upon different score calculation
    centerArray = [int(i) for i in list(game_board[ : , COLUMN_COUNT//2])]
    centerCount = centerArray.count(piece)
    score += centerCount*10

    if directions[0]:
        # Horizontal row score
        for row in range(ROW_COUNT):
            rowArray = [int(i) for i in list(game_board[row , : ])]
            for col in range(COLUMN_COUNT - 3):
                window = rowArray[col : col + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

    if directions[1]:
        # Vertical row score
        for col in range(COLUMN_COUNT):
            colArray = [int(i) for i in list(game_board[ : , col])]
            for row in range(ROW_COUNT):
                window = colArray[row : row + WINDOW_LENGTH]
                score += evaluate_window(window, piece)
            

    if directions[2]:
        # Positive slope diagonal score
        for row, col in itertools.product(range(ROW_COUNT - 3), range(COLUMN_COUNT - 3)):
            window = [game_board[row + i][col + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    if directions[3]:
        # Negative slope diagonal score
        for row, col in itertools.product(range(ROW_COUNT - 3), range(COLUMN_COUNT - 3)):
            window = [game_board[row + 3 - i][col + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Picking best moves based on scores
def pick_best_move(game_board, piece, directions=(1, 1, 1, 1)):
    valid_locations = get_valid_locations(game_board)

    best_score = -10000
    best_column = random.choice(valid_locations)

    for col in valid_locations:
        row = find_next_available_row(game_board, col)
        temp_game_board = game_board.copy()
        drop_piece(temp_game_board, row, col, piece)
        score = score_position(temp_game_board, piece, directions)

        if score > best_score:
            best_score = score
            best_column = col

    return best_column
