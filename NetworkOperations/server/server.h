#ifndef NETWORKOPERATIONS_SERVER_H
#define NETWORKOPERATIONS_SERVER_H


/* --- constants --- */

// user intents
#define     INTENT_FETCH        1
#define     INTENT_PATH         2

// server custom errors
#define     SERVER_UNKNOWN_REQ  1

// default value for empty socket
#define     SOCKET_NOT_SET      -1

// max message length
#define     USER_MSG_LEN        256
#define     USER_SEGMENT_LEN    128

/* --- methods --- */
// extract and process user's intent
void process_query(int sockfd) ;

// start the server
void start_server(int port) ;

#endif //NETWORKOPERATIONS_SERVER_H
