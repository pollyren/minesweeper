#include "logic.h"
#include <time.h> 

void init_mines(game *g, int nmines) {
    srand(time(NULL));
    int height = g->b->height, width = g->b->width;
    int count = 0, size = height * width - 1, num, i, j;
    position pos;
    pos_ll *adjacents, *tmp;
    cell *c;
    while (count < nmines) {
        num = rand() % size;
        i = num / width;
        j = num % width;
        pos = new_position(i, j);
        if (!get_cell(g->b, pos)->clear) continue;
        make_mine(g->b, pos);
        tmp = adjacents = get_adjacents(g->b, pos);
        while (tmp) {
            c = get_cell(g->b, tmp->curr);
            if (c->clear) incr_cell_value(c);
            tmp = tmp->next;
        }
        free_posll(adjacents);
        count++;
    }
}

game *new_game(int height, int width, int nmines) {
    game *res = (game*)malloc(sizeof(game));
    res->b = new_board(height, width);
    res->nmines = nmines;
    init_mines(res, nmines);
    res->num_revealed = 0;
    res->clicks = 0;
    return res;
}

void print_line(int width) {
    printf("\n    -");
    for (int j = 0; j < width; j++) {
        printf("----");
    }
    printf("\n");
}

char to_char(unsigned int num) {
    if (num < 10) {
        return num + '0';
    } 
    if (num < 36) {
        return num - 10 + 'A';
    } 
    if (num < 62) {
        return num - 36 + 'a';
    } 
    return '?';
}

void print_columns(int width) {
    printf("\n\033[34m     ");
    for (int i = 0; i < width; i++) {
        printf(" %c  ", to_char(i));
    }
    printf("\033[0m");
}

void show_game(game *g) {
    board *b = g->b;
    position pos;
    cell *c;

    print_columns(b->width);
    print_line(b->width);
    for (int i = 0; i < b->height; i++) {
        printf("\033[34m%c   \033[0m| ", to_char(i));
        for (int j = 0; j < b->width; j++) {
            pos = new_position(i, j);
            c = get_cell(b, pos);
            if (c->detonated) {
                printf("\033[1;41m*");
                printf("\033[0m");
            } else if (c->revealed) {
                if (c->clear) {
                    printf("\033[2m%c", c->value+'0');
                    printf("\033[0m");
                } else {
                    printf("\033[31m*");
                    printf("\033[0m");
                }
            } else if (c->flagged) {
                printf("\033[32mF");
                printf("\033[0m");
            } else {
                printf(".");
            }
            printf(" | ");
        }
        print_line(b->width);
    }
}

void free_game(game *g) {
    free_board(g->b);
    free(g);
}

void game_switch_flag(game *g, position pos) {
    cell *c = get_cell(g->b, pos);
    c->flagged = !c->flagged;
}

int game_reveal_cell(game *g, position pos) {
    cell *c = get_cell(g->b, pos);
    if (c->revealed || c->flagged) return -1;
    g->num_revealed++;
    return reveal_cell(c);
}

bool **new_search_matrix(int height, int width) {
    bool **res = (bool**)malloc(height * sizeof(bool*));
    for (int i = 0; i < height; i++) {
        res[i] = (bool*)calloc(width, sizeof(bool));
    }
    return res;
}

void free_search_matrix(bool **m, int height) {
    for (int i = 0; i < height; i++) {
        free(m[i]);
    }
    free(m);
}

bool **reveal_adj_empty(game *g, position pos, bool **searched) {
    if (nonzero_mine_or_flagged(get_cell(g->b, pos))) return searched;

    pos_ll *adjacents = get_adjacents(g->b, pos);
    pos_ll *tmp = adjacents;

    cell *c;
    position pos_neighbour;
    while (tmp) {
        pos_neighbour = tmp->curr;
        c = get_cell(g->b, pos_neighbour);
        if (!searched[pos_neighbour.row][pos_neighbour.col]) {
            searched[pos_neighbour.row][pos_neighbour.col] = true;
            searched = reveal_adj_empty(g, pos_neighbour, searched);
        }
        if (!c->revealed) game_reveal_cell(g, pos_neighbour);
        tmp = tmp->next;
    }
    free_posll(adjacents);
    return searched;
}

void game_reveal_adjacents(game *g, position pos) {
    bool **searched = new_search_matrix(g->b->height, g->b->width);
    game_reveal_cell(g, pos);
    reveal_adj_empty(g, pos, searched);
    free_search_matrix(searched, g->b->height);
    g->clicks++;
}

bool game_check_win(game *g) {
    return g->num_revealed == g->b->height * g->b->width - g->nmines;
}

void reveal_all_mines(game *g) {
    position pos;
    for (int i = 0; i < g->b->height; i++) {
        for (int j = 0; j < g->b->width; j++) {
            pos = new_position(i, j);
            if (!get_cell(g->b, pos)->clear) game_reveal_cell(g, pos);
        }
    }
}