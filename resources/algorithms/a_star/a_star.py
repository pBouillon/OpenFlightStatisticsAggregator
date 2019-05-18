from resources.algorithms.a_star.structures.edge import Edge
from resources.algorithms.a_star.structures.graph import Graph


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


if __name__ == '__main__':
    build_graph()
