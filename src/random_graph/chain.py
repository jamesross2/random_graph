"""Markov Chain Monte Carlo resampler for a given bipartite graph."""

import typing

import tqdm

from . import graphs

CallbackReturn = typing.TypeVar("CallbackReturn")


class Chain(object):
    def __init__(self, graph: graphs.SwitchBipartiteGraph) -> None:
        """Initialise a Markov Chain Monte Carlo (MCMC) resampler for a given graph.

        Args:
            graph: A graph against which the mutations will be applied.
        """
        self.graph = graph

    def mcmc(
        self,
        iterations: int = int(1e4),
        callback: typing.Optional[typing.Callable[[graphs.SwitchBipartiteGraph], CallbackReturn]] = None,
        call_every: int = 100,
        burn_in: int = 500,
        verbose: bool = True,
    ) -> typing.List[CallbackReturn]:
        """Run MCMC resampling on the Resampler graph, using the switch method of the graph directly.

        Args:
            iterations: Number of MCMC steps to take. This should be chosen to increase as the size of the provided
                graph increases.
            callback: A function called for its side effects. Should accept the current graph as its only input.
            call_every: Number of iterations to run before using the callback function. This will only be called after
                completing the burn in iterations, and then on iteration numbers which are a multiple of the call_every
                parameter.
            burn_in: Number of iterations to run before calling the callback function.
            verbose: If True (the default), then use a progress bar to show progress.

        Returns:
            A list of values returned by the callback function. This may be meaningless, if the provided callback
                function stores its own results.
        """
        history = []
        iters = range(iterations + burn_in)
        if verbose:
            iters = tqdm.tqdm(list(iters), leave=False)
        for iteration in iters:
            # run the basic switch
            self.graph.switch()
            if callback is not None and iteration >= burn_in and (iteration + 1) % call_every == 0:
                history.append(callback(self.graph))

        return history
