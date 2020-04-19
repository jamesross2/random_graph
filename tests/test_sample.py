import pytest

import random_graph
import random_graph.switch_bipartite_graph


def test_sample_bipartite_graph():
    # returns a graph
    edges = random_graph.sample_bipartite_graph([5] * 12, [3] * 20, n_iter=int(1e4))
    assert isinstance(edges, set)
    assert len(edges) == 60
    assert [sum(edge[0] == x for edge in edges) for x in range(13)] == [5] * 12 + [0]

    graph = random_graph.switch_bipartite_graph.SwitchBipartiteGraph(12, 20, edges)
    assert isinstance(graph, random_graph.switch_bipartite_graph.SwitchBipartiteGraph)
    assert graph.degree_sequence == {"x": (5,) * 12, "y": (3,) * 20}


def test_sample_graph():
    with pytest.raises(NotImplementedError):
        edges = random_graph.sample_graph([5] * 20)
