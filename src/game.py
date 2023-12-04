import pygame
import sys
import math
import random
import time

from enum import Enum
from variables import ROW_COUNT, COLUMN_COUNT, SQUARESIZE, size, RADIUS, colors, height, width, PLAYER, AI, \
    PLAYER_PIECE, AI_PIECE,game_end_button_width, game_end_button_height, level_button_height, \
    level_button_width
from functions import create_board, is_valid_location, get_next_open_row, drop_piece, game_over_check, draw_board, \
    board, screen, draw_dotted_circle
from score_ai import score_position
from minmax_ai import minimax
from ui_components import Button
#from ui_components import ai_move_sound, self_move_sound, ai_wins_sound, player_wins_sound

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    DIFFICULT = 3
    CHALLENGING = 4
    UNBEATABLE = 5

class ConnectFour:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() #added to initialize sound
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
        self.restart_button = Button(colors["GREEN"], self.center_x, restart_button_y,
                                     game_end_button_width, game_end_button_height,
                                     'Restart')
        pygame.display.set_caption("Connect Four")
        self.difficulty = self.choose_difficulty()
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
                #self_move_sound.play()
                self._extracted_from_ai_move_7(col, PLAYER_PIECE, "You win!! ^_^")
                self.turn ^= 1
                self.render_thinking("Thinking...")
                draw_board(self.board)
        if self.game_over:
            if self.quit_button.is_over((posx, event.pos[1])):
                sys.exit()
            elif self.restart_button.is_over((posx, event.pos[1])):
                self.__init__()


    def ai_move(self):
        if self.difficulty == Difficulty.EASY:
            col, minimaxScore, no_of_nodes_explored, pruned_nodes = minimax(self.board, 2, -math.inf, math.inf, True, 0, 0)
        if self.difficulty == Difficulty.MEDIUM:
            col, minimaxScore, no_of_nodes_explored, pruned_nodes = minimax(self.board, 3, -math.inf, math.inf, True, 0, 0)
        if self.difficulty == Difficulty.DIFFICULT:
            col, minimaxScore, no_of_nodes_explored, pruned_nodes = minimax(self.board, 4, -math.inf, math.inf, True, 0, 0)
        if self.difficulty == Difficulty.CHALLENGING:
            col, minimaxScore, no_of_nodes_explored, pruned_nodes = minimax(self.board, 6, -math.inf, math.inf, True, 0, 0)
        if self.difficulty == Difficulty.UNBEATABLE:
            col, minimaxScore, no_of_nodes_explored, pruned_nodes = minimax(self.board, 7, -math.inf, math.inf, True, 0, 0)
        print("\n")
        print("No of explored nodes",no_of_nodes_explored)
        print("No of pruned nodes", pruned_nodes)
        print("Column",col+1) 
        print("Winning factor for AI", minimaxScore)
        print("\n")
        if is_valid_location(self.board, col):
            #ai_move_sound.play()
            self._extracted_from_ai_move_7(col, AI_PIECE, "AI wins!! :[")
            self.turn ^= 1

    # TODO Rename this here and in `handle_mouse_button_down` and `ai_move`
    def _extracted_from_ai_move_7(self, col, arg1, arg2):
        row = get_next_open_row(self.board, col)
        drop_piece(self.board, row, col, arg1)
        draw_board(self.board)
        pygame.display.update()
        if game_over_check(self.board, arg1):
            self.display_winner(self.board, arg2)
            self.game_over = True
            return self.handle_game_over()

    def display_winner(self,board, message):
        if message == "AI wins!! :[":
            print("AI wins!! :[")
            print("AI Score:", score_position(board,AI_PIECE))
            #ai_wins_sound.play()
        elif message == "You win!! ^_^":
            print("You win!! ^_^")
            print("Your Score:", score_position(board,PLAYER_PIECE))
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


    def choose_difficulty(self):
        btn_height = 90
        text_color = colors['DARKGREY']
        btn_y = [i * (btn_height + 20) + height/1.8 for i in range(-3,3)]
        self.easy = Button(colors['GREEN'], self.center_x,
                           btn_y[0], 250, btn_height,
                           'EASY',
                           text_color=text_color)
        self.MEDIUM = Button(colors['GREEN'], self.center_x,
                            btn_y[1], 250, btn_height,
                            'MEDIUM',
                            text_color=text_color)

        self.DIFFICULT = Button(colors['YELLOW'], self.center_x,
                           btn_y[2], 250, btn_height,
                           'DIFFICULT',
                           text_color=text_color)
        self.CHALLENGING = Button(colors['YELLOW'], self.center_x,
                                 btn_y[3], 250, btn_height,
                                 'CHALLENGING',
                                 text_color=text_color)
        self.UNBEATABLE = Button(colors['RED'], self.center_x,
                              btn_y[4], 250, btn_height,
                              'UNBEATABLE',
                                text_color=text_color)

        screen.fill(colors['GREY'])
        self.easy.draw(screen)
        self.MEDIUM.draw(screen)
        self.DIFFICULT.draw(screen)
        self.CHALLENGING.draw(screen)
        self.UNBEATABLE.draw(screen)

        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    if self.easy.is_over((posx, posy)):
                        return Difficulty.EASY
                    elif self.MEDIUM.is_over((posx, posy)):
                        return Difficulty.MEDIUM
                    elif self.DIFFICULT.is_over((posx, posy)):
                        return Difficulty.DIFFICULT
                    elif self.CHALLENGING.is_over((posx, posy)):
                        return Difficulty.CHALLENGING
                    elif self.UNBEATABLE.is_over((posx, posy)):
                        return Difficulty.UNBEATABLE


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
