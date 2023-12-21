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
        if self.board.get_cell(pos).revealed:
            return
        self.num_revealed += 1
        return self.board.get_cell(pos).reveal_cell()

    def game_reveal_adjacents(self, pos: Position) -> None:
        '''
        Called after the position itself is revealed
        '''
        print('finding adjacents pieces to ', pos)
        tmp = set()
        # tmp.add(pos)
        visited = self.game_reveal_adj_empty(pos, tmp)
        print('visited is now: ', visited)
        for position in visited: # revealing cells that are right adjacent to empty pieces
            self.game_reveal_cell(position)

            for pos_neighbour in self.board.get_adjacents(position):
                if self.board.get_cell(pos_neighbour).revealed_mine_or_flagged():
                    continue
                self.game_reveal_cell(pos_neighbour)

    # def game_reveal_adj_empty(self, pos: Position, visited: set) -> set:
    #     for j, row in enumerate(self.board.cells):
    #         for i, cell in enumerate(row):
    #             print(i, j, cell)
    #     if self.board.get_cell(pos).revealed_mine_or_flagged():
    #         print(f'early return in adjempty because {self.board.get_cell(pos).revealed}')
    #         return visited
    #     print('pos is', pos)
    #     # if pos in visited:
    #     #     return visited
    #     visited.add(pos)
        
    #     # for pos_neighbour in self.board.get_adjacents(pos):
    #     #     print('adjacents for pos', pos_neighbour)
    #     for pos_neighbour in self.board.get_adjacents(pos):
    #         # print('pos_neighbour', pos_neighbour)
    #         for elt in visited:
    #             print("\tcurrently visited is:", end='')
    #             print(elt)
    #         if pos_neighbour not in visited:
    #             print('now visiting ', pos_neighbour)
    #             # visited.add(pos_neighbour)
    #             visited = self.game_reveal_adj_empty(pos_neighbour, visited)
    #         self.game_reveal_cell(pos_neighbour)

            
    #     return visited
    def game_reveal_adj_empty(self, pos: Position, visited: set) -> set:
        if self.board.get_cell(pos).revealed_mine_or_flagged():
            return visited
        if pos in visited:
            return visited
        
        visited.add(pos)
        for pos_neighbour in self.board.get_adjacents(pos):
            if pos_neighbour not in visited:
                self.game_reveal_adj_empty(pos_neighbour, visited)
        return visited