#include <stdio.h>

#include "logger.h"

/**
 * \fn print_log
 * \brief log an action to the console
 *
 * \param source action's source
 * \param action action to log
 */
void print_log(char *source, char *action)
{
    printf("** [LOG]\t%s\t%s\n", source, action) ;
} /* print_log */
