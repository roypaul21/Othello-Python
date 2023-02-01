import pygame
from Othello import player, interface, OthelloBoard, log
from Othello.settings import BLACK, WHITE, User

logger = log.setup_custom_logger('root')

# start
class OthelloGame:

    def __init__(self):
        self.gui = interface.Gui()
        self.board = OthelloBoard.Board()
        self.gui.show_menu(self.start)

    def start(self, *args):
        player1, player2, level = args
        logger.info('Settings: player 1: %s, player 2: %s, level: %s ', player1, player2, level)
        if player1 == User:
            self.now_playing = player.User(self.gui, BLACK)
        else:
            self.now_playing = player.Computer(BLACK, level + 3)
        if player2 == User:
            self.other_player = player.User(self.gui, WHITE)
        else:
            self.other_player = player.Computer(WHITE, level + 3)

        self.gui.show_game()
        self.gui.update(self.board.board, 2, 2, self.now_playing.color)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            if self.board.game_ended():
                whites, blacks, empty = self.board.count_stones()
                if whites > blacks:
                    winner = WHITE
                elif blacks > whites:
                    winner = BLACK
                else:
                    winner = None
                break
            self.now_playing.get_current_board(self.board)
            valid_moves = self.board.get_valid_moves(self.now_playing.color)
            if valid_moves != []:
                score, self.board = self.now_playing.get_move()
                whites, blacks, empty = self.board.count_stones()
                self.gui.update(self.board.board, blacks, whites,
                                self.now_playing.color)
            self.now_playing, self.other_player = self.other_player, self.now_playing
        self.gui.show_winner(winner)
        pygame.time.wait(1000)
        self.restart()

    def restart(self):
        self.board = OthelloBoard.Board()
        self.gui.show_menu(self.start)
        self.run()


def main():
    game = OthelloGame()
    game.run()


if __name__ == '__main__':
    main()
