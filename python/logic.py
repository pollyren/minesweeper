#!/usr/bin/env python3
import random
import board

class Game:
    def __init__(self, height: int, width: int, nmines: int) -> None:
        self.board = board.Board(height, width)
        self.mines = []
        self.init_mines(nmines)

    def __str__(self) -> str:
        return self.board.__str__()

    def place_mines(self, n: int) -> None:
        count = 0
        while count < n:
            num = random.randint(0, self.board.height * self.board.width - 1)
            i = num // self.board.width
            j = num % self.board.width
            pos = board.Position(i, j)
            if not self.board.get_cell(pos).clear:
                continue
            self.board.make_mine(board.Position(i, j))
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

g = Game(5, 10, 15)
print(g)