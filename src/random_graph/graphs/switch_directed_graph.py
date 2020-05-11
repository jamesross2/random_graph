"""Directed Graph object.

In a directed graph, edges are tuples of vertices (as opposed to sets in the undirected case), and vertices have
separate 'in' and 'out' degrees.
"""

import copy
import itertools
import random
import typing

import random_graph.utils


class SwitchDirectedGraph(object):
    def __init__(self, n: int, edges: typing.Iterable[typing.Tuple[int, int]]) -> None:
        """A new directed graph with given nodes and in and out degrees.

        A directed graph has a vertex set X and an edge set E, where every element of E is an ordered pair of vertices
        from X. This implementation of the directed graph is optimised specifically for fast iteration of the switch
        chain, and may be slow for other uses.

        Args:
            n: The number of vertices in X
            edges: A sequence of edges (each edge consists of a pair of nodes)

        Raises:
            ValueError: if the given details are incompatible, for example if edges refer to non-existent nodes.
        """
        # check that arguments are valid
        edges = list(edges)
        if not random_graph.utils.valid_directed_graph(n, edges):
            raise ValueError("Provided arguments are not a valid directed graph.")

        # store edges in fast access, quick testing type
        self._n = n
        self._edges: typing.List[random_graph.utils.SampleSet] = [
            random_graph.utils.SampleSet() for _ in range(self._n)
        ]
        for x, y in edges:
            self._edges[x].add(y)

        # store the degree sequence information (inefficient, but run once only)
        out_degrees: typing.Tuple[int] = tuple(len(self._edges[n]) for n in range(self._n))
        in_degrees: typing.Tuple[int] = tuple(int(sum(y == node for (x, y) in self.edges)) for node in range(self._n))
        self._degree_sequence: typing.Tuple[typing.Tuple[int, int]] = tuple(zip(out_degrees, in_degrees))
        self._cumulative_degree_out: typing.Tuple[int] = tuple(itertools.accumulate(out_degrees))

    @property
    def n(self):
        return self._n

    @property
    def edges(self) -> typing.Iterator[typing.Tuple[int, int]]:
        """Set of edges contained in the directed graph.

        Returns:
            A set with one (x, y) pair for each edge.
        """
        return ((x, y) for x in range(self._n) for y in self._edges[x])

    @property
    def degree_sequence(self) -> typing.Tuple[typing.Tuple[int, int]]:
        """The degree sequence is the number of edges connected to each vertex.

        Returns:
            An iterator with (in degree, out degree) pairs
        """
        return copy.deepcopy(self._degree_sequence)

    @staticmethod
    def from_degree_sequence(degree_sequence: typing.Sequence[typing.Tuple[int, int]]) -> "SwitchDirectedGraph":
        """Create a non-random directed graph with the given degree sequence.

        This implements the Kleitman-Wang algorithm for construction a directed graph with the given degree sequence.
        It is greedy and non-random, so does not satisfy the requirements of a random graph, but can be used as the
        starting state for a switch Markov chain.

        Args:
            degree_sequence: Directed degree sequence for vertices in X, in the form of (int degree, out degree) pairs.

        Returns:
            A directed graph with the given degree sequence.

        Raises:
            ValueError: If the provided degree sequence is not graphical.

        References:
            D.J. Kleitman and D.L. Wang Algorithms for Constructing Graphs and Digraphs with Given Valences and Factors,
                Discrete Mathematics, 6(1), pp. 79-88 (1973).
        """
        # argument checks
        if not random_graph.utils.directed_degree_sequence_graphical(degree_sequence):
            raise ValueError("Degree sequence is not graphical.")

        if len(degree_sequence) == 0:
            return SwitchDirectedGraph(n=len(degree_sequence), edges=set())

        # store the number of stubs remaining on each vertex by decreasing (out stubs, in stubs, vertex label) triplets
        sxy = sorted([[sout, sin, vn] for vn, (sout, sin) in enumerate(degree_sequence)], reverse=True)

        # use greedy algorithm according to Kleitman-Wang
        edges = set()
        while max(s[1] for s in sxy) > 0:
            # choose destination vertex y from degrees sorted by remaining out degree
            ks = [k for k in range(len(sxy)) if sxy[k][1] > 0]
            _, sin, vto = sxy[ks[0]]
            sxy[ks[0]][1] = 0

            # add edges (vfrom, vto) sorted by remaining in stubs
            n = 0
            for _ in range(sin):
                _, _, vfrom = sxy[n]
                if vfrom == vto:
                    n += 1
                    _, _, vfrom = sxy[n]
                edges.add((vfrom, vto))
                sxy[n][0] -= 1
                n += 1

            # re-sort triplets
            sxy = sorted(sxy, reverse=True)

        # convert to graph
        graph = SwitchDirectedGraph(n=len(degree_sequence), edges=edges)
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
        return f"Switch Directed Graph with n={self._n}, directed degrees=({degrees})"

    def switch(self) -> bool:
        """Mutates the current directed graph by swapping pairs of edges, without impacting the degree sequence.

        A switch is a general term for a small change in the structure of a graph, achieved by swapping small numbers
        of edges. Switches can take general forms, but this is one of the most basic and common switches.

        Returns:
            If a switch was performed, then return True. If the switch was rejected, then return False.
                Switches are commonly rejected because they would create a duplicate edge or loop.
        """
        # sample edges to switch using index for faster deletion
        x1, x2 = random.choices(range(self._n), cum_weights=self._cumulative_degree_out, k=2)
        y1, y2 = random.choice(self._edges[x1]), random.choice(self._edges[x2])

        if y1 in self._edges[x2] or y2 in self._edges[x1]:
            # no switch applied if it would create a duplicate edge
            return False

        # apply the switch
        self._edges[x1].replace(old=y1, new=y2, check=False)
        self._edges[x2].replace(old=y2, new=y1, check=False)

        return True
