#ifndef NETWORKOPERATIONS_ALGORITHMS_H
#define NETWORKOPERATIONS_ALGORITHMS_H

#include "structure/graph.h"


#define     DIJKSTRA    1
#define     A_STAR      2

#define     TRUE        1
#define     FALSE       0


int get_shortest_path(int algorithm, struct graph* graph) ;


#endif //NETWORKOPERATIONS_ALGORITHMS_H
