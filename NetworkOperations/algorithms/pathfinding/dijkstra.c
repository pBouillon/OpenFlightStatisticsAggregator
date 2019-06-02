#include <math.h>
#include "dijkstra.h"
#include "../algorithms.h"
#include "../structure/graph.h"


/**
 * \fn dijkstra
 * \brief get the shortest path and its cost from `source` to `dest`
 *
 * \param path_ids buffer to store the shortest path (reversed)
 * \param graph graph to work on
 * \param source starting node
 * \param dest destination node
 *
 * \return the total cost from `source` to `dest`
 */
int dijkstra(
        int* path_ids,
        struct graph* graph,
        struct node* source,
        struct node* dest
)
{
    int cpt = 0 ;
    int total_cost = 0 ;
    int total_nodes = graph->stored_nodes ;
    int ancestor_id[total_nodes] ;
    int is_node_explored[total_nodes] ;
    int cost_from_source[total_nodes] ;
    int open_set[total_nodes] ;

    int current_node ;
    int new_distance ;
    int* child_node ;

    // if there is no need to run the algorithm, return 0
    if (source->node_id == dest->node_id)
    {
        return total_cost ;
    }

    // initializing the open set to all nodes and cost to inf
    for (int i = 0; i < sizeof(open_set); ++i)
    {
        open_set[i] = graph->nodes[i]->node_id ;
        cost_from_source[i] = INFINITY ;
        is_node_explored[i] = FALSE ;
        ancestor_id[i] = i ;
    }
    cost_from_source[source->node_id] = 0 ;

    while (is_node_non_explored(is_node_explored))
    {
        current_node = INFINITY ;
        for (int i = 0; i < total_nodes; ++i)
        {
            // looking for the smallest distance
            if (cost_from_source[i] < current_node)
            {
                // pick the node if he isn't explored
                if (is_node_explored[i] == FALSE)
                {
                    current_node = i ;
                }
            }

            // remove this node to explore
            is_node_explored[i] = TRUE ;

            // update costs for all connected nodes
            child_node = graph->nodes[i]->children_ids ;
            while (child_node)
            {
                new_distance =
                        cost_from_source[current_node]
                        + get_cost(graph, current_node, *child_node) ;

                if (new_distance < cost_from_source[*child_node])
                {
                    cost_from_source[*child_node] = new_distance ;
                    ancestor_id[*child_node] = current_node ;
                }

                ++child_node ;
            }
        }
    }

    // create path
    current_node = dest->node_id ;
    while (current_node != source->node_id)
    {
        path_ids[cpt++] = current_node ;
        current_node = ancestor_id[current_node] ;
    }

    return total_cost ;
} /* dijkstra */


/**
 * \fn get_cost
 * \brief get the cost from a node to another
 *
 * \param g graph in which perform the search
 * \param from_id id of the source node
 * \param to id of the target node
 * \return the cost between `from_id` and `to_id` if exists
 *         else -1 (VALUE_NOT_SET)
 */
int get_cost(struct graph* g, int from_id, int to_id)
{
    int cost = VALUE_NOT_SET ;
    int total_nodes = g->stored_nodes ;

    // if these nodes are not in range, return an error
    if (from_id >= total_nodes
        || to_id >= total_nodes)
    {
        return cost ;
    }

    // looking for the destination
    struct node* from_node = g->nodes[from_id] ;
    for (int i = 0; i < sizeof(from_node->children_ids); ++i)
    {
        // if this children is not the one we are looking for, continue
        if (from_node->children_ids[i] != to_id)
        {
            continue ;
        }

        // on the correct child, get its cost
        cost = from_node->costs[i] ;

        // exit the search
        break ;
    }

    return cost ;
} /* get_cost */


/**
 * \fn is_node_non_explored
 * \brief evaluate if there is any non-explored node
 *
 * \return 1 (TRUE) if it remains at least one node non-explored;
 *         0 (FALSE) otherwise
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
