import math
import random

from variables import ROW_COUNT, COLUMN_COUNT, PLAYER_PIECE, AI_PIECE
from functions import check_valid_location, check_game_over, find_next_available_row, drop_piece
from score_ai import evaluate_current_score


no_of_nodes_explored = 0
pruned_nodes = 0

# Getting valid locations for AI
def get_valid_locations(game_board):
    return [col for col in range(COLUMN_COUNT) if check_valid_location(game_board, col)]

# Checking for terminal nodes
def is_terminal_node(game_board):
    return check_game_over(game_board, PLAYER_PIECE) or check_game_over(game_board, AI_PIECE) or len(get_valid_locations(game_board)) == 0

# Implimenting minimax algorithm
def minimax(game_board, depth, alpha, beta, maximizing_player):
    global no_of_nodes_explored, pruned_nodes
    valid_locations = get_valid_locations(game_board)

    if is_terminal_node(game_board):
        if check_game_over(game_board, AI_PIECE):
            return (None, math.inf)
        elif check_game_over(game_board, PLAYER_PIECE):
            return (None, -math.inf)
        else: 
            return (None, 0)
    elif depth == 0:
        return (None, evaluate_current_score(game_board, AI_PIECE))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = find_next_available_row(game_board, col)
            temp_game_board = game_board.copy()
            drop_piece(temp_game_board, row, col, AI_PIECE)
            no_of_nodes_explored+=1
            new_score = minimax(temp_game_board, depth - 1, alpha, beta, False)[1]

            if new_score > value:
                value = new_score
                column = col
            
            alpha = max(alpha, value)

            if alpha >= beta:
                pruned_nodes += 1
                break

    # Minimizing player
    else:
        value = math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            row = find_next_available_row(game_board, col)
            temp_game_board = game_board.copy()
            drop_piece(temp_game_board, row, col, PLAYER_PIECE)
            no_of_nodes_explored+=1
            new_score = minimax(temp_game_board, depth - 1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                column = col

            beta = min(beta, value)

            if alpha >= beta:
                pruned_nodes += 1
                break       
    return column, value, no_of_nodes_explored, pruned_nodes