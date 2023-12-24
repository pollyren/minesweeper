#!/usr/bin/env python3
import random
from board import *
from typing import Union

class Game:
    def __init__(self, height: int, width: int, nmines: int) -> None:
        self.board = Board(height, width)
        self.nmines = nmines
        self.init_mines(nmines)
        self.num_revealed = 0
        self.clicks = 0

    def __str__(self) -> str:
        return self.board.__str__()

    def get_board(self) -> Board:
        return self.board
    
    def get_clicks(self) -> int:
        return self.clicks
    
    def init_mines(self, n: int) -> None:
        count = 0
        while count < n:
            num = random.randint(0, self.board.get_height() * self.board.get_width() - 1)
            i, j = divmod(num, self.board.get_width())
            pos = Position(i, j)
            if not self.board.get_cell(pos).is_clear():
                continue
            self.board.make_mine(Position(i, j))
            for adj_cell in self.board.get_adjacents(pos):
                if self.board.get_cell(adj_cell).is_clear():
                    self.board.get_cell(adj_cell).incr_value()
            count += 1

    def game_reveal_cell(self, pos: Position) -> Union[int, None]:
        # print(f'call to game_reveal_cell {pos}')
        if self.board.get_cell(pos).is_revealed() or self.board.get_cell(pos).is_flagged():
            return
        if self.board.get_cell(pos).is_clear():
            self.num_revealed += 1
        return self.board.get_cell(pos).reveal_cell()

    def game_reveal_adjacents(self, pos: Position) -> None:
        searched = set()
        self.game_reveal_cell(pos)
        self.game_reveal_adj_empty(pos, searched)
        self.clicks += 1

    def game_reveal_adj_empty(self, pos: Position, searched: set) -> set:
        if self.board.get_cell(pos).zero_mine_or_flagged():
            return searched

        for pos_neighbour in self.board.get_adjacents(pos):
            cell = self.board.get_cell(pos_neighbour)
            if cell not in searched:
                searched.add(cell)
                searched = self.game_reveal_adj_empty(pos_neighbour, searched)
            if not cell.is_revealed():
                self.game_reveal_cell(pos_neighbour)
        return searched
        
    def check_win(self) -> bool:
        return self.num_revealed == self.board.get_height()*self.board.get_width()-self.nmines
    
    def reveal_all_mines(self) -> None:
        for i in range(self.board.get_height()):
            for j in range(self.board.get_width()):
                pos = Position(i, j)
                if not self.board.get_cell(pos).is_clear():
                    self.game_reveal_cell(pos)