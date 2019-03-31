# -*- coding: utf-8 -*-
"""
    dijkstra
    --------

    Dijkstra shortest path implementation.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from typing import List

from algorithms.utils.graph import Graph


def get_default_graph() -> Graph:
    """Generate a basic graph to work with

    Representation:

              ____ A ___
          3 /      |     \ 4
           /       |      \
       s =         | 1      = t
           \       |      /
          6 \ ____ B ___ / 2


    :return: the generated graph
    """
    graph = Graph()
    graph.set_distance('s', {'A': 3, 'B': 6})
    graph.set_distance('A', {'B': 1, 't': 4})
    graph.set_distance('B', {'t': 2})
    graph.set_distance('t', {})
    return graph


def astar(graph: Graph, source: str, target: str) -> List[str]:
    """Find the shortest path between `source` and `target`

    :param graph: the graph to work on
    :param source: the source node
    :param target: the target node
    :return: a list of the edges from the `source` to the `target` resulting in
             the shortest path
    """
    # if their is no searches to do
    if source == target:
        return [source]

    # initializing all distances to inf and the start to 0
    distance = {edge: float('inf') for edge in graph.edges}
    distance[source] = 0

    # keeping track of the ancestors
    ancestor = {edge: edge for edge in graph.edges}

    # nodes to parse
    open_nodes = graph.edges[:]

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(source)

    # while we can search through the nodes
    while open_nodes:
        # Get the current node
        current_node = open_list[0]
        current_index = 0

        for index, item in enumerate(open_list):
            if distance[item] < distance[current_node]:
                current_node = item
                current_index = index

        # Remove current node off open list, add to closed list
        open_list.remove(current_node)
        closed_list.append(current_node)

        # for each child of the selected node
        for child in graph.get_children(current_node):

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue


    # rebuilding the path
    path = []
    current_node = target

    # from the end, rebuilding the path to the source
    while current_node != source:
        path.append(current_node)
        current_node = ancestor[current_node]

    # add the source as final destination, then reverse the path
    return [*path, source][::-1]


def main():
    graph = get_default_graph()
    shortest_path = astar(graph, 's', 't')

    print(f'working with the graph:\n\t{graph}')
    print(f'shortest path:\n\t{shortest_path}')


if __name__ == '__main__':
    main()
