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
    random.seed(0)
    edges = random_graph.sample_bipartite_graph(dx=[5] * 12, dy=[3] * 20, n_iter=int(1e4))
    edges_expected = set.union(
        {(7, 17), (4, 3), (3, 1), (5, 4), (4, 12), (9, 2), (5, 7), (0, 2), (5, 10), (10, 0)},
        {(8, 6), (8, 18), (1, 6), (11, 14), (1, 3), (1, 9), (2, 14), (10, 15), (2, 17), (1, 15)},
        {(6, 5), (6, 8), (7, 13), (3, 3), (9, 7), (5, 12), (8, 5), (11, 1), (8, 8), (10, 11)},
        {(0, 4), (0, 10), (9, 19), (10, 8), (11, 13), (0, 19), (2, 10), (11, 19), (6, 7), (3, 2)},
        {(4, 1), (7, 18), (4, 4), (9, 0), (3, 14), (5, 11), (4, 13), (3, 17), (9, 12), (2, 0)},
        {(8, 16), (11, 18), (2, 9), (10, 16), (0, 15), (1, 16), (6, 6), (7, 5), (7, 11), (6, 9)},
    )
    assert edges == edges_expected
