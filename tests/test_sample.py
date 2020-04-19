import pytest

import random_graph
from random_graph import graphs


def test_sample_bipartite_graph():
    # returns a graph
    edges = random_graph.sample_bipartite_graph([5] * 12, [3] * 20, n_iter=int(1e4))
    assert isinstance(edges, set)
    assert len(edges) == 60
    assert [sum(edge[0] == x for edge in edges) for x in range(13)] == [5] * 12 + [0]

    graph = graphs.SwitchBipartiteGraph(12, 20, edges)
    assert isinstance(graph, graphs.SwitchBipartiteGraph)
    assert graph.degree_sequence == {"x": (5,) * 12, "y": (3,) * 20}


def test_sample_graph():
    with pytest.raises(NotImplementedError):
        edges = random_graph.sample_graph([5] * 20)
