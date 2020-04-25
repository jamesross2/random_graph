#!/usr/bin/env python3
"""Profile the MCMC iteration process.

We use this script to identify opportunities for optimisation within the package.
"""
import argparse
import cProfile
import pstats
import random
import itertools
import typing

import random_graph


# set up arguments
def parse_arguments() -> typing.Dict[str, typing.Any]:
    """Get command line arguments"""
    # get user arguments
    parser = argparse.ArgumentParser("Profile the random graph sampler")
    subparsers = parser.add_subparsers(title="Graph type", help="Choose degree sequence determination process", dest="graph_type")

    # bi-regular degrees process
    parser_regular = subparsers.add_parser("regular", help="Create a graph with uniform degree in X and Y")
    parser_regular.add_argument("--n", help="Number of vertices in X [default (%s)]", type=int, default=1000)
    parser_regular.add_argument("--dx", help="Degree for vertices in X [default (%s)]", type=int, default=50)
    parser_regular.add_argument("--dy", help="Degree for vertices in Y [default (%s)]", type=int, default=50)

    # Erdos-Renyi G(n, p) process
    parser_independent = subparsers.add_parser("independent", help="Create a graph with edges chosen independently")
    parser_independent.add_argument("--n", help="Number of vertices in X [default (%s)]", type=int, default=1000)
    parser_independent.add_argument("--m", help="Number of vertices in Y [default (%s)]", type=int, default=1000)
    parser_independent.add_argument("--p", help="Edge selection probability [default (%s)]", type=float, default=0.05)

    args = parser.parse_args()
    return vars(args)


# create graphs
def create_regular_bigraph(n: int, dx: int, dy: int) -> random_graph.graphs.SwitchBipartiteGraph:
    dx = [dx] * n
    dy = [dy] * (sum(dx) // dy)
    g = random_graph.graphs.SwitchBipartiteGraph.from_degree_sequence(dx, dy)
    return g


def sample_independent_edge_graph(n: int, m: int, p: float) -> random_graph.graphs.SwitchBipartiteGraph:
    edges = {edge for edge in itertools.product(range(n), range(m)) if random.random() <= p}
    g = random_graph.graphs.SwitchBipartiteGraph(n, m, edges)
    return g


# import run_mcmc to run chain
def profile_mcmc(arguments) -> pstats.Stats:
    """Create a bi-uniform bipartite graph and profile the MCMC operation."""
    # sample initial graph
    graph_type = arguments.pop("graph_type")
    if graph_type == "regular":
        graph = create_regular_bigraph(**arguments)
    elif graph_type == "independent":
        graph = sample_independent_edge_graph(**arguments)
    else:
        raise ValueError(f"Unrecognised graph type {graph_type}")

    # use basic settings for profiling
    profiler = cProfile.Profile()
    profiler.enable()
    for _ in range(int(1e6)):
        graph.switch()
    profiler.disable()

    # extract statistics from profiler
    stats = pstats.Stats(profiler).strip_dirs().sort_stats("cumtime")
    stats.print_stats(50)
    return stats


if __name__ == "__main__":
    arguments = parse_arguments()
    stats = profile_mcmc(arguments)
