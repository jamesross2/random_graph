"""Helper functions for random graph generation; typically not for use by user."""

import collections
import typing


def valid_bipartite_graph(nx: int, ny: int, edges: typing.List[typing.Tuple[int, int]]) -> bool:
    """Check whether given graph arguments are valid.

    This function performs basic argument validation on inputs. It is not a test for whether such a graph exists. This
    basically checks that the edges are compatible with the other arguments (rather than checking that a degree sequence
    is graphical).

    Args:
        nx: Number of vertices in X.
        ny: Number of vertices in Y.
        edges: A list of edges in the graph.

    Returns:
        True if the arguments are valid.
    """
    # check that arguments are valid
    if nx < 0 or ny < 0:
        return False

    edges = list(edges)
    if len(set(edges)) < len(edges):
        return False

    edges_valid_nodes = [edge[0] < nx and edge[1] < ny for edge in edges]
    if not all(edges_valid_nodes):
        return False

    # if nothing failed, then we are done
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


def degree_sequence_graphical(dx: typing.Sequence[int], dy: typing.Sequence[int]) -> bool:
    """Test whether the given degree sequence is graphical.

    A degree sequence is graphical if some graph with the given degree sequence exists. In the bipartite case, this
    can be tested using the Gale–Ryser theorem.

    Args:
        dx: Degree sequence for vertices in X.
        dy: Degree sequence for vertices in Y.

    Returns:
        True if the degree sequence is graphical, False otherwise.
    """
    # check that arguments are valid
    if any(d < 0 for ds in (dx, dy) for d in ds):
        # all degrees must be non-negative
        return False

    # check conditions that are likely false for very wrong sequences
    if sum(dx) != sum(dy):
        # can't have different degree totals in X and Y
        return False

    # check remaining Gale–Ryser conditions
    dx = sorted(dx, reverse=True)
    passes = all(sum(dx[:k]) <= sum(min(d, k) for d in dy) for k in range(len(dx)))
    return passes
