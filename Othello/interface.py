import pygame
import sys
from pygame.locals import *
import time
from .settings import BLACK, WHITE, DEFAULT_LEVEL, User, COMPUTER
import os
import pygame_menu
import logging

logger = logging.getLogger('root')

class Gui:
    def __init__(self):
        pygame.init()

        # colors
        self.BLACK = (0, 0, 0)                                              
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (128, 128, 0)

        # display
        self.SCREEN_SIZE = (640, 480)
        self.BOARD_POS = (100, 20)
        self.BOARD = (120, 40)
        self.BOARD_SIZE = 400
        self.SQUARE_SIZE = 50
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        # messages
        self.BLACK_LAB_POS = (5, self.SCREEN_SIZE[1] / 4)
        self.WHITE_LAB_POS = (560, self.SCREEN_SIZE[1] / 4)
        self.font = pygame.font.SysFont("Times New Roman", 22)
        self.scoreFont = pygame.font.SysFont("Serif", 58)
        self.user = pygame.font.SysFont("Serif", 30)

        # image files
        self.BACKGROUND = pygame.image.load(os.path.join("Othello/Assets","Background.png"))
        self.board_img = pygame.image.load(os.path.join("Othello/Assets", "board.bmp")).convert()
        self.black_img = pygame.image.load(os.path.join("Othello/Assets", "preta.bmp")).convert()       
        self.white_img = pygame.image.load(os.path.join("Othello/Assets", "branca.bmp")).convert()         
        self.tip_img = pygame.image.load(os.path.join("Othello/Assets", "tip.bmp")).convert()                                                
        self.clear_img = pygame.image.load(os.path.join("Othello/Assets", "empty.bmp")).convert()
                                                        

    def show_menu(self, start):

        self.level = DEFAULT_LEVEL
        self.player1 = User
        self.player2 = COMPUTER

        font = pygame_menu.font.FONT_DIGITAL
        
        self.menu = pygame_menu.Menu('Othello', 640, 480,
                                     theme=pygame_menu.themes.THEME_DARK)

        self.menu.add.button('Start Game', lambda: start(self.player1, self.player2, self.level))

        self.menu.mainloop(self.screen)

    def set_player_1(self, value, player):
        logger.debug('value:%s, player:%s', value, player)
        self.player1 = [0, User, COMPUTER][player]

    def set_player_2(self, value, player):
        logger.debug('value:%s, player:%s', value, player)
        self.player2 = [0, User, COMPUTER][player]

    def reset_menu(self):
        self.menu.disable()
        self.menu.reset(2)

    def show_winner(self, player_color):
        font = pygame.font.SysFont("Courier New", 34, bold = pygame.font.Font.bold)
        if player_color == WHITE:
            self.screen.fill(pygame.Color(255, 255, 255, 50))
            msg = font.render("White player wins", True, self.BLACK)
            
        elif player_color == BLACK:
            self.screen.fill(pygame.Color(0, 0, 0, 50))
            msg = font.render("Black player wins", True, self.WHITE)
        else:
            self.screen.fill(pygame.Color(0, 0, 0, 50))
            msg = font.render("Tie !", True, self.WHITE)
        self.screen.blit(
            msg, msg.get_rect(
                centerx=self.screen.get_width() / 2, centery=120))
        pygame.display.flip()

    def show_game(self):
        """ Game screen. """
        self.reset_menu()

        # draws initial screen
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.blit(self.BACKGROUND, (0, 0))
        self.score_size = 50
        self.score1 = pygame.Surface((self.score_size, self.score_size))
        self.score2 = pygame.Surface((self.score_size, self.score_size))
        self.screen.blit(self.background, (0, 0), self.background.get_rect())
        self.screen.blit(self.board_img, self.BOARD_POS,
                         self.board_img.get_rect())
        self.put_stone((3, 3), WHITE)
        self.put_stone((4, 4), WHITE)
        self.put_stone((3, 4), BLACK)
        self.put_stone((4, 3), BLACK)
        pygame.display.flip()

    def put_stone(self, pos, color):
        """ draws piece with given position and color """
        if pos == None:
            return

        # flip orientation (because xy screen orientation)
        pos = (pos[1], pos[0])

        if color == BLACK:
            img = self.black_img
        elif color == WHITE:
            img = self.white_img
        else:
            img = self.tip_img

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]

        self.screen.blit(img, (x, y), img.get_rect())
        pygame.display.flip()

    def clear_square(self, pos):
        """ Puts in the given position a background image, to simulate that the
        piece was removed.
        """
        # flip orientation
        pos = (pos[1], pos[0])

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]
        self.screen.blit(self.clear_img, (x, y), self.clear_img.get_rect())
        pygame.display.flip()

    def get_mouse_input(self):
        """ Get place clicked by mouse
        """
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()

                    # click was out of board, ignores
                    if mouse_x > self.BOARD_SIZE + self.BOARD[0] or \
                       mouse_x < self.BOARD[0] or \
                       mouse_y > self.BOARD_SIZE + self.BOARD[1] or \
                       mouse_y < self.BOARD[1]:
                        continue

                    # find place
                    position = ((mouse_x - self.BOARD[0]) // self.SQUARE_SIZE), \
                               ((mouse_y - self.BOARD[1]) // self.SQUARE_SIZE)
                    # flip orientation
                    position = (position[1], position[0])
                    return position

                elif event.type == QUIT:
                    sys.exit(0)

            time.sleep(.05)

    def update(self, board, blacks, whites, current_player_color):
        """Updates screen
        """
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    self.put_stone((i, j), board[i][j])

        blacks_str = '%02d' % int(blacks)
        whites_str = '%02d ' % int(whites)
        
        self.showScore(blacks_str, whites_str, current_player_color)
        print(current_player_color)
        pygame.display.flip()

    def showScore(self, blackStr, whiteStr, current_player_color):
        print(current_player_color)
        self.font_bg = (205,137,84,255)

        player_text = self.user.render("YOU!", True, self.BLACK)
        self.screen.blit(player_text, (10, 100))  

        text = self.scoreFont.render(blackStr, True, self.BLACK, self.font_bg)
        self.screen.blit(text, (self.BLACK_LAB_POS[0] + 10, self.BLACK_LAB_POS[1] + 40))   
        
        ai_text = self.user.render("A.I.", True, self.WHITE)
        self.screen.blit(ai_text, (565, 100)) 

        text2 = self.scoreFont.render(whiteStr, True, self.WHITE, self.font_bg)  
        self.screen.blit(text2, (self.WHITE_LAB_POS[0], self.WHITE_LAB_POS[1] + 40))                            
                                

    def wait_quit(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                break

    def show_valid_moves(self, valid_moves):
        logger.debug('valid movies: %s', valid_moves)
        for move in valid_moves:
            self.put_stone(move, 'tip')
