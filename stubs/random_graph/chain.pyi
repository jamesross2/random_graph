import typing
from . import graphs as graphs
from typing import Any

CallbackReturn: Any

class Chain:
    graph: Any = ...
    def __init__(self, graph: graphs.SwitchBipartiteGraph) -> None: ...
    def mcmc(self, iterations: int=..., callback: typing.Optional[typing.Callable[[graphs.SwitchBipartiteGraph], CallbackReturn]]=..., call_every: int=..., burn_in: int=..., verbose: bool=...) -> typing.List[CallbackReturn]: ...
