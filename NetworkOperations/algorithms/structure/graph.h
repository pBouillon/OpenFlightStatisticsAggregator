#ifndef NETWORKOPERATIONS_GRAPH_H
#define NETWORKOPERATIONS_GRAPH_H

#define     MAX_GRAPH_CAPACITY      1024
#define     MAX_CHILREN_CAPACITY    64

#define     VALUE_NOT_SET           -1


/**
 * \struct graph
 * \tparam head graph's first node
 */
struct graph {
    int stored_nodes ;
    struct node* nodes[MAX_GRAPH_CAPACITY] ;
} ;


/**
 * \struct node
 * \tparam node_id id of the current node
 * \tparam name name of the node
 * \tparam costs array of costs from this node
 * \tparam array of node's children
 */
struct node {
    int node_id ;
    char *name ;
    int costs[MAX_CHILREN_CAPACITY] ;
    int children_ids[MAX_CHILREN_CAPACITY] ;
} ;


#endif //NETWORKOPERATIONS_GRAPH_H
