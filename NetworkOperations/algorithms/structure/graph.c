#include <stdio.h>
#include <stdlib.h>

#include "graph.h"


/**
 * \fn create_graph
 * \brief create a new graph with only a head
 *
 * \param head the first node in the graph
 */
struct graph* create_graph(struct node* head)
{
    struct graph* graph = (struct graph*) malloc(sizeof(struct graph)) ;

    head->node_id = 0 ;
    for (int i = 0; i < MAX_CHILREN_CAPACITY; ++i)
    {
        head->children_ids[i] = VALUE_NOT_SET ;
        head->costs[i] = VALUE_NOT_SET ;
        head->heuristique[i] = VALUE_NOT_SET ;
    }

    graph->nodes[0] = head ;
    graph->stored_nodes = 1 ;

    return &graph ;
} /* graph */


/**
 * \fn add_node
 * \brief add a new node to the graph
 *
 * \param child child to append to another node
 * \param father father of the child to add
 * \param cost cost of the edge from father to child
 */
void add_node(struct graph* graph, struct node *child, struct node *father, int cost, int heuristique)
{
    // register the node in the graph
    child->node_id = graph->stored_nodes++ ;
    graph->nodes[graph->stored_nodes] = child ;

    // initialize the child node
    for (int i = 0; i < MAX_CHILREN_CAPACITY; ++i)
    {
        child->children_ids[i] = VALUE_NOT_SET ;
        child->costs[i] = VALUE_NOT_SET ;
        child->heuristique[i] = VALUE_NOT_SET ;
    }

    // link the node to its father
    for (int i = 0; i < MAX_GRAPH_CAPACITY; ++i)
    {
        // if the place is taken, continue the research
        if (father->children_ids[i] != VALUE_NOT_SET)
        {
            continue ;
        }

        // append the child to the other with its cost
        father->children_ids[i] = child->node_id ;
        father->costs[i] = cost ;
        father->heuristique[i] = heuristique ;

        // end the loop
        break ;
    }
} /* add_node */
