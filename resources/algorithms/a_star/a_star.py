from resources.algorithms.a_star.structures.edge import Edge
from resources.algorithms.a_star.structures.graph import Graph

from typing import List


def build_graph():
    """
        3
    A ----> t
    ^       ^
  5 |       | 1
    s ----> B
        6

    """
    s = Edge(name='s', x=0, y=0)
    a = Edge(name='A', x=0, y=1)
    b = Edge(name='B', x=1, y=0)
    t = Edge(name='t', x=1, y=1)

    g = Graph()
    g.set_distance(s, {
        a: 5,
        b: 6
    })
    g.set_distance(a, {
        t: 3
    })
    g.set_distance(b, {
        t: 1
    })
    g.set_distance(t, {})
    print(g)
    return g


def astar(graph: Graph, source: str, target: str) -> List[str]:
    """Find the shortest path between `source` and `target`

    :param graph: the graph to work on
    :param source: the source node
    :param target: the target node
    :return: a list of the edges from the `source` to the `target` resulting in
             the shortest path
    """

    for edge in graph.edges:
        if source == edge.name:
            start = edge
        if target == edge.name:
            goal = edge

    # Initialize both open and closed nodes
    open_nodes = []
    close_nodes = []

    # Initially, only the start node is known
    open_nodes.append(start)

    # cameFrom will contain the most efficient previous step.
    ancestor = {edge: 0 for edge in graph.edges}

    # For each node, the cost of getting from the start node to that node
    g_cost = {edge: float('inf') for edge in graph.edges}
    # The cost of going from start to start is zero
    g_cost[start] = 0

    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic
    f_cost = {edge: float('inf') for edge in graph.edges}
    #  For the first node, that value is completely heuristic
    f_cost[source] = heuristic_cost_estimate(start, goal)

    while open_nodes:
        # looking at the node with the smallest distance
        current_node = min(open_nodes, key=f_cost.get)

        if current_node == goal:
            return reconstruct_path(ancestor, current_node)

        # Remove current node off open list, add to closed list
        open_nodes.remove(current_node)
        close_nodes.append(current_node)

        # for each child of the selected node
        for child in graph.get_children(current_node):
            if child in close_nodes:
                continue

            tentatice_g_cost = g_cost[current_node] + graph.get_distance(current_node, child)
            if child not in open_nodes:
                open_nodes.append(child)
            elif tentatice_g_cost >= g_cost[child]:
                continue

            ancestor[child] = current_node
            g_cost[child] = tentatice_g_cost
            f_cost[child] = g_cost[child] + heuristic_cost_estimate(child, goal)


def heuristic_cost_estimate(node, target):

    return abs(target.x - node.x) + abs(target.y - node.y)


def reconstruct_path(ancestor, node):
    total_path = [node.name]
    while node in ancestor.keys():
        node = ancestor[node]
        if node != 0:
            total_path.append(node.name)
    return total_path[::-1]






def main():
    graph = build_graph()
    shortest_path = astar(graph, 's', 't')

    print(f'working with the structures:\n\t{graph}')
    print(f'shortest path:\n\t{shortest_path}')


if __name__ == '__main__':
    main()
