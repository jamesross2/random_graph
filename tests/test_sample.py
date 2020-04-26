import random

import pytest

import random_graph


def test_sample_bipartite_graph():
    # returns a graph
    edges = random_graph.sample_bipartite_graph([5] * 12, [3] * 20, n_iter=int(1e4))
    assert isinstance(edges, set)
    assert len(edges) == 60
    assert [sum(edge[0] == x for edge in edges) for x in range(13)] == [5] * 12 + [0]

    graph = random_graph.graphs.SwitchBipartiteGraph(12, 20, edges)
    assert isinstance(graph, random_graph.graphs.SwitchBipartiteGraph)
    assert graph.degree_sequence == {"x": (5,) * 12, "y": (3,) * 20}


def test_sample_graph():
    with pytest.raises(NotImplementedError):
        edges = random_graph.sample_graph([5] * 20)


def test_random_seed_switching():
    # check that results are consistent after setting seed
    random.seed(0)
    edges1 = random_graph.sample_bipartite_graph(dx=[5] * 12, dy=[3] * 20, n_iter=int(1e4))
    edges2 = random_graph.sample_bipartite_graph(dx=[5] * 12, dy=[3] * 20, n_iter=int(1e4))
    random.seed(0)
    edges3 = random_graph.sample_bipartite_graph(dx=[5] * 12, dy=[3] * 20, n_iter=int(1e4))

    assert edges1 == edges3
    assert edges1 != edges2
