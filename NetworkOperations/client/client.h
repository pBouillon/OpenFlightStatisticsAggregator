#ifndef NETWORKOPERATIONS_CLIENT_H
#define NETWORKOPERATIONS_CLIENT_H

/* --- constants  --- */
#define     RESPONSE_BUFFER_LEN     32768

/* --- methods --- */
// start the client
void start_client(char *server_addr, char *server_port, char *intent);

#endif //NETWORKOPERATIONS_CLIENT_H
