import copy

import pytest

import random_graph


def test_init():
    # check that empty initialisation (and variations of) work
    _ = random_graph.SwitchBipartiteGraph([], [], [])
    _ = random_graph.SwitchBipartiteGraph(10, [], [])
    _ = random_graph.SwitchBipartiteGraph([], 15, [])
    _ = random_graph.SwitchBipartiteGraph(17, 19, [])

    # check that graphs work with integers or chosen vertices
    size = 10
    edges = [(x, y) for x in range(size) for y in range(size) if abs(x - y) < 2 or size - abs(x - y) < 2]
    g1 = random_graph.SwitchBipartiteGraph(size, size, edges)
    g2 = random_graph.SwitchBipartiteGraph(list(range(size)), list(range(size)), edges)
    assert g1 == g2

    # check that numbers of nodes are correct
    g = random_graph.SwitchBipartiteGraph(7, 9, [])
    assert len(g.nodes["x"]) == 7
    assert len(g.nodes["y"]) == 9
    g = random_graph.SwitchBipartiteGraph(list(range(5, 15)), list(range(13, 17)), [])
    assert len(g.nodes["x"]) == 10
    assert len(g.nodes["y"]) == 4

    # check that invalid edges are rejected
    with pytest.raises(ValueError, match="Not all edges are unique."):
        random_graph.SwitchBipartiteGraph(10, 10, [(0, 0), (0, 0)])
    with pytest.raises(ValueError, match="does not appear in nodes"):
        random_graph.SwitchBipartiteGraph(10, 10, [(99, 0)])


def test_simple():
    g_simple = random_graph.SwitchBipartiteGraph(5, 5, ((x, x) for x in range(5)))
    assert g_simple.simple

    g_nonsimple = random_graph.SwitchBipartiteGraph(5, 5, ((0, 0), (0, 1)))
    assert not g_nonsimple.simple


def test_neighbourhoods():
    # build a hypergraph with clear neighbourhoods
    n, d, r = 10, 6, 3
    xs = list(range(n))
    ys = list(range((n * d) // r))
    edges = [(x, y) for x in xs for y in ys if abs(2 * x - y + 0.5) < 3 or len(ys) - abs(2 * x - y + 0.5) < 3]
    g = random_graph.SwitchBipartiteGraph(xs, ys, edges)
    neighbourhoods = g.neighbourhoods()

    assert set(neighbourhoods.keys()) == {"x", "y"}
    assert len(neighbourhoods["x"]) == n
    assert len(neighbourhoods["y"]) == (n * d) // r
    assert all(len(nhood) == d for nhood in neighbourhoods["x"])
    assert all(len(nhood) == r for nhood in neighbourhoods["y"])
    assert [0, 1, 2, 3, 18, 19] in neighbourhoods["x"]
    assert list(range(12, 2)) not in neighbourhoods["x"]
    assert [0, 1, 9] in neighbourhoods["y"]
    assert [0, 4, 9] not in neighbourhoods["y"]


def test_switch():
    assert True
