"""High-level functions for creating random graphs with given degree sequence.

These functions are intended for users who are satisfied with using the default arguments for their sampling process.
They are convenient, and provide a simple interface to the underlying objects and classes.
"""

import typing

from . import graphs


def sample_bipartite_graph(
    dx: typing.Sequence[int], dy: typing.Sequence[int], n_iter: int = int(1e6)
) -> typing.List[typing.Tuple[int, int]]:
    """Sample a bipartite graph with given degree sequence approximately uniformly at random.

    Args:
        dx: Degree sequence for vertices in X.
        dy: Degree sequence for vertices in Y.
        n_iter: Number of iterations to perform in the resampling phase.

    Returns:
        A set of edges in the form of vertex pairs (x, y).
    """
    # TODO: determine whether degree sequence is proven to be rapidly converging
    # TODO: if not provided, determine number of iterations required to ensure randomness

    # start with a greedily-created bipartite graph
    graph = graphs.SwitchBipartiteGraph.from_degree_sequence(dx, dy)

    # apply iterations to ensure graph is sufficiently random
    for _ in range(n_iter):
        graph.switch()

    # return created graph
    return list(graph.edges)


def sample_directed_graph(
    degree_sequence: typing.Sequence[typing.Tuple[int, int]], n_iter: int = int(1e6)
) -> typing.List[typing.Tuple[int, int]]:
    """Sample a directed graph with given degree sequence approximately uniformly at random.

    Args:
        degree_sequence: Degree sequence, in the form of a sequence of (in_degree, out_degree) pairs.
        n_iter: Number of iterations to perform in the resampling phase.

    Returns:
        A list of edges in the form of vertex pairs (x, y).
    """
    # TODO: determine whether degree sequence is proven to be rapidly converging
    # TODO: if not provided, determine number of iterations required to ensure randomness

    # start with a greedily-created bipartite graph
    graph = graphs.SwitchDirectedGraph.from_degree_sequence(degree_sequence)

    # apply iterations to ensure graph is sufficiently random
    for _ in range(n_iter):
        graph.switch()

    # return created graph
    return list(graph.edges)


def sample_multi_hypergraph(
    degree_sequence: typing.Sequence[int], edge_sequence: typing.Sequence[int], n_iter: int = int(1e6)
) -> typing.List[typing.Set[int]]:
    """Sample a multi hypergraph with given degree sequence and edge sequence approximately uniformly at random.

    Args:
        degree_sequence: Degree sequence for vertices in X.
        edge_sequence: List containing the sizes of each edge.
        n_iter: Number of iterations to perform in the resampling phase.

    Returns:
        A list of edges in the form of vertex pairs (x, y).
    """
    # TODO: determine whether degree sequence is proven to be rapidly converging
    # TODO: if not provided, determine number of iterations required to ensure randomness

    # start with a greedily-created bipartite graph
    graph = graphs.SwitchMultiHypergraph.from_degree_sequence(degree_sequence, edge_sequence)

    # apply iterations to ensure graph is sufficiently random
    for _ in range(n_iter):
        graph.switch()

    # return created graph
    return list(graph.edges)


def sample_simple_graph(degree_sequence: typing.Sequence[int], n_iter: int = int(1e6)) -> typing.List[typing.Set[int]]:
    """Sample a simple graph with given degree sequence approximately uniformly at random.

    Args:
        degree_sequence: Degree sequence for vertices in X.
        n_iter: Number of iterations to perform in the resampling phase.

    Returns:
        A list of edges in the form of vertex pairs (x, y).
    """
    # TODO: determine whether degree sequence is proven to be rapidly converging
    # TODO: if not provided, determine number of iterations required to ensure randomness

    # start with a greedily-created bipartite graph
    graph = graphs.SwitchSimpleGraph.from_degree_sequence(degree_sequence)

    # apply iterations to ensure graph is sufficiently random
    for _ in range(n_iter):
        graph.switch()

    # return created graph
    return list(graph.edges)
