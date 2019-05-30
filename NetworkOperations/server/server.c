#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include "server.h"

/**
 * \fn launch_server
 * \brief starts the server process
 *
 * \param port the port of the server
 */
int start_server(int port)
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

    FD_ZERO(&allset) ;
    FD_ZERO(&read_set) ;
    FD_SET(sockfd, &read_set) ;

    max_sockfd = sockfd + 1 ;
    min_sockfd = -1 ;

    // listening to connections
    for (;;)
    {
        allset = rset ;

        fd_index = select(
            max_sockfd,
            (struct sockaddr *) &cli_addr,
            &clilen
        )
        if (fd_index < 0)
        {
            perror("unable to perform select") ;
            exit(TCP_ERROR_SELECT) ;
        }

        // on connection request
        if (FD_ISSET(sockfd, &allset))
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
                    && FD_ISSET(sock))
                {
                    max_sockfd =  new_sockfd + 1 ;
                    --fd_index ;
                }

                for (i = 0; fd_index > 0 && i < min_sockfd; ++i)
                {
                    client_sock = clients_tab[i] ;

                    if (client_sock >= 0
                        && FD_ISSET(client_sock, &allset))
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