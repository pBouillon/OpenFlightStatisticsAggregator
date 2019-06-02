#ifndef NETWORKOPERATIONS_DAL_H
#define NETWORKOPERATIONS_DAL_H

#include <sqlite3.h>

/* --- constants --- */
// custom errors
#define     DB_ERROR_CONENCT    1
#define     DB_ERROR_REQUEST    2

// sqlite default database path
#define     DB_PATH             "../DatabaseNormalizer/static/sql/sql_dump/ppii.db"
#define     DB_MAX_ROW          2500
#define     DB_MAX_ROW_LEN      1024
#define     MAX_GRAPH_CAPACITY  1024

/* --- methods --- */
// fetch some rows of a specefic column in a table
void fetch(char **rcv_buff, char *table, char *column, int limit) ;
void retrieve_airport (char **rcv_buff, char *restriction) ;
struct graph* add_child(
        int father,
        double father_lat,
        double father_long,
        struct graph* graph,
        int *liste_node[MAX_GRAPH_CAPACITY],
        int j
) ;
void shortest_path(char **rcv_buff, char *source, char *destination) ;

#endif //NETWORKOPERATIONS_DAL_H
