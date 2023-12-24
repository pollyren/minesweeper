#ifndef BOARD_H
#define BOARD_H

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

typedef struct {
    int row, col;
} position;

position new_position(int row, int col);

typedef struct pos_ll pos_ll;
struct pos_ll {
    position curr;
    pos_ll *next;
};

typedef struct {
    int value;
    bool clear, revealed, flagged, detonated;
} cell;

cell new_cell(int value, bool clear, bool revealed, bool flagged);

void incr_cell_value(cell *c);

int reveal_cell(cell *c);

void switch_cell_flag(cell *c);

bool zero_mine_or_flagged(cell *c);


typedef struct {
    int height, width;
    cell **cells;
} board;

board *new_board(int height, int width);

void free_board(board *b);

cell *get_cell(board* b, position pos);

cell **get_row(board* b, int i);

void set_cell(board *b, position pos, cell c);

void make_mine(board *b, position pos);

bool on_board(board *b, position pos);

pos_ll *get_adjacents(board *b, position pos);

void free_posll(pos_ll *head);

void show_board(board *b);

#endif