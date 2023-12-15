import random
from typing import List
import board

class DisplayCell:
    def __init__(self, cell: board.Cell, value: int=0) -> None:
        self.cell = cell
        self.value = value

class Game:
    def __init__(self, height: int, width: int, nbombs: int) -> None:
        self.board = board.Board(height, width)
        self.nbombs = nbombs

    def __str__(self):
        pass

    def place_bombs(self, n: int) -> None:
        placed = []
        while len(placed) < n:
            r = random.randint(0, self.board.height-1)
            c = random.randint(0, self.board.width-1)
            if (r,c) in placed:
                continue
            self.board.make_bomb(r, c)
            placed.append((r, c))
