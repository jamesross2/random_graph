import typing
from . import sample_set as sample_set, utils as utils
from typing import Any

class SwitchBipartiteGraph:
    neighborhoods: Any = ...
    def __init__(self, nx: int, ny: int, edges: typing.Iterable[typing.Tuple[int, int]]) -> None: ...
    @property
    def nx(self): ...
    @property
    def ny(self): ...
    @property
    def edges(self) -> typing.Set[typing.Tuple[int, int]]: ...
    @property
    def degree_sequence(self) -> typing.Dict[str, typing.Tuple[int]]: ...
    def simple(self) -> bool: ...
    def __eq__(self, other: Any) -> Any: ...
    def neighbourhoods(self, side: str) -> typing.List[typing.Set[int]]: ...
    def switch(self) -> bool: ...