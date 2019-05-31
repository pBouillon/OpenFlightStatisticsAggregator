#ifndef NETWORKOPERATIONS_DAL_H
#define NETWORKOPERATIONS_DAL_H

#include <sqlite3.h>

/* --- constants --- */
// custom errors
#define     DB_ERROR_CONENCT    1
#define     DB_ERROR_REQUEST    2

// sqlite default database path
#define     DB_PATH             "./"
#define     DB_MAX_ROW          2500
#define     DB_MAX_ROW_LEN      1024

/* --- methods --- */
// connect to the database
sqlite3 *connect();

// fetch some rows of a specefic column in a table
char **fetch(char *table, char *column, int limit) ;

#endif //NETWORKOPERATIONS_DAL_H
