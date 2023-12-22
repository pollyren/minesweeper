#!/usr/bin/env python3
import pygame
from board import Cell, Position
from logic import Game
import sys
import argparse

PIECE_SIZE = 35
MARGIN = 20

# pygame event button constants
LEFT = 1
MIDDLE = 2
RIGHT = 3

def get_arguments() -> tuple:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--height', type=int, required=True, help='number of rows in the board')
    parser.add_argument('-w', '--width', type=int, required=True, help='number of columns in the board')
    parser.add_argument('-b', '--bombs', type=int, required=True, help='number of bombs in the game')
    parser.add_argument('--help', action='help')
    args = parser.parse_args()
    return (args.height, args.width, args.bombs)

def show_game(game: Game, board: pygame.Surface, screen: pygame.Surface, font: pygame.font.Font) -> None:
    for i in range(len(game.board.cells)):
            for j in range(len(game.board.get_row(i))):
                piece = Piece(j, i, game.board.get_cell(Position(i, j)))
                piece.draw(board, font)
    screen.blit(board, (MARGIN, MARGIN))
    pygame.display.update()

class Piece:
    def __init__(self, x: int, y: int, cell: Cell):
        self.x = x
        self.y = y
        self.cell = cell

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        if self.cell.revealed:
            pygame.draw.rect(surface, (0, 0, 0), (self.x*PIECE_SIZE, self.y*PIECE_SIZE, PIECE_SIZE, PIECE_SIZE), 1)
            pygame.draw.rect(surface, (200, 200, 200) if not self.cell.detonated else (250, 158, 0), (self.x*PIECE_SIZE+0.1, self.y*PIECE_SIZE+0.1, PIECE_SIZE-0.2, PIECE_SIZE-0.2))

            value = self.cell.value if self.cell.clear else 0
            text = str(value if value > 0 else '') if self.cell.clear else '*'
            text_surface = font.render(text, True, (139, 0, 0) if text=='*' else (value*25, value*25, value*25))
            text_rect = text_surface.get_rect(center=(self.x*PIECE_SIZE+PIECE_SIZE/2, self.y*PIECE_SIZE+PIECE_SIZE/2+2.2*(text=='*')))
            surface.blit(text_surface, text_rect)
        elif self.cell.flagged:
            pygame.draw.rect(surface, (0, 0, 0), (self.x*PIECE_SIZE, self.y*PIECE_SIZE, PIECE_SIZE, PIECE_SIZE), 1)
            pygame.draw.rect(surface, (222, 222, 222), (self.x*PIECE_SIZE+0.1, self.y*PIECE_SIZE+0.1, PIECE_SIZE-0.2, PIECE_SIZE-0.2))

            text_surface = font.render('F', True, (0, 88, 0))
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

    ongoing = True
    while ongoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    yb, xb = pygame.mouse.get_pos()
                    x = (xb - MARGIN) // PIECE_SIZE
                    y = (yb - MARGIN) // PIECE_SIZE
                    pos = Position(x, y)

                    if x >= game.board.height or y >= game.board.width:
                        continue

                    if game.board.get_cell(pos).revealed:
                        game.game_reveal_adjacents(pos)
                    else:
                        game.board.get_cell(pos).switch_flag()
                
                if event.key == pygame.K_r:
                    game = Game(height, width, nmines)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                yb, xb = pygame.mouse.get_pos()
                x = (xb - MARGIN) // PIECE_SIZE
                y = (yb - MARGIN) // PIECE_SIZE
                pos = Position(x, y)

                if x >= game.board.height or y >= game.board.width:
                    continue
                if game.board.get_cell(pos).revealed:
                    continue
                while not game.board.get_cell(pos).clear and game.clicks == 0: # cannot lose on first move
                    print('new game')
                    game = Game(height, width, nmines)
                if not game.board.get_cell(pos).clear: 
                    game.board.get_cell(pos).detonated = True
                    game.reveal_all_mines()
                    show_game(game, board, screen, font)

                game.game_reveal_adjacents(pos)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                yb, xb = pygame.mouse.get_pos()
                x = (xb - MARGIN) // PIECE_SIZE
                y = (yb - MARGIN) // PIECE_SIZE
                pos = Position(x, y)

                if x >= game.board.height or y >= game.board.width:
                    continue
                game.board.get_cell(pos).switch_flag()

        board.fill((222, 222, 222))

        show_game(game, board, screen, font)
        if game.check_win():
            game.reveal_all()
            show_game(game, board, screen, font)

    print('game overrr')
    print(game.board)

if __name__ == '__main__':
    main()