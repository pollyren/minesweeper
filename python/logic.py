#!/usr/bin/env python3
import random
from board import *
from typing import Union

class Game:
    def __init__(self, height: int, width: int, nmines: int) -> None:
        self.board = Board(height, width)
        self.mines = []
        self.init_mines(nmines)
        self.num_revealed = 0
        self.clicks = 0

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

    def game_reveal_cell(self, pos: Position) -> Union[int, None]:
        print(f'call to game_reveal_cell {pos}')
        if self.board.get_cell(pos).revealed or self.board.get_cell(pos).flagged:
            return
        self.num_revealed += 1
        return self.board.get_cell(pos).reveal_cell()

    def game_reveal_adjacents(self, pos: Position) -> None:
        searched = set()
        searched_pos = set()
        self.game_reveal_cell(pos)
        searched_pos, _ = self.game_reveal_adj_empty(pos, searched, searched_pos)
        # for pos in searched_pos:
        #     for pos_neighbour in self.board.get_adjacents(pos):
        #         if self.board.get_cell(pos_neighbour).zero_mine_or_flagged():
        #             continue
        #         self.game_reveal_cell(pos_neighbour)
        self.clicks += 1

    def game_reveal_adj_empty(self, pos: Position, searched: set, searched_pos: set) -> set:
        if self.board.get_cell(pos).zero_mine_or_flagged():
            return searched_pos, searched

        for pos_neighbour in self.board.get_adjacents(pos):
            cell = self.board.get_cell(pos_neighbour)
            if cell not in searched:
                searched.add(cell)
                searched_pos.add(pos_neighbour)
                searched_pos, searched = self.game_reveal_adj_empty(pos_neighbour, searched, searched_pos)

            if not cell.revealed:
                self.game_reveal_cell(pos_neighbour)

        return searched_pos, searched
        
    def check_win(self) -> bool:
        return self.num_revealed == self.board.height*self.board.width-len(self.mines)
    
    def reveal_all_mines(self) -> None:
        for i in range(self.board.height):
            for j in range(self.board.width):
                pos = Position(i, j)
                if self.board.get_cell(pos).flagged:
                    self.board.get_cell(pos).switch_flag()
                if not self.board.get_cell(pos).clear:
                    self.game_reveal_cell(pos)