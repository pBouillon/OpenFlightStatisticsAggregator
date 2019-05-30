#ifndef NETWORKOPERATIONS_SERVER_H
#define NETWORKOPERATIONS_SERVER_H


/* --- constants --- */

// set socket flags to none
#define     TCP_NO_FLAG         0

// tcp custom errors
#define     TCP_ERROR_ACCEPT    1
#define     TCP_ERROR_BIND      2
#define     TCP_ERROR_SELECT    3
#define     TCP_ERROR_SOCKET    4

// default value for empty socket
#define     SOCKET_NOT_SET      -1


/* --- methods --- */

// start the server
void start_server() ;

#endif //NETWORKOPERATIONS_SERVER_H
