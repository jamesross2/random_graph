"""High-level functions for creating random graphs with given degree sequence.

These functions are intended for users who are satisfied with using the default arguments for their sampling process.
They are convenient, and provide a simple interface to the underlying objects and classes.
"""

import typing

from . import graphs


def sample_bipartite_graph(
    dx: typing.Sequence[int], dy: typing.Sequence[int], n_iter: int = int(1e6)
) -> typing.Set[typing.Tuple[int, int]]:
    """Sample a bipartite graph with given degree sequence, approximately uniformly at random from all possibilities.

    This function uses a switch chain to sample bipartite graphs approximately uniformly at random. It initialises
    the chain with a non-random starting state (created using an approach from the Gale-Ryser theorem that mirrors the
    Havel-Hakimi construction for simple graphs). It then applies a number of switches, each of which swaps the
    endpoints of a pair of edges. This Markov chain is reversible and has the uniform distribution as its stationary
    distribution, so the result is a bipartite graph sampled approximately uniformly at random after sufficiently many
    iterations. Moreover, it is rapidly converging (so that the total variation distance between the uniform
    distribution and the state distribution approaches epsilon in time $O(log(n) * log(epsilon^{-1}))$.

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
    return set(graph.edges)


def sample_graph(d: typing.Sequence[int], n_iter: int = int(1e6)) -> NotImplementedError:
    """Sample a simple graph with given degree sequence, approximately uniformly at random from all possibilities.

    This function is not yet implemented. Raise a feature request on the project GitHub to let the authors know that
    you're interested!

    Args:
        d: Degree sequence.
        n_iter: Number of iterations to perform in the resampling phase.

    Raises:
        NotImplementedError: This will be raised until the code is finished.
    """
    raise NotImplementedError("Let the authors know you'd like this function!")
