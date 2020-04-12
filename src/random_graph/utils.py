"""Helper functions for random graph generation; typically not for use by user."""

import collections
import typing


def assert_valid_bipartite_graph(nx: int, ny: int, edges: typing.List[typing.Tuple[int, int]]) -> bool:
    """Check whether given graph arguments are valid.

    This function performs basic argument validation on inputs. It is not a test for whether such a graph exists! This
    does not make sense when we know the edges (it is used if we only know the degree sequence, for example).

    Args:
        nx: Number of vertices in X.
        ny: Number of vertices in Y.
        edges: A list of edges in the graph.

    Returns:
        True if the arguments are valid.

    Raises:
        ValueError: If the provided inputs are invalid.
    """
    # check that arguments are valid
    if nx < 0 or ny < 0:
        raise ValueError("Must have a non-negative number of nodes")

    edges = list(edges)
    if len(set(edges)) < len(edges):
        raise ValueError("Not all edges are unique.")

    edges_valid_nodes = [edge[0] < nx and edge[1] < ny for edge in edges]
    if not all(edges_valid_nodes):
        bad_index = min(n for n, test in enumerate(edges_valid_nodes) if not test)
        bad_edge = edges[bad_index]
        raise ValueError(f"Provided edge {bad_edge} does not appear in nodes.")

    return True


def all_unique(x: typing.Iterable[collections.abc.Hashable]) -> bool:
    """Checks that every element of the iterable is unique.

    Args:
        x: an iterable to check for unique elements. No further iteration is done if a duplicate is found.

    Returns:
        True if all elements are unique, False otherwise.
    """
    seen = set()
    for element in x:
        if element in seen:
            return False
        else:
            seen.add(element)
    return True
