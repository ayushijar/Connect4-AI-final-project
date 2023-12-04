import numpy as np
import itertools
import pygame
import random
import math


from pygame import gfxdraw
from variables import ROW_COUNT, COLUMN_COUNT, size, colors, SQUARESIZE, RADIUS, height, width, PLAYER_PIECE, AI_PIECE

# Creating game board
def create_connect4_board():
    return np.zeros((ROW_COUNT,COLUMN_COUNT))

# Creating the board
board = create_connect4_board()

# Checking if the top row of a selected column is empty or not
def check_valid_location(board, column):
    return board[ROW_COUNT-1][column] == 0

# Getting the lowest empty slot of the selected column
def find_next_available_row(board, column):
    for slot in range(ROW_COUNT):
        if board[slot][column] == 0:
            return slot

# Dropping the piece in the board
def drop_piece(board, row, column, piece):
    board[row][column] = piece

# Checking if the game is over
def check_game_over(board, piece):

    # Checking horizontal row
    for col, row in itertools.product(range(COLUMN_COUNT - 3), range(ROW_COUNT)):
        if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
            return True

    # Checking vertical row
    for col, row in itertools.product(range(COLUMN_COUNT), range(ROW_COUNT - 3)):
        if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
            return True

    # Checking positive slop diagonal row
    for col, row in itertools.product(range(COLUMN_COUNT - 3), range(ROW_COUNT - 3)):
        if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
            return True

    # Checking negative slop diagonal row
    for col, row in itertools.product(range(COLUMN_COUNT - 3), range(3, ROW_COUNT)):
        if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
            return True

    return False

# Setting screen size
screen = pygame.display.set_mode(size)

# Drawing board graphics
def draw_connect4_board(board):
    for col, row in itertools.product(range(COLUMN_COUNT), range(ROW_COUNT)):
        rect_pos = (col * SQUARESIZE, row * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)
        pygame.gfxdraw.box(screen, rect_pos, colors["BLUE"])
        x, y = (int(col * SQUARESIZE + SQUARESIZE / 2), int(row * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2))

        # Gradient shading for holes
        for offset in range(RADIUS):
            pygame.gfxdraw.filled_circle(screen, x, y, RADIUS - offset, (40 + offset, 40 + offset, 40 + offset))

    for col, row in itertools.product(range(COLUMN_COUNT), range(ROW_COUNT)):
        x, y = (int(col * SQUARESIZE + SQUARESIZE / 2), height - int(row * SQUARESIZE + SQUARESIZE / 2))
        color = None
        if board[row][col] == PLAYER_PIECE:
            color = colors["YELLOW"]
        elif board[row][col] == AI_PIECE:
            color = colors["RED"]

        if color:
            pygame.gfxdraw.filled_circle(screen, x, y, RADIUS, color)

        pygame.gfxdraw.aacircle(screen, x, y, RADIUS, colors["DARKGREY"])

    pygame.display.update()


def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if check_valid_location(board, col)]

def draw_dotted_circle(surface, x, y, radius, color, dot_length=4, gap_length=4, line_width=3):
    num_dots = int(2 * math.pi * radius / (dot_length + gap_length))
    angle_between_dots = 2 * math.pi / num_dots

    for i in range(num_dots):
        start_angle = i * angle_between_dots
        end_angle = start_angle + dot_length / radius

        start_x = x + radius * math.cos(start_angle)
        start_y = y + radius * math.sin(start_angle)

        end_x = x + radius * math.cos(end_angle)
        end_y = y + radius * math.sin(end_angle)

        pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), line_width)
