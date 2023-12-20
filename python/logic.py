#!/usr/bin/env python3
import random
from board import Board, Position, Cell

class Game:
    def __init__(self, height: int, width: int, nmines: int) -> None:
        self.board = Board(height, width)
        self.mines = []
        self.init_mines(nmines)
        self.num_revealed = 0

    def __str__(self) -> str:
        return self.board.__str__()

    def place_mines(self, n: int) -> None:
        count = 0
        while count < n:
            num = random.randint(0, self.board.height * self.board.width - 1)
            i, j = divmod(num, self.board.width)
            pos = Position(i, j)
            if not self.board.get_cell(pos).clear:
                continue
            self.board.make_mine(Position(i, j))
            self.mines.append(pos)
            count += 1

    def update_mine_values(self) -> None:
        for mine_pos in self.mines:
            for adj_cell in self.board.get_adjacents(mine_pos):
                if self.board.get_cell(adj_cell).clear:
                    self.board.get_cell(adj_cell).incr_value()

    def init_mines(self, n: int) -> None:
        self.place_mines(n)
        self.update_mine_values()

    def reveal_adjacents(self, pos: Position):
        to_check = list(filter(Cell.revealed_or_mine, map(self.board.get_cell, self.board.get_adjacents(pos))))
        while len(to_check):
            check_pos = to_check.pop()
            self.board.get_cell(check_pos).reveal_cell()
            next_check = list(filter(Cell.revealed_or_mine, map(self.board.get_cell, self.board.get_adjacents(check_pos))))
            to_check.extend(next_check)