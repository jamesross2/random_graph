import typing
from . import switch_bipartite_graph as switch_bipartite_graph
from typing import Any

CallbackReturn: Any

class Chain:
    graph: Any = ...
    def __init__(self, graph: switch_bipartite_graph.SwitchBipartiteGraph) -> None: ...
    def mcmc(self, iterations: int=..., callback: typing.Optional[typing.Callable[[switch_bipartite_graph.SwitchBipartiteGraph], CallbackReturn]]=..., call_every: int=..., burn_in: int=...) -> typing.List[CallbackReturn]: ...
