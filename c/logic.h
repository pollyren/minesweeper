#ifndef LOGIC_H
#define LOGIC_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "board.h"

typedef struct {
    board *b;
    int nmines, num_revealed, clicks;
} game;

game *new_game(int height, int width, int nmines);

void show_game(game *g);

void free_game(game *g);

void game_switch_flag(game *g, position pos);

int game_reveal_cell(game *g, position pos);

void game_reveal_adjacents(game *g, position pos);

bool **new_search_matrix(int height, int width);

void free_search_matrix(bool **m, int height);

bool **game_reveal_adj_empty(game *g, position pos, bool **searched);

bool game_check_win(game *g);

void reveal_all_mines(game *g);

#endif