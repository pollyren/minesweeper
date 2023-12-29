#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include "logic.h"
#include "board.h"
#include <gtk/gtk.h>

typedef struct gtk_game {
    GtkWidget ***widgets;
    game *g;
} gtk_game;

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

static void
print_hello(GtkWidget *widget,
             gpointer   data)
{
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

static void activate(GtkApplication* app, gpointer user_data) {
    GtkWidget *window;
    GtkWidget *grid;
    GtkWidget *button;
    gtk_game *gg = (gtk_game*)user_data;
    int height = gg->g->b->height, width = gg->g->b->width, nmines = gg->g->nmines;

    window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "minesweeper");
    gtk_container_set_border_width(GTK_CONTAINER(window), 10);

    grid = gtk_grid_new();
    gtk_container_add(GTK_CONTAINER(window), grid);

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            gg->widgets[i][j] = gtk_button_new();
            g_signal_connect(gg->widgets[i][j], "clicked", G_CALLBACK(print_hello), NULL);
            gtk_grid_attach(GTK_GRID(grid), gg->widgets[i][j], j, i, 1, 1);
        }
    }

    button = gtk_button_new_with_label("Quit");
    g_signal_connect_swapped(button, "clicked", G_CALLBACK(gtk_widget_destroy), window);
    gtk_grid_attach(GTK_GRID(grid), button, 0, height, width, 1);

    gtk_widget_show_all(window);
}

int main(int argc, char* argv[]) {
    GtkApplication* app = gtk_application_new("minesweeper.gtk", G_APPLICATION_FLAGS_NONE);
    int status;

    int height = 10, width = 15, nmines = 20;

    gtk_game *gg = new_gtk_game(height, width, nmines);

    g_signal_connect(app, "activate", G_CALLBACK(activate), gg);
    status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);

    free_gtk_game(gg);
    return status;
}