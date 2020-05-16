import copy
import itertools

import pytest

import random_graph


def test_init():
    # check that empty initialisation (and variations of) work
    _ = random_graph.graphs.SwitchSimpleGraph(0, [])
    _ = random_graph.graphs.SwitchSimpleGraph(10, [])

    # check that numbers of nodes are correct
    g = random_graph.graphs.SwitchSimpleGraph(7, [])
    assert g.n == 7
    assert list(g.edges) == []

    # check that invalid edges are rejected
    with pytest.raises(ValueError, match="Provided arguments are not a valid simple graph"):
        random_graph.graphs.SwitchSimpleGraph(10, [{0, 1}, {0, 1}])
    with pytest.raises(ValueError, match="Provided arguments are not a valid simple graph"):
        random_graph.graphs.SwitchSimpleGraph(10, [{99, 0}])

    # check that graphs with edges are correct
    g = random_graph.graphs.SwitchSimpleGraph.from_degree_sequence([2] * 5)
    assert g.n == 5
    assert 2 * len(list(g.edges)) == 2 * 5
    assert g.degree_sequence == (2,) * 5

    # create an asymmetric graph for further testing
    edges = ({1, 2}, {1, 4}, {3, 1}, {2, 3}, {3, 4})
    g = random_graph.graphs.SwitchSimpleGraph(n=5, edges=edges)
    assert g.n == 5
    assert len(list(g.edges)) == len(edges)
    assert all(edge in g.edges for edge in edges)
    assert all(edge not in list(g.edges) for edge in [{0, x} for x in range(5)])
    assert g.degree_sequence == (0, 3, 2, 3, 2)


def test_print():
    g_short = random_graph.graphs.SwitchSimpleGraph(4, ({0, 2}, {0, 1}, {1, 3}, (2, 1)))
    assert str(g_short).startswith("Switch Simple Graph with n=4, degrees=(2, 3, 2, 1)")

    g_complete = random_graph.graphs.SwitchSimpleGraph(20, ({x, y} for x in range(20) for y in range(x + 1, 20)))
    assert str(g_complete).startswith("Switch Simple Graph with n=20")


def test_switch():
    # create a graph that can be mutated
    g = random_graph.graphs.SwitchSimpleGraph.from_degree_sequence((3,) * 10)

    # force one mutation
    edges_start = set(tuple(sorted(edge)) for edge in g.edges)
    g_init = copy.deepcopy(g)
    switched = g.switch()
    while not switched:
        switched = g.switch()
    edges_final = set(tuple(sorted(edge)) for edge in g.edges)
    assert g_init != g

    # check that difference is correct
    assert len(edges_start - edges_final) == 2
    print(edges_start - edges_final)
    print(edges_final - edges_start)
    assert len(edges_final - edges_start) == 2
    vertices_start = {v for e in edges_start - edges_final for v in e}
    vertices_final = {v for e in edges_final - edges_start for v in e}
    assert vertices_start == vertices_final
    assert len(vertices_start) <= 4


def test_from_degree_sequence():
    g = random_graph.graphs.SwitchSimpleGraph.from_degree_sequence([])
    assert g.n == 0
    assert list(g.edges) == []

    d = list(range(1, 6)) + list(range(5, 0, -1))
    graph = random_graph.graphs.SwitchSimpleGraph.from_degree_sequence(d)
    assert isinstance(graph, random_graph.graphs.SwitchSimpleGraph)
    assert graph.degree_sequence == tuple(d)

    with pytest.raises(ValueError, match="Degree sequence is not graphical"):
        random_graph.graphs.SwitchSimpleGraph.from_degree_sequence((10, 2, 2, 2))
