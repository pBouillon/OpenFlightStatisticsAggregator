#ifndef NETWORKOPERATIONS_DIJKSTRA_H
#define NETWORKOPERATIONS_DIJKSTRA_H

#include "../structure/graph.h"

int a_star() ;
int dijkstra(struct graph* graph) ;
int get_shortest_path(int algorithm, struct graph* graph) ;
int is_node_non_explored(int *nodes_status) ;

#endif //NETWORKOPERATIONS_DIJKSTRA_H
