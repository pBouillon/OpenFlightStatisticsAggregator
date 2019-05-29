#include <stdio.h>
#include <stdlib.h>


#define     ARGS_REQUIRED   2
#define     MODE            2
#define     SERVER_MODE     1
#define     CLIENT_MODE     2

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
    printf("%s\n", TEXT_INTRO) ;
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
} /* show_help */


/**
 * program's entry point
 */
int main(int argc, char **argv)
{
    // show header
    show_header() ;

    // check args
    if (argc !=  ARGS_REQUIRED)
    {
        show_help() ;
        perror("bad arg number\n") ;
        return EXIT_FAILURE ;
    }

    // acting depending on the provided mode
    switch (atoi(argv[MODE])) // NOLINT(cert-err34-c)
    {
        case CLIENT_MODE:
            // TODO: pass the
            break;
        case SERVER_MODE:
            break;
        default:
            show_help() ;
            perror("unknown mode") ;
            return EXIT_FAILURE ;
    }

    return EXIT_SUCCESS ;
}
