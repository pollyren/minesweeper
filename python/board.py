import sys
from enum import Enum
from typing import Union

class Cell:
    def __init__(self, clear: bool=True, value: Union[int, None]=0) -> None:
        self.clear = clear
        self.value = value
    
    def incr_value(self) -> None:
        if not self.clear:
            raise Exception('cannot call incr_value on a non-clear cell')
        self.value += 1

class Position:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

class Board:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]

    def get_cell(self, pos: Position) -> Cell:
        i, j = pos.row, pos.col
        if i >= self.height or j >= self.width:
            raise Exception(f'position ({i}, {j}) is not on the board')
        return self.cells[i][j]
    
    def set_cell(self, pos: Position, cell: Cell) -> None:
        i, j = pos.row, pos.col
        if i >= self.height or j >= self.width:
            raise Exception(f'position ({i}, {j}) is not on the board')
        self.cells[i][j] = cell

    def __str__(self) -> str:
        res = ''
        for i in range(self.height):
            for j in range(self.width):
                current_cell = self.get_cell(Position(i, j))
                res += str(current_cell.value) if current_cell.clear else '*'
            res += '\n'
        return res
    
    def make_mine(self, pos: Position) -> None:
        i, j = pos.row, pos.col
        self.set_cell(Position(i, j), Cell(False, None))

    def on_board(self, pos: Position) -> bool:
        return 0 <= pos.row < self.height and 0 <= pos.col < self.width
    
    def get_adjacents(self, pos: Position) -> list:
        directions = (-1, 0, 1)
        res = []
        for dy in directions:
            for dx in directions:
                if dx == dy == 0: 
                    continue
                new_pos = Position(pos.row+dy, pos.col+dx)
                if not self.on_board(new_pos):
                    continue
                res.append(new_pos)
        return res