#include "dijkstra.h"
#include "../algorithms.h"
#include "../structure/graph.h"


/**
 *
 */
int a_star()
{
    return 0 ;
} /* a_star */


/**
 *
 */
int dijkstra()
{
    return 0 ;
} /* dijkstra */


/**
 *
 */
int get_shortest_path(int algorithm)
{
    switch (algorithm)
    {
        case DIJKSTRA:
            dijkstra() ;
            break ;

        case A_STAR:
            break ;

        default:
            return 1 ;
    }
}
