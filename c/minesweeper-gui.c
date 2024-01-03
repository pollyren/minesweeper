#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <string.h>
#include "logic.h"
#include "board.h"
#include <gtk/gtk.h>

// gtk event button constants
int LEFT = 1;
int MIDDLE = 2;
int RIGHT = 3;

typedef struct gtk_game {
    GtkWidget ***widgets;
    game *g;
} gtk_game;

typedef struct button_update_info {
    gtk_game *gg;
    position pos;
} bui;

bui *new_bui(gtk_game *gg, position pos) {
    bui *res = (bui*)malloc(sizeof(bui));
    res->gg = gg;
    res->pos = pos;
    return res;
}

void get_arguments(int argc, char *argv[], int *height, int *width, int *nmines) {
        int opt;
        bool x = false, y = false, m = false;
        while((opt = getopt(argc, argv, "x:y:m:")) != -1) {
                switch(opt) {
                        case 'x':
                                *height = atoi(optarg);
                                x = true;
                                break;
                        case 'y':
                                *width = atoi(optarg);
                                y = true;
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

        if(!x || !y || !m) {
                fprintf(stderr, "usage: ./minesweeper_gui -x HEIGHT -y WIDTH -m MINES\n");
                exit(1);
        }
}

static void print_hello(GtkWidget *widget, gpointer data) {
    g_print("Hello World\n");
}

gtk_game *new_gtk_game(int height, int width, int nmines) {
    gtk_game *res = (gtk_game*)malloc(sizeof(gtk_game));
    res->g = new_game(height, width, nmines);
    res->widgets = (GtkWidget***)malloc(height * sizeof(GtkWidget**));
    for (int i = 0; i < height; i++) {
        res->widgets[i] = (GtkWidget**)malloc(width * sizeof(GtkWidget*));
        for (int j = 0; j < width; j++) {
            res->widgets[i][j] = NULL;
        }
    }
    return res;
}

void free_gtk_game(gtk_game *gg) {
    for (int i = 0; i < gg->g->b->height; i++) {
        free(gg->widgets[i]);
    }
    free(gg->widgets);
    free_game(gg->g);
    free(gg);
}


void button_label_update(gtk_game *gg, position pos) {
    cell *c = get_cell(gg->g->b, pos);
    char *label = (char*)calloc(2, sizeof(char)); // flag or number is 1 character, plus null termination char
    if (c->revealed) {
        snprintf(label, sizeof(char), "%d", c->value);
        gtk_button_set_label(gg->widgets[pos.row][pos.col], label);
    } else if (c->flagged) {
        label[0] = 'F';
        gtk_button_set_label(gg->widgets[pos.row][pos.col], label);
    } 
}

void gtk_game_switch_flag(gtk_game *gg, position pos) {
    game_switch_flag(gg->g, pos);
    button_label_update(gg, pos);
}

int gtk_game_reveal_cell(gtk_game *gg, position pos) {
    int res = game_reveal_cell(gg->g, pos);
    button_label_update(gg, pos);
    return res;
}

void gtk_game_reveal_adjacents(gtk_game *gg, position pos) {
    game_reveal_adjacents(gg->g, pos);
    
}

bool gtk_game_check_win(gtk_game *gg) {
    return game_check_win(gg->g);
}

void button_update(GtkWidget *widget, GdkEventButton *event, gpointer data) {
    bui *tmp = (bui*)data;
    gtk_game *gg = tmp->gg;
    game *g = gg->g;
    position pos = tmp->pos;
    if (event->type == GDK_BUTTON_PRESS) {
        if (event->button == LEFT) {
            g_print("Hello World from the left\n");
            if (get_cell(g->b, pos)->revealed) return;
            if (!get_cell(g->b, pos)->clear) {
                print('you lose...game over...');
            } else {
                gtk_game_reveal_adjacents(gg, pos);
            }
        } else if (event->button == RIGHT) {
            g_print("Hello World from the right\n");
        }
    }
}

static void activate(GtkApplication* app, gpointer user_data) {
    GtkWidget *window;
    GtkWidget *grid;
    GtkWidget *button;

    bui *tmp;
    gtk_game *gg = (gtk_game*)user_data;
    int height = gg->g->b->height, width = gg->g->b->width, nmines = gg->g->nmines;

    window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "minesweeper");
    gtk_container_set_border_width(GTK_CONTAINER(window), 10);

    grid = gtk_grid_new();
    gtk_container_add(GTK_CONTAINER(window), grid);

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            tmp = new_bui(gg, new_position(i, j)); // TODO: deal with freeing these
            gg->widgets[i][j] = gtk_button_new();
            g_signal_connect(GTK_BUTTON(gg->widgets[i][j]), "button-press-event", G_CALLBACK(button_update), tmp);
            gtk_grid_attach(GTK_GRID(grid), gg->widgets[i][j], j, i, 1, 1);
        }
    }

    button = gtk_button_new_with_label("quit");
    g_signal_connect_swapped(button, "clicked", G_CALLBACK(gtk_widget_destroy), window);
    gtk_grid_attach(GTK_GRID(grid), button, 0, height, width, 1);

    gtk_widget_show_all(window);
}

int main(int argc, char* argv[]) {
    GtkApplication* app;
    int status;

    int height = 10, width = 15, nmines = 20;

    gtk_game *gg = new_gtk_game(height, width, nmines);

    app = gtk_application_new("minesweeper.gtk", G_APPLICATION_FLAGS_NONE);
    g_signal_connect(app, "activate", G_CALLBACK(activate), gg);
    status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);

    free_gtk_game(gg);
    return status;
}