import sys
from enum import Enum

class Cell(Enum):
    CLEAR = 1
    BOMB = 2

class Board:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.cells = []
        for _ in range(height):
            self.cells.append([Cell.CLEAR] * width)

    def __str__(self) -> str:
        res = ''
        for i in range(self.height):
            for j in range(self.width):
                res += '.' if self.cells[i][j] == Cell.CLEAR else 'x'
            res += '\n'
        return res
    
    def make_bomb(self, row: int, col: int) -> None:
        if row >= self.height or col >= self.width:
            raise Exception(f'cannot update cell at position ({row}, {col})')
        self.cells[row][col] = Cell.BOMB