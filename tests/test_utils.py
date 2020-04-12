import pytest

import random_graph.utils


def test_assert_valid_bipartite_graph():
    assert random_graph.utils.assert_valid_bipartite_graph(10, 9, [])
    assert random_graph.utils.assert_valid_bipartite_graph(5, 4, [])
    assert random_graph.utils.assert_valid_bipartite_graph(8, 9, [])
    with pytest.raises(ValueError, match="Must have a non-negative number of nodes"):
        random_graph.utils.assert_valid_bipartite_graph(-1, 10, [])
    with pytest.raises(ValueError, match="Not all edges are unique"):
        random_graph.utils.assert_valid_bipartite_graph(5, 10, [(1, 1), (1, 1)])
    with pytest.raises(ValueError, match="does not appear in nodes"):
        random_graph.utils.assert_valid_bipartite_graph(5, 5, [(10, 10)])


def test_all_unique():
    assert random_graph.utils.all_unique([])
    assert random_graph.utils.all_unique("abcdefg")
    assert random_graph.utils.all_unique(range(5))
    assert random_graph.utils.all_unique([None, 1, 2, "a"])
    assert not random_graph.utils.all_unique("abba")
    assert not random_graph.utils.all_unique(list(range(5)) + [4])
