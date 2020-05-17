"""Switch simple graph object.

In a simple graph, edges are sets of pairs of vertices.
"""

import copy
import itertools
import random
import typing

import random_graph.utils


class SwitchSimpleGraph(object):
    def __init__(self, n: int, edges: typing.Iterable[typing.Set[int]]) -> None:
        """A new simple graph with given nodes and in and out degrees.

        A simple graph has a vertex set X and an edge set E, where every element of E is a set of two vertices from X.
        This implementation is optimised specifically for fast iteration of the switch chain, and may be slow for other
        uses.

        Args:
            n: The number of vertices in X.
            edges: A sequence of edges (each edge consists of a set of two nodes).

        Raises:
            ValueError: if the given details are incompatible, for example if edges refer to non-existent nodes.
        """
        # check that arguments are valid
        edges = list(edges)
        if not random_graph.utils.valid_simple_graph(n, edges):
            raise ValueError("Provided arguments are not a valid simple graph.")

        # store edges in fast access, quick testing type
        self._n = n
        self._edges: typing.List[random_graph.utils.SampleSet] = [
            random_graph.utils.SampleSet() for _ in range(self._n)
        ]
        for x, y in edges:
            self._edges[x].add(y)
            self._edges[y].add(x)

        # store the degree sequence information (inefficient, but run once only)
        self._degree_sequence: typing.Tuple[int] = tuple(len(edges) for edges in self._edges)
        self._cumulative_degree_out: typing.Tuple[int] = tuple(itertools.accumulate(self._degree_sequence))

    @property
    def n(self):
        return self._n

    @property
    def edges(self) -> typing.Iterator[typing.Set[int]]:
        """Edges contained in the directed graph.

        Returns:
            An iterator of {x, y} sets for each edge.
        """
        return ({x, y} for x in range(self._n) for y in self._edges[x] if x < y)

    @property
    def degree_sequence(self) -> typing.Tuple[int]:
        """The degree sequence is the number of edges connected to each vertex.

        Returns:
            A tuple of the degree sequence
        """
        return copy.deepcopy(self._degree_sequence)

    @staticmethod
    def from_degree_sequence(degree_sequence: typing.Sequence[int]) -> "SwitchSimpleGraph":
        """Create a non-random simple graph with the given degree sequence.

        This implements a Havel-Hakimi style algorithm to produce a graph with the given degree sequence. It is greedy
        and non-random, so does not satisyf the requirements of a random graph, but can be used as the starting state
        for a switch Markov chain.

        Args:
            degree_sequence: Degree sequence for vertices in X.

        Returns:
            A simple graph with the given degree sequence.

        Raises:
            ValueError: If the provided degree sequence is not graphical.
        """
        # argument checks
        if not random_graph.utils.simple_degree_sequence_graphical(degree_sequence):
            raise ValueError("Degree sequence is not graphical.")

        if len(degree_sequence) == 0:
            return SwitchSimpleGraph(n=len(degree_sequence), edges=[])

        # store the number of stubs remaining on each vertex in X and Y
        # sorting guarantees order from largest to smallest
        stubs = sorted(([d, x] for x, d in enumerate(degree_sequence)), reverse=True)

        # use greedy Havel-Hakimi algorithm
        edges: typing.List[typing.Set[int]] = []
        while 2 * len(edges) < sum(degree_sequence):
            d, x = stubs[0]
            # get Y vertices to attach to current X vertex
            for n in range(1, d + 1):
                edges.append({x, stubs[n][1]})
                stubs[n][0] -= 1
                stubs[0][0] -= 1
            # update Y stubs
            stubs = sorted(stubs, reverse=True)

        # convert to graph
        graph = SwitchSimpleGraph(n=len(degree_sequence), edges=edges)
        return graph

    def __eq__(self, other):
        # check degree sequence simply for speed
        # computing edges is relatively expensive (without referring to self._edge)
        return (
            self.n == other.n
            and self.degree_sequence == other.degree_sequence
            and list(self.edges) == list(other.edges)
        )

    def __str__(self):
        if self.n > 10:
            degrees = [str(d) for d in self._degree_sequence[:9]] + ["..."]
        else:
            degrees = [str(d) for d in self._degree_sequence]
        degrees = ", ".join(degrees)
        return f"Switch Simple Graph with n={self._n}, degrees=({degrees})"

    def switch(self) -> bool:
        """Mutates the current graph by swapping pairs of edges, without impacting the degree sequence.

        A switch is a general term for a small change in the structure of a graph, achieved by swapping small numbers
        of edges. Switches can take general forms, but this is one of the most basic and common switches.

        Returns:
            If a switch was performed, then return True. If the switch was rejected, then return False.
                Switches are commonly rejected because they would create a duplicate edge or loop.
        """
        # sample edges to switch using index for faster deletion
        x1, x2 = random.choices(range(self._n), cum_weights=self._cumulative_degree_out, k=2)
        y1, y2 = random.choice(self._edges[x1]), random.choice(self._edges[x2])

        # fail case 1: chosen edges intersect
        if {x1, y1}.intersection({x2, y2}) != set():
            # no switch applied if it would create a duplicate edge
            return False

        # fail case 2: chosen edges would produce a multiple edge
        if y2 in self._edges[x1] or y1 in self._edges[x2]:
            return False

        # apply the switch
        self._edges[x1].replace(old=y1, new=y2, check=False)
        self._edges[x2].replace(old=y2, new=y1, check=False)
        self._edges[y1].replace(old=x1, new=x2, check=False)
        self._edges[y2].replace(old=x2, new=x1, check=False)

        return True
