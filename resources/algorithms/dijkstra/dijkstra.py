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
    def __init__(self):
        self._graph = dict()

    def __str__(self):
        return json.dumps(self._graph, indent=4)

    def get_distance(self, source: str, target: str) -> int:
        """

        :param source:
        :param target:
        :return:
        """
        return self._graph[source][target]

    def set_distance(self, edge: str, distances_to: Dict[str, int]):
        """

        :param edge:
        :param distances_to:
        :return:
        """
        self._graph[edge] = distances_to

    @property
    def edges(self) -> List[str]:
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
    pass


if __name__ == '__main__':
    main()
