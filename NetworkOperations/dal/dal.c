#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

