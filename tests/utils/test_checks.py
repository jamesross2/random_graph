import pytest

import random_graph.utils


def test_valid_bipartite_graph():
    assert random_graph.utils.valid_bipartite_graph(10, 9, [])
    assert random_graph.utils.valid_bipartite_graph(5, 4, [])
    assert random_graph.utils.valid_bipartite_graph(8, 9, [])

    assert not random_graph.utils.valid_bipartite_graph(-1, 10, [])
    assert not random_graph.utils.valid_bipartite_graph(5, 10, [(1, 1), (1, 1)])
    assert not random_graph.utils.valid_bipartite_graph(5, 5, [(10, 10)])


def test_all_unique():
    assert random_graph.utils.checks.all_unique([])
    assert random_graph.utils.checks.all_unique("abcdefg")
    assert random_graph.utils.checks.all_unique(range(5))
    assert random_graph.utils.checks.all_unique([None, 1, 2, "a"])

    assert not random_graph.utils.checks.all_unique("abba")
    assert not random_graph.utils.checks.all_unique(list(range(5)) + [4])


def test_degree_sequence_graphical():
    assert random_graph.utils.degree_sequence_graphical([5] * 3, [3] * 5)
    assert random_graph.utils.degree_sequence_graphical([1] * 10, [1] * 10)
    assert random_graph.utils.degree_sequence_graphical([1] * 10, [10] * 1)
    assert random_graph.utils.degree_sequence_graphical([5] * 5, [5] * 5)

    assert not random_graph.utils.degree_sequence_graphical([5] * 3, [3])
    assert not random_graph.utils.degree_sequence_graphical([-1], [-1])
    assert not random_graph.utils.degree_sequence_graphical([6, 6], [4, 4, 4])
