import random

import pytest

import random_graph


def test_sample_bipartite_graph():
    # returns a graph
    dx = (5,) * 12
    dy = (3,) * 20
    edges = random_graph.sample_bipartite_graph(dx, dy, n_iter=int(1e4))
    assert isinstance(edges, list)
    assert all(isinstance(edge, tuple) for edge in edges)
    assert len(edges) == 60
    assert [sum(edge[0] == x for edge in edges) for x in range(13)] == [5] * 12 + [0]

    graph = random_graph.graphs.SwitchBipartiteGraph(12, 20, edges)
    assert isinstance(graph, random_graph.graphs.SwitchBipartiteGraph)
    assert graph.degree_sequence == {"x": dx, "y": dy}


def test_sample_directed_graph():
    degree_sequence = ((1, 2),) * 3 + ((2, 1),) * 3
    edges = random_graph.sample_directed_graph(degree_sequence, n_iter=int(1e4))
    assert isinstance(edges, list)
    assert all(isinstance(edge, tuple) for edge in edges)
    assert len(edges) == 9
    assert all(len(edge) == 2 for edge in edges)

    graph = random_graph.graphs.SwitchDirectedGraph(6, edges)
    assert graph.degree_sequence == degree_sequence


def test_sample_multi_hypergraph():
    degree_sequence = (5,) * 6
    edge_sizes = (3,) * 10
    edges = random_graph.sample_multi_hypergraph(degree_sequence, edge_sizes, n_iter=int(1e4))
    assert isinstance(edges, list)
    assert all(isinstance(edge, set) for edge in edges)
    assert len(edges) == 10
    assert all(len(edge) == 3 for edge in edges)

    graph = random_graph.graphs.SwitchMultiHypergraph(6, edges)
    assert graph.degree_sequence == degree_sequence
    assert graph.edge_sizes == edge_sizes


def test_sample_simple_graph():
    degree_sequence = (6,) * 20
    edges = random_graph.sample_simple_graph(degree_sequence, n_iter=int(1e4))
    assert isinstance(edges, list)
    assert all(isinstance(edge, set) for edge in edges)
    assert len(edges) == 60
    assert all(len(edge) == 2 for edge in edges)

    graph = random_graph.graphs.SwitchSimpleGraph(20, edges)
    assert graph.degree_sequence == degree_sequence


def test_random_seed_switching():
    # check that results are consistent after setting seed
    random.seed(0)
    edges1 = random_graph.sample_bipartite_graph(dx=[5] * 12, dy=[3] * 20, n_iter=int(1e4))
    edges2 = random_graph.sample_bipartite_graph(dx=[5] * 12, dy=[3] * 20, n_iter=int(1e4))
    random.seed(0)
    edges3 = random_graph.sample_bipartite_graph(dx=[5] * 12, dy=[3] * 20, n_iter=int(1e4))

    assert edges1 == edges3
    assert edges1 != edges2
