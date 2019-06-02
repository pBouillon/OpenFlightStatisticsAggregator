#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../algorithms/structure/graph.c"
#include "../algorithms/pathfinding/dijkstra.c"
#include <math.h>

#include "dal.h"


/**
 * \fn fetch
 * \brief fetch some rows of a specefic column in a table
 * 
 * \param rcv_buff buffer to store the results
 * \param table table to query
 * \param column column to fetch
 * \param limit number of row to fetch
 */
void fetch(char **rcv_buff, char *table, char *column, int limit)
{
    int rc ;
    sqlite3 *db ;
    char *err_msg = 0 ;
    char *sql_request ;
    sqlite3_stmt *stmt ;

    // checking request validity
    if (limit > DB_MAX_ROW)
    {
        perror("bad request") ;
        exit(DB_ERROR_REQUEST) ;
    }

    // checking buffer size
    rc = sizeof(rcv_buff) / sizeof(rcv_buff[0]) ;
    if (rc > DB_MAX_ROW)
    {
        perror("bad buffer provided") ;
        exit(DB_ERROR_REQUEST) ;
    }

    // reach the database
    rc = sqlite3_open(DB_PATH, &db) ;

    if (rc != SQLITE_OK)
    {
        perror("unable to reach the database") ;
        exit(DB_ERROR_CONENCT) ;
    }

    // prepare the request
    sql_request = "select ?1 from ?2;" ;
    sqlite3_prepare_v2(db, sql_request, -1, &stmt, NULL) ;
    sqlite3_bind_text(stmt, 1, column, -1, SQLITE_STATIC) ;
    sqlite3_bind_text(stmt, 2, table, -1, SQLITE_STATIC) ;

    // perform the request
    for (int i = 0; sqlite3_step(stmt) == SQLITE_ROW && i < limit; ++i)
    {
        // copy line result in the return buffer
        sprintf(
            rcv_buff[i],
            "%s",
            sqlite3_column_text(stmt, 0)
        ) ;
    }

    // close the connection
    sqlite3_finalize(stmt) ;
    sqlite3_free(err_msg) ;
    sqlite3_close(db) ;
} /* fetch */

/**
 * TODO: doc
 */
void retrieve_airport(char **rcv_buff, char *restriction)
{
    int rc ;
    sqlite3 *db ;
    char *err_msg = 0 ;
    char *sql_request ;
    sqlite3_stmt *stmt ;

    // checking buffer size
    rc = sizeof(rcv_buff) / sizeof(rcv_buff[0]) ;
    if (rc > DB_MAX_ROW)
    {
        perror("bad buffer provided") ;
        exit(DB_ERROR_REQUEST) ;
    }

    // reach the database
    rc = sqlite3_open(DB_PATH, &db) ;

    if (rc != SQLITE_OK)
    {
        perror("unable to reach the database") ;
        exit(DB_ERROR_CONENCT) ;
    }

    // prepare the request
    sql_request = "select a.name from airport a, country c where a.id_country = c.id AND country = '?1';" ;
    sqlite3_prepare_v2(db, sql_request, -1, &stmt, NULL) ;
    sqlite3_bind_text(stmt, 1, restriction, -1, SQLITE_STATIC) ;

    // perform the request
    for (int i = 0; sqlite3_step(stmt) == SQLITE_ROW; ++i)
    {
        // copy line result in the return buffer
        sprintf(
                rcv_buff[i],
                "%s",
                sqlite3_column_text(stmt, 0)
        ) ;
    }

    // close the connection
    sqlite3_finalize(stmt) ;
    sqlite3_free(err_msg) ;
    sqlite3_close(db) ;
} /* fetch */

