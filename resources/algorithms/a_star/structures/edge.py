from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Edge:
    name: str
    x: int
    y: int
    heuristic: float = float('inf')
    weight: float = float('inf')
