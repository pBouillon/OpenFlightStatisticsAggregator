#include <stddef.h>
#include "a_star.h"
#include "../algorithms.h"
#include "../structure/graph.h"

typedef struct s_List List;
struct s_List
{
    List *next ;
    void *data ;
} ;

List *
list_create(void *data)
{
    List *list = malloc(sizeof(list)) ;
    if(list)
    {
        list->data = data ;
        list->next = NULL ;
    }
    return list ;
}

List *
list_append_open_nodes(List *list ,void *data)
{
    List **plist = &list ;
    while (*plist)
        plist = &(*plist)->next ;
    *plist = list_create(data) ;
    if (*plist)
        return list ;
    else
        return NULL ;
}

void a_star(struct graph* graph, char *source, char *target)
{
    List *open_nodes = NULL ;
    List *list_close = NULL ;

    open_nodes = list_create(*source) ;




}