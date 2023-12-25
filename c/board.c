#include "board.h"

position new_position(int row, int col) {
    position new;
    new.row = row;
    new.col = col;
    return new;
}

cell new_cell(int value, bool clear, bool revealed, bool flagged) {
    cell new;
    new.value = value;
    new.clear = clear;
    new.revealed = revealed;
    new.flagged = flagged;
    new.detonated = false;
    return new;
}

void incr_cell_value(cell *c) {
    c->value++;
}

int reveal_cell(cell *c) {
    c->revealed = true;
    return c->clear ? 0 : 1;
}

void switch_cell_flag(cell *c) {
    c->flagged = !c->flagged;
}

bool nonzero_mine_or_flagged(cell *c) {
    return !c->clear || c->value || c->flagged;
}

board *new_board(int height, int width) {
    board *b = (board*)malloc(sizeof(board));
    b->height = height;
    b->width = width;
    cell **matrix = (cell**)malloc(height * sizeof(cell*));
    for (int i = 0; i < height; i++) {
        matrix[i] = (cell*)malloc(width * sizeof(cell));
        for (int j = 0; j < width; j++) {
            matrix[i][j] = new_cell(0, true, false, false);
        }
    }
    b->cells = matrix;
    return b;
}

void free_board(board *b) {
    for (int i = 0; i < b->height; i++) {
        free(b->cells[i]);
    }
    free(b);
}

cell *get_cell(board *b, position pos) {
    return &b->cells[pos.row][pos.col];
}

cell **get_row(board *b, int i) {
    return &b->cells[i];
}

void set_cell(board *b, position pos, cell c) {
    cell *tmp = get_cell(b, pos);
    tmp->value = c.value;
    tmp->clear = c.clear;
    tmp->flagged = c.flagged;
    tmp->revealed = c.revealed;
    tmp->detonated = c.detonated;
}

void make_mine(board *b, position pos) {
    cell mine = {-1, false, false, false, false};
    set_cell(b, pos, mine);
}

bool on_board(board *b, position pos) {
    return 0 <= pos.row && pos.row < b->height && 0 <= pos.col && pos.col < b->width;
}

pos_ll *prepend(position to_prepend, pos_ll *head) {
    pos_ll *res = (pos_ll*)malloc(sizeof(pos_ll));
    res->curr = to_prepend;
    res->next = head;
    return res;
}

pos_ll *get_adjacents(board *b, position pos) {
    int directions[] = {-1, 0, 1};
    pos_ll *res = NULL;
    position new_pos;
    int dx, dy;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            dx = directions[i], dy = directions[j];
            if (dx == dy && dy == 0) continue;
            new_pos = new_position(pos.row + dy, pos.col + dx);
            if (!on_board(b, new_pos)) continue;
            res = prepend(new_pos, res);
        }
    }
    return res;
}

void free_posll(pos_ll *head) {
    pos_ll *tmp;
    while (tmp = head) {
        head = head->next;
        free(tmp);
    }
}

void show_board(board *b) {
    position pos;
    cell *current_cell;
    for (int i = 0; i < b->height; i++) {
        for (int j = 0; j < b->width; j++) {
            pos = new_position(i, j);
            current_cell = get_cell(b, pos);
            printf("%c", current_cell->clear ? current_cell->value+'0' : '*');
        }
        printf("\n");
    }
}
