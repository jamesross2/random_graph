import copy

import pytest

import random_graph


def create_graph(graph_type="1", **kwargs):
    if graph_type == "1":
        size = kwargs.get("size", 10)
        edges = [(x, y) for x in range(size) for y in range(size) if abs(x - y) < 2 or size - abs(x - y) < 2]
        g = random_graph.SwitchBipartiteGraph(size, size, edges)
        return g


def test_init():
    # check that empty initialisation (and variations of) work
    _ = random_graph.SwitchBipartiteGraph(0, 0, [])
    _ = random_graph.SwitchBipartiteGraph(10, 0, [])
    _ = random_graph.SwitchBipartiteGraph(0, 15, [])
    _ = random_graph.SwitchBipartiteGraph(17, 19, [])

    # check that numbers of nodes are correct
    g = random_graph.SwitchBipartiteGraph(7, 9, [])
    assert g.nx == 7
    assert g.ny == 9

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
    nx, d, r = 10, 6, 3
    ny = (nx * d) // r
    edges = [(x, y) for x in range(nx) for y in range(ny) if abs(2 * x - y + 0.5) < 3 or ny - abs(2 * x - y + 0.5) < 3]
    g = random_graph.SwitchBipartiteGraph(nx, ny, edges)

    assert len(g.neighbourhoods("x")) == nx
    assert len(g.neighbourhoods("y")) == ny
    assert all(len(nhood) == d for nhood in g.neighbourhoods("x"))
    assert all(len(nhood) == r for nhood in g.neighbourhoods("y"))
    assert {0, 1, 2, 3, 18, 19} in g.neighbourhoods("x")
    assert set(range(12, 2)) not in g.neighbourhoods("x")
    assert {0, 1, 9} in g.neighbourhoods("y")
    assert {0, 4, 9} not in g.neighbourhoods("y")


def test_switch():
    # create a graph that can be mutated
    g = create_graph(type="1", size=10)

    # force one mutation
    edges_start = copy.deepcopy(g.edges)
    switched = g.switch()
    while not switched:
        switched = g.switch()
    edges_final = copy.deepcopy(g.edges)

    # check that difference is correct
    assert len(edges_start - edges_final) == 2
    assert len(edges_final - edges_start) == 2
    vertices_start = {v for e in edges_start - edges_final for v in e}
    vertices_final = {v for e in edges_final - edges_start for v in e}
    assert vertices_start == vertices_final
    assert len(vertices_start) <= 4
