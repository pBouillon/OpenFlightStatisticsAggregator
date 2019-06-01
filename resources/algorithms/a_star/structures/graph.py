import json
from typing import List, Dict

from resources.algorithms.a_star.structures.edge import Edge


class Graph:
    """
    """

    def __init__(self):
        self._graph = dict()

    def __str__(self) -> str:
        render = ''
        for edge in self._graph:
            render += f'{edge.name} ->'
            for neighbor, weight in self._graph[edge].items():
                render += f' [{neighbor.name}: {weight}]'
            render += '\n'
        return render

    def get_children(self, edge: Edge) -> List[Edge]:
        """
        """
        return list(self._graph[edge].keys())

    def get_distance(self, source: Edge, target: Edge) -> int:
        """
        """
        return self._graph[source][target]

    def set_distance(self, edge: Edge, distance_to: Dict[Edge, int]):
        """
        """
        self._graph[edge] = distance_to
    
    @property
    def edges(self) -> List[Edge]:
        """
        """
        return list(self._graph.keys())
