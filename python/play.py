#!/usr/bin/env python3
import pygame
from board import Cell, Position
from logic import Game
import sys
import argparse

PIECE_SIZE = 30
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

def show_game(game: Game, board: pygame.Surface, screen: pygame.Surface) -> None:
    for i in range(len(game.board.cells)):
            for j in range(len(game.board.get_row(i))):
                piece = Piece(j, i, game.board.get_cell(Position(i, j)))
                piece.draw(board)
    screen.blit(board, (MARGIN, MARGIN))
    pygame.display.update()

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 30)

class Piece:
    def generate_text_colour(n: int) -> tuple:
        return (n*20, n*20, n*20)

    def __init__(self, x: int, y: int, cell: Cell):
        self.x = x
        self.y = y
        self.cell = cell

    def draw(self, surface: pygame.Surface):
        if self.cell.revealed:
            pygame.draw.rect(surface, (0, 0, 0), (self.x*PIECE_SIZE, self.y*PIECE_SIZE, PIECE_SIZE, PIECE_SIZE), 1)
            pygame.draw.rect(surface, (200, 200, 200), (self.x*PIECE_SIZE+0.1, self.y*PIECE_SIZE+0.1, PIECE_SIZE-0.2, PIECE_SIZE-0.2))
        elif self.cell.flagged:
            pygame.draw.rect(surface, (0, 0, 0), (self.x*PIECE_SIZE, self.y*PIECE_SIZE, PIECE_SIZE, PIECE_SIZE), 1)
            pygame.draw.rect(surface, (222, 222, 222), (self.x*PIECE_SIZE+0.1, self.y*PIECE_SIZE+0.1, PIECE_SIZE-0.2, PIECE_SIZE-0.2))
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
    board.fill((222, 222, 222))
    screen.blit(board, (MARGIN, MARGIN))
    pygame.display.flip()

    show_game(game, board, screen)

    ongoing = True
    while ongoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                yb, xb = pygame.mouse.get_pos()
                x = (xb - MARGIN) // PIECE_SIZE
                y = (yb - MARGIN) // PIECE_SIZE
                pos = Position(x, y)

                if game.board.get_cell(pos).revealed:
                    continue
                if not game.board.get_cell(pos).clear:
                    show_game(game, board, screen)
                    ongoing = False
                # game.game_reveal_cell(pos)
                
                game.game_reveal_adjacents(pos)
                print('left click', x, y)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                yb, xb = pygame.mouse.get_pos()
                x = (xb - MARGIN) // PIECE_SIZE
                y = (yb - MARGIN) // PIECE_SIZE

                game.board.get_cell(Position(x, y)).switch_flag()
                
                print('right click', x, y)

        board.fill((222, 222, 222))

        show_game(game, board, screen)

    print('game overrr')
    print(game.board)
    pygame.quit()

if __name__ == '__main__':
    main()