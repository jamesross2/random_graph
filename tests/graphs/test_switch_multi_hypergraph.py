import copy
import itertools

import pytest

import random_graph


def test_init():
    # check that empty initialisation (and variations of) work
    _ = random_graph.graphs.SwitchMultiHypergraph(0, [])
    _ = random_graph.graphs.SwitchMultiHypergraph(10, [])

    # check that numbers of nodes are correct
    g = random_graph.graphs.SwitchMultiHypergraph(7, [])
    assert g.n == 7
    assert g.m == 0

    g = random_graph.graphs.SwitchMultiHypergraph(9, [{i, i + 1, i + 2} for i in range(7)])
    assert g.n == 9
    assert g.m == 7

    g = random_graph.graphs.SwitchMultiHypergraph(5, [{1, 2, 3}] * 7)
    assert g.n == 5
    assert g.m == 7

    # check that invalid edges are rejected
    with pytest.raises(ValueError, match="Provided arguments are not a valid multi-hypergraph"):
        assert not random_graph.graphs.SwitchMultiHypergraph(5, [{10, 11}])
    with pytest.raises(ValueError, match="Provided arguments are not a valid multi-hypergraph"):
        assert not random_graph.graphs.SwitchMultiHypergraph(10, [(1, 1, 1)])

    # create an asymmetric graph for further testing
    edges = ({1, 2, 3}, {1, 2, 3, 4}, {2, 3, 4}, {3, 4})
    g = random_graph.graphs.SwitchMultiHypergraph(n=5, edges=edges)
    assert g.n == 5
    assert g.m == 4
    assert len(list(g.edges)) == len(edges)
    assert all(tuple(edge in list(g.edges) for edge in edges))
    assert g.degree_sequence == (0, 2, 3, 4, 3)
    assert g.edge_sizes == (3, 4, 3, 2)


def test_switching():
    g1 = random_graph.graphs.SwitchMultiHypergraph(5, ({i, (i + 1) % 5} for i in range(5)))
    g2 = copy.deepcopy(g1)
    assert g1 == g2
    switched = g2.switch()
    while not switched:
        switched = g2.switch()
    assert g1 != g2


def test_simple():
    g_simple = random_graph.graphs.SwitchMultiHypergraph(5, ({i, (i + 1) % 5} for i in range(5)))
    assert g_simple.simple()

    g_nonsimple = random_graph.graphs.SwitchMultiHypergraph(5, tuple({i, (i + 1) % 5} for i in range(5)) + ({1, 2},))
    assert not g_nonsimple.simple()


def test_print():
    g_short = random_graph.graphs.SwitchMultiHypergraph(3, ({0, 1, 2}, {0, 2}))
    assert str(g_short).startswith("Switch Multi-Hypergraph with n=3, degrees=(2, 1, 2), edge sizes=(3, 2)")

    g_complete = random_graph.graphs.SwitchMultiHypergraph(20, ({x, y} for x in range(20) for y in range(x)))
    degrees = ", ".join(str(n) for n in [19] * 9) + ", ..."
    edge_sizes = ", ".join(str(n) for n in [2] * 9) + ", ..."
    assert str(g_complete).startswith(
        f"Switch Multi-Hypergraph with n=20, degrees=({degrees}), edge sizes=({edge_sizes})"
    )


def test_neighbourhoods():
    # build a hypergraph with clear neighbourhoods
    n, d, r = 10, 6, 3
    m = (n * d) // r
    edges = [set((x + i) % n for i in range(r)) for x in range(n)]
    g = random_graph.graphs.SwitchMultiHypergraph(n, edges)

    assert g.n == n
    assert g.m == n
    assert len(list(g.edges)) == n  # one edge rooted from each vertex
    assert len(list(g.edge_sizes)) == n

    assert all(len(edge) == r for edge in g.edges)
    assert all(edge in g.edges for edge in ({0, 1, 2}, {2, 3, 4}, {4, 5, 6}))
    assert set(range(12, 2)) not in g.edges


def test_switch():
    # create a graph that can be mutated
    g = random_graph.graphs.SwitchMultiHypergraph.from_degree_sequence((5,) * 9, (3,) * 15)

    # force one mutation
    edges_start = sorted(sorted(edge) for edge in g.edges)
    switched = g.switch()
    while not switched:
        switched = g.switch()
    edges_final = sorted(sorted(edge) for edge in g.edges)

    # check that difference is correct
    assert sum(edge_start != edge_final for edge_start, edge_final in zip(edges_start, edges_final)) == 2


def test_from_degree_sequence():
    dx = list(range(1, 6)) + list(range(5, 0, -1))
    dy = [3] * 5 + [2] * 5 + [1] * 5
    graph = random_graph.graphs.SwitchMultiHypergraph.from_degree_sequence(dx, dy)
    assert isinstance(graph, random_graph.graphs.SwitchMultiHypergraph)
    assert graph.degree_sequence == tuple(dx)
    assert graph.edge_sizes == tuple(dy)

    with pytest.raises(ValueError, match="Degree sequence is not graphical"):
        random_graph.graphs.SwitchMultiHypergraph.from_degree_sequence(
            dx, dy * 2
        )  # check that graphs with edges are correct
