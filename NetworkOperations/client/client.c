/* sockaddr, sockaddr_in, etc. */
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>

/* close */
#include <unistd.h>

/* perror et printf */
#include <errno.h>
#include <stdio.h>

/* memset */
#include <string.h>

/* EXIT constants */
#include <stdlib.h>

/* custom imports */
#include "client.h"
#include "../tcp/tcp_errors.h"

/**
 * \fn launch_client
 * \brief starts the client process
 */
void start_client(char *server_addr, char *server_port, char *intent)
{
    // server structure
    struct sockaddr_in serv_in ;
    // server IP on 32 bits
    struct in_addr serv_addr ;

    socklen_t addrlen ;

    char response_buffer[RESPONSE_BUFFER_LEN] ;

    int sockfd ;
    int rc ;

    // create socket
    sockfd = socket(
        AF_INET,
        SOCK_STREAM,
        TCP_NO_FLAG
    ) ;

    if (sockfd < 0)
    {
        perror("unable to create the socket") ;
        exit(TCP_ERROR_SOCKET) ;
    }

    // initialize structure
    memset(
        &serv_in,
        0,
        sizeof(struct sockaddr_in)
    ) ;

    serv_in.sin_family = AF_INET ;
    serv_in.port = htons(atoi(server_port)) ;

    rc = inet_aton(server_addr, &serv_addr) ;
    if (rc < 0)
    {
        perror("invalid IP address") ;
        exit (TCP_ERROR_INET_ATON) ;
    }
    serv_in.sin_addr = serv_addr ;

    // connection
    addrlen = sizeof(serv_in) ;
    rc = connect(
        sockfd,
        (struct sockaddr *) &serv_in,
        addrlen
    ) ;

    if (rc < 0)
    {
        perror("unable to reach the server") ;
        exit(TCP_ERROR_CONNECT) ;
    }

    // send the query
    rc = write(
        sockfd,
        intent,
        strlen(intent) + 1
    ) ;

    if (rc < 0)
    {
        perror("unable to send the intent to the server") ;
        exit(TCP_ERROR_WRITE) ;
    }

    // receive server's response
    rc = read(
        sockfd,
        response_buffer,
        RESPONSE_BUFFER_LEN
    ) ;

    if (rc < 0)
    {
        perror("unable to retrieve response from the server") ;
        exit(TCP_ERROR_READ) ;
    }

    // TODO: handle response

    close(sockfd) ;
} /* start_client */
