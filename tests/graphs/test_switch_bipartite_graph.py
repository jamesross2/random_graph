import copy
import itertools

import pytest

import random_graph


def create_graph(graph_type="1", **kwargs):
    if graph_type == "1":
        size = kwargs.get("size", 10)
        edges = [(x, y) for x in range(size) for y in range(size) if abs(x - y) < 2 or size - abs(x - y) < 2]
        g = random_graph.graphs.SwitchBipartiteGraph(size, size, edges)
        return g


def test_init():
    # check that empty initialisation (and variations of) work
    _ = random_graph.graphs.SwitchBipartiteGraph(0, 0, [])
    _ = random_graph.graphs.SwitchBipartiteGraph(10, 0, [])
    _ = random_graph.graphs.SwitchBipartiteGraph(0, 15, [])
    _ = random_graph.graphs.SwitchBipartiteGraph(17, 19, [])

    # check that numbers of nodes are correct
    g = random_graph.graphs.SwitchBipartiteGraph(7, 9, [])
    assert g.nx == 7
    assert g.ny == 9

    # check that invalid edges are rejected
    with pytest.raises(ValueError, match="Provided arguments are not a valid bipartite graph"):
        assert not random_graph.graphs.SwitchBipartiteGraph(10, 10, [(0, 0), (0, 0)])
    with pytest.raises(ValueError, match="Provided arguments are not a valid bipartite graph"):
        assert not random_graph.graphs.SwitchBipartiteGraph(10, 10, [(99, 0)])

    # check that graphs with edges are correct
    g = create_graph(type="1", size=5)
    assert g.nx == 5
    assert g.ny == 5
    assert len(list(g.edges)) == 5 * 3
    assert all(edge in g.edges for edge in [(1, 1), (2, 2), (1, 0), (1, 2), (2, 1), (4, 4)])
    assert all(
        edge not in g.edges for edge in [(0, 2), (0, 3), (1, 3), (1, 4), (2, 4), (2, 0), (3, 0), (3, 1), (4, 1), (4, 2)]
    )
    assert g.degree_sequence == {"x": (3, 3, 3, 3, 3), "y": (3, 3, 3, 3, 3)}

    # create an asymmetric graph for further testing
    edges = ((1, 1), (1, 6), (2, 1), (2, 2), (3, 4), (3, 5), (3, 6), (4, 6))
    g = random_graph.graphs.SwitchBipartiteGraph(nx=5, ny=8, edges=edges)
    assert g.nx == 5
    assert g.ny == 8
    assert len(list(g.edges)) == len(edges)
    assert all(edge in g.edges for edge in edges)
    assert all(edge not in g.edges for edge in itertools.product(range(5), range(8)) if edge not in edges)
    assert g.degree_sequence == {"x": (0, 2, 2, 3, 1), "y": (0, 2, 1, 0, 1, 1, 3, 0)}


def test_switching():
    g1 = random_graph.graphs.SwitchBipartiteGraph(5, 5, [(x, y) for x in range(5) for y in (x, (x + 1) % 5)])
    g2 = copy.deepcopy(g1)
    assert g1 == g2
    switched = g2.switch()
    while not switched:
        switched = g2.switch()
    assert g1 != g2


def test_print():
    g_short = random_graph.graphs.SwitchBipartiteGraph(3, 3, ((0, 0), (0, 1), (1, 1), (2, 2)))
    assert str(g_short).startswith("Switch Bipartite Graph with nx=3")

    g_complete = random_graph.graphs.SwitchBipartiteGraph(20, 20, ((x, y) for x in range(20) for y in range(20)))
    assert str(g_complete).startswith("Switch Bipartite Graph with nx=20")


def test_neighbourhoods():
    # build a hypergraph with clear neighbourhoods
    nx, d, r = 10, 6, 3
    ny = (nx * d) // r
    edges = [(x, y) for x in range(nx) for y in range(ny) if abs(2 * x - y + 0.5) < 3 or ny - abs(2 * x - y + 0.5) < 3]
    g = random_graph.graphs.SwitchBipartiteGraph(nx, ny, edges)

    assert len(g.neighbourhoods("x")) == nx
    assert len(g.neighbourhoods("y")) == ny
    assert all(len(nhood) == d for nhood in g.neighbourhoods("x"))
    assert all(len(nhood) == r for nhood in g.neighbourhoods("y"))
    assert {0, 1, 2, 3, 18, 19} in g.neighbourhoods("x")
    assert set(range(12, 2)) not in g.neighbourhoods("x")
    assert {0, 1, 9} in g.neighbourhoods("y")
    assert {0, 4, 9} not in g.neighbourhoods("y")

    with pytest.raises(ValueError, match="Side must be 'x' or 'y'"):
        g.neighbourhoods("z")


def test_switch():
    # create a graph that can be mutated
    g = create_graph(type="1", size=10)

    # force one mutation
    edges_start = set(g.edges)
    switched = g.switch()
    while not switched:
        switched = g.switch()
    edges_final = set(g.edges)

    # check that difference is correct
    assert len(edges_start - edges_final) == 2
    assert len(edges_final - edges_start) == 2
    vertices_start = {v for e in edges_start - edges_final for v in e}
    vertices_final = {v for e in edges_final - edges_start for v in e}
    assert vertices_start == vertices_final
    assert len(vertices_start) <= 4


def test_from_degree_sequence():
    dx = list(range(1, 6)) + list(range(5, 0, -1))
    dy = [3] * 5 + [2] * 5 + [1] * 5
    graph = random_graph.graphs.SwitchBipartiteGraph.from_degree_sequence(dx, dy)
    assert isinstance(graph, random_graph.graphs.SwitchBipartiteGraph)
    assert graph.degree_sequence == {"x": tuple(dx), "y": tuple(dy)}

    with pytest.raises(ValueError, match="Degree sequence is not graphical"):
        random_graph.graphs.SwitchBipartiteGraph.from_degree_sequence(dx, dy * 2)


def test_hypergraph_conversion():
    # create a basic bipartite graph to convert
    hgraph = random_graph.graphs.SwitchMultiHypergraph.from_degree_sequence([6] * 8, [3] * 16)
    bgraph = hgraph.to_bipartite_graph()
    assert bgraph.nx == 8
    assert bgraph.ny == 16
    assert bgraph.degree_sequence == {"x": (6,) * 8, "y": (3,) * 16}