struct graph* add_child(
        int father,
        double father_lat,
        double father_long,
        struct graph* graph,
        int *liste_node[MAX_GRAPH_CAPACITY],
        int j
)
{
    sqlite3 *db ;
    char *err_msg = 0 ;
    char *sql_request ;
    sqlite3_stmt *stmt ;
    char **id_airport, **lat_airport, **long_airport ;
    double cost ;
    struct node* child ;

    int i = 0 ;
    while (i <= MAX_GRAPH_CAPACITY && liste_node[i] != NULL)
    {
        if(father == liste_node[i])
        {
            return graph ;
        }
        // prepare the request
        sql_request = "select ap.id, ap.latitude, ap.longitude from airport ap, airway aw, step_in s where s.id_airport = ap.id and s.id_airway = aw.id and (aw.id, s.rank) in (select aw.id, s.rank + 1 from airport ap, step_in s, airway aw where s.id_airport = ap.id and s.id_airway = aw.id and ap.id = '?1');" ;
        sqlite3_prepare_v2(db, sql_request, -1, &stmt, NULL) ;
        sqlite3_bind_text(stmt, 1, father, -1, SQLITE_STATIC) ;

        if(sqlite3_step(stmt) != 1)
        {
            perror("bad source") ;
            exit(DB_ERROR_CONENCT) ;
        }

        // copy line result in the return buffer
        for (int i = 0; sqlite3_step(stmt) == SQLITE_ROW; ++i)
        {
            // copy line result in the return buffer
            sprintf(
                    id_airport[i],
                    "%s",
                    sqlite3_column_text(stmt, 0)
            ) ;
            sprintf(
                    lat_airport[i],
                    "%s",
                    sqlite3_column_text(stmt, 1)
            ) ;
            sprintf(
                    long_airport[i],
                    "%s",
                    sqlite3_column_text(stmt, 2)
            ) ;
            cost = acos(cos(father_lat * M_PI / 180) * cos(atof(lat_airport[i]) * M_PI / 180) * cos((atof(long_airport[i]) * M_PI / 180) - (father_long * M_PI / 180)) + sin(father_lat * M_PI / 180) * sin(atof(lat_airport[i]) * M_PI / 180)) * 6371 ;
            child->node_id = atoi(id_airport[i]) ;
            liste_node[j] = atoi(id_airport[i]) ;
            add_node(graph, &child, &father, cost) ;
            add_child(atoi(id_airport[i]), atof(lat_airport[i]), atof(long_airport[i]), graph, &liste_node, j+1) ;
        }

        // close the connection
        sqlite3_finalize(stmt) ;
        sqlite3_free(err_msg) ;
    }




}

void shortest_path(char **rcv_buff, char *source, char *destination)
{
    int rc, node[MAX_GRAPH_CAPACITY] ;
    sqlite3 *db ;
    char *err_msg = 0 ;
    char *sql_request ;
    sqlite3_stmt *stmt ;
    struct graph* graph ;
    struct node *src, *dest ;



    rc = sizeof(rcv_buff) / sizeof(rcv_buff[0]) ;
    if (rc > DB_MAX_ROW)
    {
        perror("bad buffer provided") ;
        exit(DB_ERROR_REQUEST) ;
    }

    // reach the database
    rc = sqlite3_open(DB_PATH, &db) ;

    if (rc != SQLITE_OK)
    {
        perror("unable to reach the database") ;
        exit(DB_ERROR_CONENCT) ;
    }

    // prepare the request
    sql_request = "select a.id, a.latitude, a.longitude from airport a where a.name = '?1';" ;
    sqlite3_prepare_v2(db, sql_request, -1, &stmt, NULL) ;
    sqlite3_bind_text(stmt, 1, source, -1, SQLITE_STATIC) ;

    if(sqlite3_step(stmt) != 1)
    {
        perror("bad source") ;
        exit(DB_ERROR_CONENCT) ;
    }

    // copy line result in the return buffer
    sprintf(
            rcv_buff[0],
            "%s",
            sqlite3_column_text(stmt, 0)
    ) ;
    sprintf(
            rcv_buff[1],
            "%s",
            sqlite3_column_text(stmt, 1)
    ) ;
    sprintf(
            rcv_buff[2],
            "%s",
            sqlite3_column_text(stmt, 2)
    ) ;

    // close the connection
    sqlite3_finalize(stmt) ;
    sqlite3_free(err_msg) ;
    src->node_id = atoi(rcv_buff[0]);

    graph = create_graph(src) ;
    node[0] = atoi(rcv_buff[0]) ;
    add_child(atoi(rcv_buff[0]), atof(rcv_buff[1]), atof(rcv_buff[2]), graph, &node, 1) ;

    // prepare the request
    sql_request = "select a.id from airport a where a.name = '?1';" ;
    sqlite3_prepare_v2(db, sql_request, -1, &stmt, NULL) ;
    sqlite3_bind_text(stmt, 1, destination, -1, SQLITE_STATIC) ;

    if(sqlite3_step(stmt) != 1)
    {
        perror("bad source") ;
        exit(DB_ERROR_CONENCT) ;
    }

    // copy line result in the return buffer
    sprintf(
            rcv_buff[0],
            "%s",
            sqlite3_column_text(stmt, 0)
    ) ;

    // close the connection
    sqlite3_finalize(stmt) ;
    sqlite3_free(err_msg) ;
    dest->node_id = atoi(rcv_buff[0]);

    dijkstra(NULL, graph, src, dest) ;

    sqlite3_close(db) ;



}
