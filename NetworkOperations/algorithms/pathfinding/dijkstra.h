#ifndef NETWORKOPERATIONS_DIJKSTRA_H
#define NETWORKOPERATIONS_DIJKSTRA_H

#include "../structure/graph.h"

int a_star() ;

int dijkstra(
    int* path_ids,
    struct graph* graph,
    struct node* source,
    struct node* dest
) ;

int get_cost(struct graph* g, int from_id, int to_id) ;

int is_node_non_explored(int *nodes_status) ;

#endif //NETWORKOPERATIONS_DIJKSTRA_H
