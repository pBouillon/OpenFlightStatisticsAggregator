#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include "server.h"
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


/**
 * \fn process_query
 * \brief extract and execute user's intent
 * 
 * \param sockfd dialog socket
 */
void process_query(int sockfd)
{
    // user intent and query payload
    int intent ;
    char **payload ;

    // parse the request -> strtok
    // TODO

    switch (intent) 
    {
        case INTENT_FETCH:
            // performed on 'table/column/nb'
            // TODO
            break ;
        
        case INTENT_PATH:
            // performs on 'flight/duration="shortest",&dest="____"'
            // TODO
            break ;
        
        default:
            perror("unable to process the user intent") ;
            exit(SERVER_UNKNOWN_REQ) ; // FIXME: close sockets and connection on exit
    }
} /* extract_query */


/**
 * \fn launch_server
 * \brief starts the server process
 *
 * \param port the port of the server
 */
void start_server(int port)
{
    /* --- initialisation --- */

    // sockets
    int sockfd, new_sockfd, client_sock ;

    // return code, used for error detection, counter
    int rc, i ;

    int nb_fd ;

    // TODO
    int fd_index ;

    // TODO
    int max_sockfd, min_sockfd ;

    // TODO
    socklen_t clilen ;

    struct sockaddr_in cli_addr ;
    struct sockaddr_in serv_addr ;

    // contains the associated sockfd for each associated client
    int clients_tab[FD_SETSIZE] ;

    // contains all descriptors
    fd_set all_set ;
    // contains read only event 
    fd_set read_set ;

    /* --- server creation --- */
    // create the server's socket
    sockfd = socket(
        AF_INET,
        SOCK_STREAM,
        TCP_NO_FLAG
    ) ;

    if (sockfd < 0) 
    {
        perror("unable to create the server's socket") ;
        exit(TCP_ERROR_SOCKET) ;
    }

    // initialize the server structure
    memset(
        (char*) &serv_addr,
        0,
        sizeof(serv_addr)
    ) ;
    // using IPv4
    serv_addr.sin_family = AF_INET ; // using IPv4
    // addr does not matter for the server
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY) ; 
    // using default port
    serv_addr.sin_port = port ;

    // binding the socket and the server structure
    rc = bind (
        sockfd,
        (struct sockaddr *) &serv_addr,
        sizeof(serv_addr)
    ) ;

    if (rc < 0)
    {
        perror ("unable to bind the socket to the server") ;
        exit(TCP_ERROR_BIND) ;
    }

    // initializing stored socket fd
    for (i = 0; i < FD_SETSIZE; ++i)
    {
        clients_tab[i] = SOCKET_NOT_SET ;
    }

    FD_ZERO(&all_set) ;
    FD_ZERO(&read_set) ;
    FD_SET(sockfd, &read_set) ;

    max_sockfd = sockfd + 1 ;
    min_sockfd = -1 ;

    // listening to connections
    for (;;)
    {
        all_set = read_set ;

        fd_index = select(
            max_sockfd,
            &all_set,
            NULL,
            NULL,
            NULL
        ) ;
        if (fd_index < 0)
        {
            perror("unable to perform select") ;
            exit(TCP_ERROR_SELECT) ;
        }

        // on connection request
        if (FD_ISSET(sockfd, &all_set))
        {
            clilen = sizeof(cli_addr) ;
            new_sockfd = accept(
                sockfd,
                (struct sockaddr *) &cli_addr,
                &clilen
            ) ;

            if (new_sockfd < 0)
            {
                perror("unable to accept the incomming connection") ;
                exit(TCP_ERROR_ACCEPT) ;
            }

            // add the client to the known clients
            for (i = 0; i < FD_SETSIZE && clients_tab[i] >= 0; ++i) { } ;
            
            if (i == FD_SETSIZE)
            {
                perror("too many clients") ;
                exit(TCP_ERROR_ACCEPT) ;
            }

            clients_tab[i] = new_sockfd ;
            FD_SET (new_sockfd, &read_set) ;

            if (i > min_sockfd) {
                min_sockfd = i ;
            }
            
            if (new_sockfd >= max_sockfd)
            {
                max_sockfd =  new_sockfd + 1 ;
                --fd_index ;
            }

            for (i = 0; fd_index > 0 && i < min_sockfd; ++i)
            {
                client_sock = clients_tab[i] ;

                if (client_sock >= 0
                    && FD_ISSET(client_sock, &all_set))
                {
                    max_sockfd =  new_sockfd + 1 ;
                    --fd_index ;
                }

                for (i = 0; fd_index > 0 && i < min_sockfd; ++i)
                {
                    client_sock = clients_tab[i] ;

                    if (client_sock >= 0
                        && FD_ISSET(client_sock, &all_set))
                    {
                        // TODO: handle connection using `client_sock`

                        close(client_sock) ;
                        clients_tab[i] = SOCKET_NOT_SET ;
                        FD_CLR(client_sock, &read_set) ;

                        --fd_index ;
                    }
                }
            }
        }
    }
}
