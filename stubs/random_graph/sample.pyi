import typing
from . import switch_bipartite_graph as switch_bipartite_graph

def sample_bipartite_graph(dx: typing.Sequence[int], dy: typing.Sequence[int], n_iter: int=...) -> typing.Set[typing.Tuple[int, int]]: ...
def sample_graph(d: typing.Sequence[int], n_iter: int=...) -> typing.Set[typing.Tuple[int, int]]: ...
