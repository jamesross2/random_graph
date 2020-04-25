#!/usr/bin/env python3
"""Run an MCMC chain over a range of regular degree sequences to estimate H-simple likelihoods."""
import argparse
import typing
import random_graph
import warnings
import itertools
import csv
import pathlib
import tqdm
import logging


def parse_arguments() -> typing.Dict[str, typing.Any]:
    # get user arguments
    parser = argparse.ArgumentParser("Run MCMC sampling to estimate proportion of H-simple bipartite graphs")
    parser.add_argument(
        "-n", nargs="+", type=int, help="Comma-separated list of orders [default (%s)]", required=True
    )
    parser.add_argument(
        "-d",
        nargs="+",
        type=int,
        help="Comma-separated list of (regular) degrees [default (%s)]",
        required=True,
    )
    parser.add_argument(
        "-r",
        nargs="+",
        type=int,
        help="Comma-separated list of (uniform) edge sizes [default (%s)]",
        required=True,
    )
    parser.add_argument("--iterations", type=int, help="Number of MCMC iterations [default (%s)]", default=int(1e6))
    parser.add_argument(
        "-o",
        "--output_directory",
        type=pathlib.Path,
        help="Directory to save output in [default (%s)]",
        default=pathlib.Path("output"),
    )

    arguments = vars(parser.parse_args())
    return arguments


def mcmc(n: int, d: int, r: int, iterations: int) -> typing.Sequence[bool]:
    """Run MCMC sampling on a provided graph to test for simple-ness"""
    try:
        graph = random_graph.graphs.SwitchBipartiteGraph.from_degree_sequence([d] * n, [r] * ((n * d) // r))
    except ValueError:
        warnings.warn(f"No graph with n={n}, d={d}, r={r}.")
        return []
    resampler = random_graph.Chain(graph)
    history = resampler.mcmc(iterations=iterations, callback=lambda g: g.simple(), call_every=100, burn_in=int(1e4))
    return history


def sample(
    n: typing.Sequence[int],
    d: typing.Sequence[int],
    r: typing.Sequence[int],
    iterations: int,
    output_filepath: typing.Union[str, pathlib.Path],
):
    results = []
    for n_curr, d_curr, r_curr in tqdm.tqdm(list(itertools.product(n, d, r)), desc="parameters", leave=True):
        results_curr = mcmc(n_curr, d_curr, r_curr, iterations)
        results_abbrev = (n_curr, d_curr, r_curr, len(results_curr), sum(results_curr))
        results.append(results_abbrev)
        logging.info(f"MCMC iteration completed with results {results_abbrev}")

    # write results to csv
    with open(output_filepath, "w", newline="") as csvfile:
        item_writer = csv.writer(csvfile, delimiter=",")
        item_writer.writerow(["nodes", "degree", "edge_size", "samples", "simple_samples"])
        item_writer.writerows(results)

    # finished! return results (never sure who wants them)
    return results


def main():
    arguments = parse_arguments()

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
    results = sample(
        n=arguments["n"],
        d=arguments["d"],
        r=arguments["r"],
        iterations=arguments["iterations"],
        output_filepath=arguments["output_filepath"],
    )
    return results


if __name__ == "__main__":
    results = main()
