import pygame
import sys
import math
import random
import time

from enum import Enum
from variables import ROW_COUNT, COLUMN_COUNT, SQUARESIZE, size, RADIUS, colors, height, width, PLAYER, AI, \
    PLAYER_PIECE, AI_PIECE, thinking_time, game_end_button_width, game_end_button_height, level_button_height, \
    level_button_width
from functions import create_board, is_valid_location, get_next_open_row, drop_piece, game_over_check, draw_board, \
    board, screen, draw_dotted_circle
from score_ai import pick_best_move
from minmax_ai import minimax
from ui_components import Button

class ConnectFour:
    def __init__(self):
        pygame.init()
        self.game_over = False
        self.turn = random.randint(PLAYER, AI)
        self.board = create_board()
        self.myfont = pygame.font.SysFont("monospace", 80)
        padding = 20
        restart_button_y = height // 2
        quit_button_y = restart_button_y + game_end_button_height + padding
        self.center_x = width // 2 - game_end_button_width // 2
        self.quit_button = Button(colors["RED"], self.center_x, quit_button_y, game_end_button_width,
                                  game_end_button_height, 'Quit')
        self.restart_button = Button(colors["YELLOW"], self.center_x, restart_button_y,
                                     game_end_button_width, game_end_button_height,
                                     'Restart')
        pygame.display.set_caption("Connect Four")
        screen.fill(colors["DARKGREY"])
        draw_board(self.board)
        pygame.display.update()

    def handle_mouse_motion(self, event):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))
        posx = event.pos[0]
        if self.turn == PLAYER:
            draw_dotted_circle(screen, posx, int(SQUARESIZE / 2), RADIUS, colors["YELLOW"], gap_length=6)
        pygame.display.update()

    def handle_mouse_button_down(self, event):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))
        posx = event.pos[0]
        if self.turn == PLAYER:
            col = int(math.floor(posx / SQUARESIZE))
            if is_valid_location(self.board, col):
                self._extracted_from_ai_move_7(col, PLAYER_PIECE, "You win!! ^_^")
                self.turn ^= 1
                self.render_thinking("Lemme Think...")
                draw_board(self.board)
        if self.game_over:
            if self.quit_button.is_over((posx, event.pos[1])):
                sys.exit()
            elif self.restart_button.is_over((posx, event.pos[1])):
                self.__init__()


    def ai_move(self):
        thinking_time = 1
        col, minimaxScore = minimax(self.board, 7, -math.inf, math.inf, True)
        if is_valid_location(self.board, col):
            self._extracted_from_ai_move_7(col, AI_PIECE, "AI wins!! :[")
            self.turn ^= 1

    # TODO Rename this here and in `handle_mouse_button_down` and `ai_move`
    def _extracted_from_ai_move_7(self, col, arg1, arg2):
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, arg1)
        draw_board(self.board)
        pygame.display.update()
        if game_over_check(self.board, arg1):
            self.display_winner(arg2)
            self.game_over = True
            return self.handle_game_over()

    def display_winner(self, message):
        #how can we display message??
        #if message == "AI wins!! :[":
            #ai_wins_sound.play()
        #elif message == "You win!! ^_^":
            #player_wins_sound.play()
        label = self.myfont.render(message, 1, colors["DARKGREY"])
        screen.blit(label, (40, 10))
        pygame.display.update()

    def handle_game_over(self):
        self.clear_label()
        draw_board(self.board)
        self.quit_button.draw(screen, outline_color=colors["DARKGREY"])
        self.restart_button.draw(screen, outline_color=colors["DARKGREY"])
        pygame.display.update()
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    if self.quit_button.is_over((posx, posy)):
                        sys.exit()
                    elif self.restart_button.is_over((posx, posy)):
                        self.__init__()
                        return self.game_start()

            pygame.display.update()

    def game_start(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
            if self.turn == AI and not self.game_over:
                self.ai_move()
            if self.game_over:
                self.handle_game_over()

            pygame.display.update()

    def clear_label(self):
        pygame.draw.rect(screen, colors["DARKGREY"], (0, 0, width, SQUARESIZE))


    def render_thinking(self, text):
        self.clear_label()
        label = pygame.font.SysFont("monospace", 60).render(text, 1, colors["YELLOW"])
        screen.blit(label, (40, 10))
        pygame.display.update()

if __name__ == "__main__":
    game = ConnectFour()
    game.game_start()


# TODO Complete the game and make a downloadable file for the game. Use pybag to take the game to the web.
