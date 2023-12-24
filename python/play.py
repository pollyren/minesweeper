#!/usr/bin/env python3
import pygame
from board import Cell, Position
from logic import Game
import sys
import argparse
import time

PIECE_SIZE = 35
MARGIN = 20

# pygame event button constants
LEFT = 1
MIDDLE = 2
RIGHT = 3

game_state = True

def change_game_state() -> None:
    global game_state
    game_state = not game_state

def reset_game_state() -> None:
    global game_state
    game_state = True

def get_arguments() -> tuple:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--height', type=int, required=True, help='number of rows in the board')
    parser.add_argument('-w', '--width', type=int, required=True, help='number of columns in the board')
    parser.add_argument('-m', '--mines', type=int, required=True, help='number of mines in the game')
    parser.add_argument('--help', action='help')
    args = parser.parse_args()
    return (args.height, args.width, args.mines)

def show_game(game: Game, board: pygame.Surface, screen: pygame.Surface, font: pygame.font.Font) -> None:
    for i in range(len(game.get_board().get_cells())):
            for j in range(len(game.get_board().get_row(i))):
                piece = Piece(j, i, game.get_board().get_cell(Position(i, j)))
                piece.draw(board, font)
    screen.blit(board, (MARGIN, MARGIN))
    pygame.display.update()

class Piece:
    def __init__(self, x: int, y: int, cell: Cell):
        self.x = x
        self.y = y
        self.cell = cell

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        global game_state
        if self.cell.is_revealed():
            pygame.draw.rect(surface, (0, 0, 0), (self.x*PIECE_SIZE, self.y*PIECE_SIZE, PIECE_SIZE, PIECE_SIZE), 1)
            pygame.draw.rect(surface, (200, 200, 200) if not self.cell.is_detonated() else (250, 158, 0), (self.x*PIECE_SIZE+0.1, self.y*PIECE_SIZE+0.1, PIECE_SIZE-0.2, PIECE_SIZE-0.2))

            value = self.cell.get_value() if self.cell.is_clear() else 0
            text = str(value if value > 0 else '') if self.cell.is_clear() else '*'
            text_surface = font.render(text, True, (139, 0, 0) if text=='*' else (value*25, value*25, value*25))
            text_rect = text_surface.get_rect(center=(self.x*PIECE_SIZE+PIECE_SIZE/2, self.y*PIECE_SIZE+PIECE_SIZE/2+2.2*(text=='*')))
            surface.blit(text_surface, text_rect)
        elif self.cell.flagged:
            pygame.draw.rect(surface, (0, 0, 0), (self.x*PIECE_SIZE, self.y*PIECE_SIZE, PIECE_SIZE, PIECE_SIZE), 1)
            pygame.draw.rect(surface, (222, 222, 222), (self.x*PIECE_SIZE+0.1, self.y*PIECE_SIZE+0.1, PIECE_SIZE-0.2, PIECE_SIZE-0.2))

            text_surface = font.render('F', True, (0, 88, 0) if game_state or not self.cell.is_clear() else (200, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x*PIECE_SIZE+PIECE_SIZE/2, self.y*PIECE_SIZE+PIECE_SIZE/2))
            surface.blit(text_surface, text_rect)
        else: 
            pygame.draw.rect(surface, (0, 0, 0), (self.x*PIECE_SIZE, self.y*PIECE_SIZE, PIECE_SIZE, PIECE_SIZE), 1)
            pygame.draw.rect(surface, (222, 222, 222), (self.x*PIECE_SIZE+0.1, self.y*PIECE_SIZE+0.1, PIECE_SIZE-0.2, PIECE_SIZE-0.2))

    def __str__(self) -> str:
        return f'x {self.x}, y {self.y}, cell {self.cell}'

def main():
    height, width, nmines = get_arguments()

    game = Game(height, width, nmines)

    pygame.init()
    pygame.display.set_caption('minesweeper')

    screen = pygame.display.set_mode((width*PIECE_SIZE + 2*MARGIN, height*PIECE_SIZE + 2*MARGIN))
    board = pygame.Surface((width*PIECE_SIZE, height*PIECE_SIZE))
    font = pygame.font.SysFont('monospace', 30)

    board.fill((222, 222, 222))
    screen.blit(board, (MARGIN, MARGIN))
    pygame.display.flip()

    show_game(game, board, screen, font)

    start_time = time.time()
    ongoing = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                if not ongoing:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        game = Game(height, width, nmines)
                        reset_game_state()
                        start_time = time.time()
                        ongoing = True

                else: 
                    if event.key == pygame.K_SPACE:
                        yb, xb = pygame.mouse.get_pos()
                        x = (xb - MARGIN) // PIECE_SIZE
                        y = (yb - MARGIN) // PIECE_SIZE
                        pos = Position(x, y)

                        if x >= game.get_board().get_height() or y >= game.get_board().get_width() or x < 0 or y < 0:
                            continue

                        if game.get_board().get_cell(pos).is_revealed():
                            game.game_reveal_adjacents(pos)
                        else:
                            game.get_board().get_cell(pos).switch_flag()
                
                    if event.key == pygame.K_r:
                        game = Game(height, width, nmines)
                        reset_game_state()
                        start_time = time.time()

            if ongoing: # prevents moves after the game is over
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    yb, xb = pygame.mouse.get_pos()
                    x = (xb - MARGIN) // PIECE_SIZE
                    y = (yb - MARGIN) // PIECE_SIZE
                    pos = Position(x, y)

                    if x >= game.get_board().get_height() or y >= game.get_board().get_width() or x < 0 or y < 0:
                        continue
                    if game.get_board().get_cell(pos).is_revealed():
                        continue
                    while not game.get_board().get_cell(pos).is_clear() and game.get_clicks() == 0: # cannot lose on first move
                        game = Game(height, width, nmines)
                    if not game.get_board().get_cell(pos).is_clear(): 
                        print('you lose...game over...')
                        change_game_state()
                        game.get_board().get_cell(pos).detonate()
                        game.reveal_all_mines()
                        show_game(game, board, screen, font)
                        ongoing = False

                    game.game_reveal_adjacents(pos)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                    yb, xb = pygame.mouse.get_pos()
                    x = (xb - MARGIN) // PIECE_SIZE
                    y = (yb - MARGIN) // PIECE_SIZE
                    pos = Position(x, y)

                    if x >= game.get_board().get_height() or y >= game.get_board().get_width():
                        continue
                    game.get_board().get_cell(pos).switch_flag()

        board.fill((222, 222, 222))

        show_game(game, board, screen, font)
        if game.check_win():
            print(f'YOU WIN, time elapsed: {time.time() - start_time : 0,.5f}s')
            change_game_state()
            game.reveal_all_mines()
            show_game(game, board, screen, font)
            ongoing = False

if __name__ == '__main__':
    main()