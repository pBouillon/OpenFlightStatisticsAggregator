from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Edge:
    name: str
    x: float
    y: float
    heuristic: float = float('inf')
    weight: float = float('inf')
