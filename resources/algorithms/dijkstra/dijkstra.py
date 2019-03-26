# -*- coding: utf-8 -*-
"""
    dijkstra
    --------

    Dijkstra shortest path implementation.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
import json
from typing import Dict, List


class Graph:
    """References Graph

    Minimal implementation of a graph
    """

    DISPLAY_INDENT = 2

    def __init__(self):
        self._graph = dict()

    def __str__(self):
        return json.dumps(self._graph, indent=self.DISPLAY_INDENT)

    def get_distance(self, source: str, target: str) -> int:
        """Get the distance from `source` to `target`

        :raise KeyError: on a non-existing edge

        :param source: source edge
        :param target: target edge
        :return: the distance between them as an int
        """
        return self._graph[source][target]

    def set_distance(self, edge: str, distances_to: Dict[str, int]):
        """Add a distance from `edge` to all edges as keys in `distance_to`

        :param edge: source
        :param distances_to: dict as {target: distance_to_target]
        """
        self._graph[edge] = distances_to

    @property
    def edges(self) -> List[str]:
        """Get all edges

        :return: list of edges
        """
        return list(self._graph.keys())


def get_default_graph() -> Graph:
    """Generate a basic graph to work with

    Representation:

              ____ A ___
          3 /      |     \ 3
           /       |      \
       s =         | 1      = t
           \       |      /
          6 \ ____ B ___ / 2


    :return: the generated graph
    """
    graph = Graph()
    graph.set_distance('s', {'A': 3, 'B': 6})
    graph.set_distance('A', {'B': 1, 't': 3})
    graph.set_distance('B', {'t': 2})
    graph.set_distance('t', {})
    return graph


def main():
    graph = get_default_graph()
    print(graph)
    print(
        f'distance from `s` to `A`: '
        f'{graph.get_distance(source="s", target="A")}'
    )


if __name__ == '__main__':
    main()
