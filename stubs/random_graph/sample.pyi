import typing
from . import graphs as graphs

def sample_bipartite_graph(dx: typing.Sequence[int], dy: typing.Sequence[int], n_iter: int=...) -> typing.List[typing.Tuple[int, int]]: ...
def sample_directed_graph(degree_sequence: typing.Sequence[typing.Tuple[int, int]], n_iter: int=...) -> typing.List[typing.Tuple[int, int]]: ...
def sample_multi_hypergraph(degree_sequence: typing.Sequence[int], edge_sequence: typing.Sequence[int], n_iter: int=...) -> typing.List[typing.Set[int]]: ...
def sample_simple_graph(degree_sequence: typing.Sequence[int], n_iter: int=...) -> typing.List[typing.Set[int]]: ...
