#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include "logic.h"
#include "board.h"

void get_arguments(int argc, char *argv[], int *height, int *width, int *nmines) {
    int opt;
    bool h = false, w = false, m = false;
    while ((opt = getopt(argc, argv, "h:w:m:")) != -1) {
        switch (opt) {
            case 'h':
                *height = atoi(optarg);
                h = true;
                break;
            case 'w':
                *width = atoi(optarg);
                w = true;
                break;
            case 'm':
                *nmines = atoi(optarg);
                m = true;
                break;
            case '?':
                break;
            default:
                fprintf(stderr, "get_arguments: error in getopt\n");
                exit(1);
        }
    }

    if (!h || !w || !m) {
        fprintf(stderr, "usage: play.py -h HEIGHT -w WIDTH -m MINES\n");
        exit(1);
    }
}

int from_char(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    }
    if (c >= 'A' && c <= 'Z') {
        return c - 'A' + 10;
    }
    if (c >= 'a' && c <= 'z') {
        return c - 'a' + 36;
    }
    return -1;
}

int main(int argc, char *argv[]) {
    int height, width, nmines;
    get_arguments(argc, argv, &height, &width, &nmines);

    char c1, c2, c3;
    char cont = 'r';

    game *g;
    position pos;
    cell *c;
    bool lose = false, quit = false;
    while (cont == 'r') {
        g = new_game(height, width, nmines);
        while (!game_check_win(g)) {
            show_game(g);
            scanf("%c%c%c%*c", &c1, &c2, &c3);

            if (c1 == 'q') {
                quit = true;
                break;
            }  
            if (from_char(c2) == -1 || from_char(c3) == -1) {
                printf("invalid position, please try again\n");
                continue;
            }
            pos = new_position(from_char(c2), from_char(c3));
            if (!on_board(g->b, pos)) {
                printf("invalid position, please try again\n");
                continue;
            }
            if (c1 == 'c') {
                c = get_cell(g->b, pos);
                if (!c->clear) {
                    c->detonated = true;
                    lose = true;
                    break;
                }
                game_reveal_adjacents(g, pos);
            } else if (c1 == 'f') {
                game_switch_flag(g, pos);
            }
            fflush(stdin);
        }
        reveal_all_mines(g);
        show_game(g);
        if (quit) {
            printf("quitting game :(\n");
            free_game(g);
            exit(0);
        }
        printf(lose ? "\033[6myou lose...game over...\n" : "\033[5mYOU WIN!!\n");
        printf("\033[0m");
        scanf("%c%*c", &cont);
        free_game(g);
    }
}