#!/usr/bin/env python3
"""Run an MCMC chain over a range of regular degree sequences to estimate H-simple likelihoods."""
import argparse
import typing
import random_graph
import networkx
import warnings
import itertools
import random
import csv
import pathlib
import tqdm
import logging


def create_graph(n: int, d: int, r: int, attempts: int = int(1e3)) -> random_graph.SwitchBipartiteGraph:
    """Create a BipartiteGraph with the given properties."""
    # create degree sequences as expected by networkX
    if ((n * d) % r) != 0:
        raise ValueError("No regular, uniform graphs exist with given parameters.")
    num_edges = (n * d) // r
    deg_x = [d] * n
    deg_y = [r] * num_edges

    if attempts < 1:
        raise ValueError(f"Number of attempts must be positive, found {attempts}.")
    for iteration in range(attempts):
        graph = networkx.algorithms.bipartite.reverse_havel_hakimi_graph(aseq=deg_x, bseq=deg_y, create_using=networkx.Graph())
        if graph.degree() == deg_x + deg_y:
            break

    # check that graph satisfies requirements
    if graph.degree() != deg_x + deg_y:
        raise RuntimeError(f"Could not generate graph with (n={n}, d={d}, r={r}) in {attempts} iterations.")

    # convert graph into BipartiteGraph format
    bipartite_graph = random_graph.SwitchBipartiteGraph(nodes_x=list(range(n)), nodes_y=range(n, n + num_edges), edges=list(graph.edges))
    return bipartite_graph


def create_uniform_regular_graph(n: int, d: int, r: int, attempts: int = int(1e3)) -> random_graph.SwitchBipartiteGraph:
    """Create a BipartiteGraph with the given properties.

    Note that the current implementation is non-random, and will also fail for various valid degree sequences.
    """
    # check inputs
    if ((n * d) % r) != 0:
        raise ValueError("No regular, uniform graphs exist with given parameters.")
    num_edges_final = (n * d) // r
    num_edges_phase1 = n * (d // r)

    # choose floor(d/r) unique edges to "spread" across all nodes
    # remove first edge: if degrees line up in a certain way, this is the only way to get certain degree sequences
    edge_bases = [(0, *nodes) for nodes in itertools.combinations(range(1, n), r-1)]
    edge_base_p1 = edge_bases if num_edges_final == num_edges_phase1 else edge_bases[1:]

    # phase 1: choose an edge and spread across all nodes
    edges = set()
    while len(edges) < num_edges_phase1:
        base = edge_base_p1.pop(random.choice(range(len(edge_base_p1))))
        if base not in edges:
            new_edges = set(tuple((node + shift) % n for node in base) for shift in range(n))
            # only update if we don't overshoot!
            if len(edges) + len(new_edges) <= num_edges_final:
                edges.update(new_edges)

    # phase 2: spread edges that align within nodes perfectly
    while len(edges) < num_edges_final:
        raise NotImplementedError("More work needed to handle this degree sequence!")

    # edges acquired; return graph
    edges_bipartite = [(node, edge) for edge, nodes in enumerate(edges) for node in nodes]
    graph = random_graph.SwitchBipartiteGraph(nodes_x=list(range(n)), nodes_y=range(num_edges_final), edges=edges_bipartite)
    return graph


def mcmc(n: int, d: int, r: int, iterations: int) -> typing.Sequence[bool]:
    """Run MCMC sampling on a provided graph to test for simple-ness"""
    try:
        graph = create_uniform_regular_graph(n, d, r)
    except RuntimeError:
        warnings.warn("Could not generated graph.")
        return []

    resampler = random_graph.Resampler(graph)
    history = resampler.mcmc(iterations=iterations, callback=lambda g: g.simple, call_every=1, burn_in=100)
    return history


def sample(n: typing.Sequence[int], d: typing.Sequence[int], r: typing.Sequence[int], iterations: int, output_filepath: typing.Union[str, pathlib.Path]):
    results = []
    for n_curr, d_curr, r_curr in tqdm.tqdm(itertools.product(n, d, r), desc="parameters", leave=True):
        results_curr = mcmc(n_curr, d_curr, r_curr, iterations)
        results_abbrev = (n_curr, d_curr, r_curr, len(results_curr), sum(results_curr))
        results.append(results_abbrev)
        logging.info(f"MCMC iteration completed with results {results_abbrev}")

    # write results to csv
    with open(output_filepath, 'w', newline='') as csvfile:
        item_writer = csv.writer(csvfile, delimiter=",")
        item_writer.writerow(["nodes", "degree", "edge_size", "samples", "simple_samples"])
        item_writer.writerows(results)

    # finished! return results (never sure who wants them)
    return results


if __name__ == "__main__":
    # get user arguments
    parser = argparse.ArgumentParser("Run MCMC sampling to estimate proportion of H-simple bipartite graphs")
    parser.add_argument("-n", "--nodes", nargs='+', type=int, help="Comma-separated list of node counts[default = (%s)]")
    parser.add_argument("-d", "--degrees", nargs='+', type=int, help="Comma-separated list of (regular) degrees [default = (%s)]")
    parser.add_argument("-e", "--edges", nargs='+', type=int, help="Comma-separated list of (uniform) edge sizes [default = (%s)]")
    parser.add_argument("--iterations", type=int, help="Number of MCMC iterations [default = (%s)]", default=int(1e6))
    parser.add_argument("-o", "--output_directory", type=pathlib.Path, help="Driectory to save output in [default = (%s)]", default=pathlib.Path("output"))
    arguments = vars(parser.parse_args())

    # check argument validity
    if not arguments["output_directory"].is_dir():
        warnings.warn("Output directory does not exist; creating")
        arguments["output_directory"].mkdir(parents=True, exist_ok=True)
    arguments["output_filepath"] = arguments["output_directory"].joinpath("mcmc_results.csv")
    if arguments["output_filepath"].is_file():
        raise ValueError("Output filepath exists; stopping.")

    # set up logging
    logging.basicConfig(filename=arguments["output_directory"].joinpath("mcmc_log.txt"), level=logging.INFO)
    logging.info(str(arguments))

    # run specified function
    results = sample(n=arguments["nodes"], d=arguments["degrees"], r=arguments["edges"], iterations=arguments["iterations"], output_filepath=arguments["output_filepath"])