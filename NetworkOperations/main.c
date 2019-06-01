#include <stdio.h>
#include <stdlib.h>

#include "server/server.h"
#include "client/client.h"


#define     ARGS_REQUIRED           2
#define     MODE                    1

#define     SERVER_ARGS_EXPECTED    3
#define     SERVER_MODE             1
#define     SERVER_PORT             2

#define     CLIENT_ADDR             2
#define     CLIENT_ARGS_EXPECTED    4
#define     CLIENT_MODE             2
#define     CLIENT_PORT             3
#define     CLIENT_REQ              4


#define     TEXT_INTRO      "*****\n" \
                              "**  - Projet PPII - \n" \
                              "**\n" \
                              "** Auteurs: \n" \
                              "**     BOUILLON Pierre, CESARI Alexandre\n" \
                              "**\n" \
                              "** Url: \n" \
                              "**     https://gitlab.telecomnancy.univ-lorraine.fr/ppii-2k19/project-grpa2\n"\
                              "*****"

/**
 * \fn show_header
 * \brief show program's header
 */
void show_header()
{
    printf("%s\n\n", TEXT_INTRO) ;
} /* show_header */


/**
 * \fn show_help
 * \brief show program's help
 */
void show_help()
{
    printf("usage: ./main mode\n") ;
    printf("mode:\n") ;
    printf("\t- %d: server mode\n", SERVER_MODE) ;
    printf("\t- %d: client mode\n", CLIENT_MODE) ;
    printf("usage per mode:\n") ;
    printf("\tserver: ./main server_port\n") ;
    printf("\tclient: ./main client_addr client_port request\n\n") ;
} /* show_help */


/**
 * program's entry point
 */
int main(int argc, char **argv)
{
    // show header
    show_header() ;

    if (argc < ARGS_REQUIRED)
    {
        show_help() ;
        perror ("at least one mode expected") ;
        return EXIT_FAILURE ;
    }

    switch (atoi(argv[MODE]))
    {
        case CLIENT_MODE:
            if (argc != CLIENT_ARGS_EXPECTED)
            {
                show_help() ;
                perror ("bad arg count") ;
                return EXIT_FAILURE ;
            }
            start_client(
                argv[CLIENT_ADDR], 
                argv[CLIENT_PORT],
                argv[CLIENT_REQ]
            ) ;
            break ;
        
        case SERVER_MODE:
            if (argc != SERVER_ARGS_EXPECTED)
            {
                show_help() ;
                perror ("bad arg count") ;
                return EXIT_FAILURE ;
            }
            start_server(atoi(argv[SERVER_PORT])) ;
            break ;
        
        default:
            show_help() ;
            perror("unknown mode") ;
            return EXIT_FAILURE ;
    }

    return EXIT_SUCCESS ;
}
