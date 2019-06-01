#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "server.h"
#include "../dal/dal.h"
#include "../log/logger.h"
#include "../tcp/tcp_errors.h"

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
    char msg[USER_MSG_LEN] ;
    char *payload[USER_SEGMENT_LEN] ;
    char rcv_buff[DB_MAX_ROW][DB_MAX_ROW_LEN] ;

    // read the user request
    intent = read(sockfd, msg, USER_MSG_LEN - 1) ;

    if (intent < 0)
    {
        perror("unable to retrieve user message") ;
        exit(TCP_ERROR_READ) ;
    }

    // parse the request
    if (strstr(msg, "GET ") == NULL)
    {
        perror("malformated request") ;
        exit(TCP_ERROR_READ) ;
    }

    // récupérer juste la partie interessante de la requete: "GET la/requete" -> "la/requete"
    int i;
    char *request;
    for (i = 3; i <= strlen(msg); i++)
    {
        request[i-3] = msg[i];
    }

    // faire le traitement de chaque partie de la requete
    // pour chaque partie entre /
    // mettre la partie dans payload
    // exemple: airport/city
    // donne: payloed = ["airport", "city"]
    char *tocken = strtok(request, "/") ;
    i = 0;
    while(tocken)
    {
        payload[i] = tocken ;
        tocken = strtok(NULL , "/") ;
        i++ ;
    }

    // TODO
    // selon la requete, assigner une valeur à intent
    // si table/... alors intent = INTENT_FETCH
    // si flight/duration/etc...= INTENT_PATH
    if (strstr(payload[0], "airport") != NULL)
    {
        intent = INTENT_RETRIEVE_AIRPORT ;
        if (strstr(payload[1], "=") == NULL)
        {
            perror("malformated request") ;
            exit(TCP_ERROR_READ) ;
        }
        int j = 0 ;
        for (i = (strstr(payload[1], "=") + 1); i <= (strlen(payload[1]) - 1); i++)
        {
            payload[1][j] = payload[1][i] ;
            j++ ;
        }
    }
    else if (strstr(payload[0], "flight") != NULL)
    {
        intent = INTENT_PATH ;
    }
    else
    {
        intent = INTENT_FETCH ;
    }

    // process the request
    switch (intent) 
    {
        case INTENT_FETCH:
            // performed on 'table/column/nb'
            fetch(rcv_buff, payload[0], payload[1], atoi(payload[2])) ;
            break ;
        
        case INTENT_PATH:
            // performs on 'flight/duration="shortest",&dest="____"'
            // TODO: dijkstra / a*
            break ;
        case INTENT_RETRIEVE_AIRPORT:
            retrieve_airport(rcv_buff, payload[1]) ;

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

    // TODO: doc
    int fd_index ;

    // TODO: doc
    int max_sockfd, min_sockfd ;

    // TODO: doc
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

    print_log("server", "socket created") ;

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

    print_log("server", "socket server binded") ;

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
    print_log("server", "started polling") ;
    if (listen(sockfd, SOMAXCONN) < 0)
    {
        perror("unable to perform listen") ;
        exit(TCP_ERROR_LISTEN) ;
    }

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
                perror("unable to accept the incoming connection") ;
                exit(TCP_ERROR_ACCEPT) ;
            }

            // add the client to the known clients
            i = 0 ;
            while(i < FD_SETSIZE  && clients_tab[i] >= 0){
                i++ ;
            }
            
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

            for (i = 0; fd_index > 0 && i < min_sockfd; i++)
            {
                client_sock = clients_tab[i] ;

                if (client_sock >= 0
                    && FD_ISSET(client_sock, &all_set))
                {
                    max_sockfd =  new_sockfd + 1 ;
                    --fd_index ;
                }

                for (i = 0; fd_index > 0 && i < min_sockfd; i++)
                {
                    client_sock = clients_tab[i] ;

                    if (client_sock >= 0
                        && FD_ISSET(client_sock, &all_set))
                    {
                        print_log("server", "communication received") ;

                        // handle client request
                        process_query(sockfd) ;

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
