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
int dijkstra(struct graph* graph)
{
    int explored_nodes[graph->stored_nodes] ;
    int open_set[graph->stored_nodes] ;

    // TODO: weight list

    // initializing the open set to all nodes
    for (int i = 0; i < sizeof(open_set); ++i)
    {
        open_set[i] = graph->nodes[i]->node_id ;
        explored_nodes[i] = FALSE ;
    }

    while (is_node_non_explored(explored_nodes))
    {
        // todo final implementation
    }

    return 0 ;
} /* dijkstra */


/**
 *
 */
int get_shortest_path(int algorithm, struct graph* graph)
{
    switch (algorithm)
    {
        case DIJKSTRA:
            dijkstra(graph) ;
            break ;

        case A_STAR:
            break ;

        default:
            return 1 ;
    }
} /* get_shortest_path */


/**
 *
 */
int is_node_non_explored(int *nodes_status)
{
    while (nodes_status)
    {
        if (*nodes_status == TRUE) {
            return TRUE ;
        }
        ++nodes_status ;
    }
    return FALSE ;
} /* is_node_non_explored */
