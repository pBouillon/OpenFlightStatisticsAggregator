#include <sqlite3.h>

#include "dal.h"

/**
 * \fn connect
 * \brief connect to the sqlite database
 *
 * \return 0 on success
 */
sqlite3 *connect()
{
    int rc ;
    sqlite3 *db ;
    char *zErrMsg = 0 ;

    rc = sqlite3_open(DB_PATH, &db) ;

    if (rc)
    {
        perror("unable to reach the database") ;
        exit(DB_ERROR_CONENCT) ;
    }

    return db ;
} /* connect */

/**
 * \fn fetch
 * \brief fetch some rows of a specefic column in a table
 * 
 * \param table table to query
 * \column column column we are looking for
 * \limit number of records to return
 * 
 * \return TODO
 */
char **fetch(char *table, char *column, int limit)
{
    char results[DB_MAX_ROW][DB_MAX_ROW_LEN] ;

    if (limit > DB_MAX_ROW)
    {
        perror("malformatted request") ;
        exit(DB_ERROR_REQUEST) ;
    }

    // reach the database
    sqlite3 *db = connect() ;

    // TODO: perform query
    // see: http://www.tutorialspoint.com/sqlite/sqlite_c_cpp.htm

    // close the connection
    sqlite3_close(db) ;

    return results;
} /* fetch */
