import typing
from random_graph import switch_bipartite_graph as bipartite_graph
from typing import Any

CallbackReturn: Any

class Resampler:
    graph: Any = ...
    def __init__(self, graph: bipartite_graph.SwitchBipartiteGraph) -> None: ...
    def mcmc(
        self,
        iterations: int = ...,
        callback: typing.Optional[typing.Callable[[bipartite_graph.SwitchBipartiteGraph], CallbackReturn]] = ...,
        call_every: int = ...,
        burn_in: int = ...,
    ) -> typing.List[CallbackReturn]: ...
