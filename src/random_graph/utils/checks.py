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

    edges_valid_nodes = [x < nx and y < ny for (x, y) in edges]
    if not all(edges_valid_nodes):
        return False

    # if nothing failed, then we are done
    return True


def valid_directed_graph(n: int, edges: typing.List[typing.Tuple[int, int]]) -> bool:
    """Check whether given graph arguments are valid

    Args:
        n: Number of vertices in X.
        edges: A list of edges in the graph.

    Returns:
        True if the arguments are valid.
    """
    # check that arguments are valid
    if n < 0:
        return False

    edges = list(edges)
    if len(set(edges)) < len(edges):
        return False

    edges_valid_nodes = [x < n and y < n for (x, y) in edges]
    if not all(edges_valid_nodes):
        return False

    if any(x == y for (x, y) in edges):
        return False

    # if nothing failed, then we are done
    return True


def valid_multi_hypergraph(n: int, edges: typing.List[typing.Set[int]]) -> bool:
    """Check whether given arguments are valid

    Args:
        n: Number of vertices in X.
        edges: A list of edges in the graph.

    Returns:
        True if the arguments are valid.
    """
    # check that arguments are valid
    if n < 0:
        return False

    edges = list(edges)
    edges_valid_nodes = [x < n for edge in edges for x in edge]
    if not all(edges_valid_nodes):
        return False

    edges_valid_sets = [len(edge) == len(set(edge)) for edge in edges]
    if not all(edges_valid_sets):
        return False

    # if nothing failed, then we are done
    return True


def valid_simple_graph(n: int, edges: typing.List[typing.Set[int]]) -> bool:
    """Check whether given arguments are valid

    Args:
        n: Number of vertices in X.
        edges: A list of edges in the graph.

    Returns:
        True if the arguments are valid.
    """
    # non-negative number of vertices
    if n < 0:
        return False

    # edges all unique
    edges = [tuple(sorted(edge)) for edge in edges]
    if len(set(edges)) < len(edges):
        return False

    # edges all contain pairs of nodes
    if any(len(set(edge)) != 2 or len(edge) != 2 for edge in edges):
        return False

    # edges all contain valid nodes
    edges_valid_nodes = [x < n and y < n for (x, y) in edges]
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


def bipartite_degree_sequence_graphical(dx: typing.Sequence[int], dy: typing.Sequence[int]) -> bool:
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


def directed_degree_sequence_graphical(degree_sequence: typing.Sequence[typing.Tuple[int, int]]) -> bool:
    """Test whether the given directed degree sequence is graphical.

    Args:
        degree_sequence: Directed degree sequence for vertices in X, in the form of (int degree, out degree) pairs.

    Returns:
        True if the degree sequence is graphical, False otherwise.

    References:
        D.R. Fulkerson: Zero-one matrices with zero trace. In: Pacific J. Math. No. 12, 1960, pp. 831–836.
        Wai-Kai Chen: On the realization of a (p,s)-digraph with prescribed degrees. In: Journal of the Franklin
            Institute No. 6, 1966, pp. 406–422.
        Richard Anstee: Properties of a class of (0,1)-matrices covering a given matrix. In: Can. J. Math., 1982, pp.
            438–453.
    """
    # check that arguments are valid
    if any(dx < 0 or dy < 0 for (dx, dy) in degree_sequence):
        # all degrees must be non-negative
        return False

    # check conditions that are likely false for very wrong sequences
    dx, dy = zip(*degree_sequence)
    if sum(dx) != sum(dy):
        # can't have different degree totals in X and Y
        return False

    # sort degrees simultaneously
    dx, dy = zip(*sorted(degree_sequence, reverse=True))

    # check remaining Gale–Ryser conditions
    passes = all(
        sum(dx[:k]) <= sum(min(d, k - 1) for d in dy[:k]) + sum(min(d, k) for d in dy[k:]) for k in range(len(dx))
    )
    return passes


def simple_degree_sequence_graphical(degree_sequence: typing.Sequence[int]) -> bool:
    """Test whether the given degree sequence is graphical.

    Args:
        degree_sequence: Degree sequence for vertices in X.

    Returns:
        True if the degree sequence is graphical, False otherwise.

    References:
        P. Erdős, T. Gallai: Gráfok előírt fokszámú pontokkal, Matematikai Lapok (1960), 11: 264–274
    """
    # check that arguments are valid
    if any(d < 0 for d in degree_sequence):
        # all degrees must be non-negative
        return False

    if sum(degree_sequence) % 2 != 0:
        # must have even total degree
        return False

    # check remaining Gale–Ryser conditions
    ds = degree_sequence
    passes = all(sum(ds[:k]) <= k * (k - 1) + sum(min(d, k) for d in ds[k + 1 :]) for k in range(1, len(ds) + 1))
    return passes
