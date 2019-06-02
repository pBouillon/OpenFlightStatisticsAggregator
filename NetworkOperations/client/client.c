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
#include <netdb.h>

/* custom imports */
#include "client.h"
#include "../log/logger.h"
#include "../tcp/tcp_errors.h"


/**
 * \fn launch_client
 * \brief starts the client process
 * 
 * \param server_addr address of the server to reach
 * \param server_port port of the server to reach
 * \param intent query to send to the server
 */
void start_client(char *server_addr, char *server_port, char *intent)
{
    // server structure
    struct sockaddr_in serv_in ;
    // server IP on 32 bits
    struct in_addr serv_addr ;

    struct hostent *hp ;
    // communication utility
    socklen_t addrlen ;
    char response_buffer[RESPONSE_BUFFER_LEN] ;

    // socket descriptor
    int sockfd ;

    // store return codes
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

    print_log("client", "socket created") ;

    // initialize structure
    memset(
        &serv_in,
        0,
        sizeof(struct sockaddr_in)
    ) ;

    serv_in.sin_family = AF_INET ;
    serv_in.sin_port = htons(atoi(server_port)) ;

    hp = gethostbyname(server_addr) ;
    if (hp == NULL)
    {
        perror("invalid IP address") ;
        exit (TCP_ERROR_INET_ATON) ;
    }
    serv_in.sin_addr = *((struct in_addr *)(hp->h_addr)) ;

    print_log("client", "initializing server's information") ;

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

    print_log("client", "connected to the server") ;

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

    print_log("client", "data sent to the server") ;

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

    print_log("client", "response received") ;

    // TODO: handle response

    // close the communication
    close(sockfd) ;
} /* start_client */
