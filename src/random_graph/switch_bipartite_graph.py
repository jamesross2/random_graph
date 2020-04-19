"""Bipartite Graph objects.

Bipartite graphs can be used to represent hypergraphs (and multihypergraphs, more generally), and can
be more convenient computationally to work with,
"""

import copy
import random
import typing

import random_graph.utils


class SwitchBipartiteGraph(object):
    def __init__(self, nx: int, ny: int, edges: typing.Iterable[typing.Tuple[int, int]]) -> None:
        """A new bipartite graph with given nodes and degrees.

        A bipartite graph has a vertex set consisting of disjoint subsets X and Y, such that all edges are between
        one node in X and one node in Y. Note that this implementation is designed specifically for fast mutation
        using a switch chain.

        Args:
            nx: If an integer, constructs this many empty nodes. If a sequence of nodes, uses the nodes
            ny: If an integer, constructs this many empty nodes. If a sequence of nodes, uses the nodes
            edges: A sequence of edges (each edge consists of a pair of nodes)

        Raises:
            ValueError: if the given details are incompatible, for example if edges refer to non-existent nodes.

        References:
            Miklós, I., Erdős, P. L., & Soukup, L. (2013). Towards Random Uniform Sampling of Bipartite Graphs with
                given Degree Sequence. The Electronic Journal of Combinatorics, 20(1), P16.
            Greenhill, C. (2015, January). The switch Markov chain for sampling irregular graphs. In Proceedings of the
                twenty-sixth annual ACM-SIAM symposium on Discrete algorithms (pp. 1564-1572).
        """
        # check that arguments are valid
        edges = list(edges)
        if not random_graph.utils.valid_bipartite_graph(nx, ny, edges):
            raise ValueError("Provided arguments are not a valid bipartite graph.")

        # store edges in fast access, quick testing type
        self._nx = nx
        self._ny = ny
        self._edges: typing.List[random_graph.utils.SampleSet] = [
            random_graph.utils.SampleSet() for _ in range(self._nx)
        ]
        for x, y in edges:
            self._edges[x].add(y)

        # store the degree sequence
        self._degree_sequence: typing.Dict[str, typing.Tuple[int]] = {
            "x": tuple(len(self._edges[n]) for n in range(self._nx)),
            "y": tuple(int(sum(edge[1] == node for edge in self.edges)) for node in range(self._ny)),
        }

        # aliases: satisfy the yanks
        self.neighborhoods = self.neighbourhoods

    @property
    def nx(self):
        return self._nx

    @property
    def ny(self):
        return self._ny

    @property
    def edges(self) -> typing.Set[typing.Tuple[int, int]]:
        """Set of edges contained in the bipartite graph.

        Returns:
            A set with one (x, y) pair for each edge.
        """
        return {(x, y) for x in range(self._nx) for y in self._edges[x]}

    @property
    def degree_sequence(self) -> typing.Dict[str, typing.Tuple[int]]:
        """The degree sequence is the number of edges connected to each vertex.

        Returns:
            A dictionary, with 'x' and 'y' keys, each containing a degree sequence.
        """
        return copy.deepcopy(self._degree_sequence)

    @staticmethod
    def from_degree_sequence(dx: typing.Sequence[int], dy: typing.Sequence[int]) -> "SwitchBipartiteGraph":
        """Create a non-random bipartite graph with the given degree sequence.

        This is a basic extension of the Havel-Hakimi algorithm (for constructing simple graphs), which uses the Gale-
        Ryser theorem to construct simple bipartite graphs. The result is a non-random bipartite graph. To sample a 
        bipartite graph approximately uniformly at random, the switch chain can be applied, which is often rapidly 
        converging.
        
        Args:
            dx: Degree sequence for vertices in X.
            dy: Degree sequence for vertices in Y.

        Returns:
            A bipartite graph with the given degree sequence.

        Raises:
            ValueError: If the provided degree sequence is not graphical.
        """
        # argument checks
        if not random_graph.utils.degree_sequence_graphical(dx, dy):
            raise ValueError("Degree sequence is not graphical.")

        # store the number of stubs remaining on each vertex in X and Y
        # sorting guarantees order from largest to smallest
        sx = sorted(([d, x] for x, d in enumerate(dx)), reverse=True)
        sy = sorted(([d, y] for y, d in enumerate(dy)), reverse=True)

        # use greedy algorithm akin to Havel Hakimi
        edges = set()
        for d, x in sx:
            # get Y vertices to attach to current X vertex
            for n in range(d):
                edges.add((x, sy[n][1]))
                sy[n][0] -= 1

            # update Y stubs
            sy = sorted(sy, reverse=True)

        # convert to graph
        graph = SwitchBipartiteGraph(nx=len(dx), ny=len(dy), edges=edges)
        return graph

    def simple(self) -> bool:
        """Test whether the bipartite graph is H-simple.

        A bipartite graph is H-simple bipartite if no two nodes from Y have the same neighbourhood in X. Equivalently,
        a bipartite graph is H-simple if and only if it represents a simple hypergraph.

        Returns:
            True if the current bipartite graph is H-simple, False otherwise.
        """
        return random_graph.utils.all_unique(tuple(neighbourhood) for neighbourhood in self.neighbourhoods(side="y"))

    def __eq__(self, other):
        # check degree sequence simply for speed
        # computing edges is relatively expensive (without referring to self._edge)
        return (
            self.nx == other.nx
            and self.ny == other.ny
            and self.degree_sequence == other.degree_sequence
            and self.edges == other.edges
        )

    def __str__(self):
        if self.nx > 10:
            degrees = [str(d) for d in self._degree_sequence["x"][:9]] + ["..."]
        else:
            degrees = [str(d) for d in self._degree_sequence["x"]]
        degrees = ", ".join(degrees)
        return f"Bipartite Graph with nx={self._nx}, ny={self._ny}, X degrees=({degrees})"

    def neighbourhoods(self, side: str) -> typing.List[typing.Set[int]]:
        """Get the neighbourhoods of all nodes.

        Args:
            side: Either "x" or "y". Determines which set of neighbourhoods will be returned.

        Returns:
            A list of neighbourhoods, where each neighbourhood is a set of vertex indices (from the partition opposite
                to the one indicated by side).

        Raises:
            ValueError: If a side other than "x" or "y" is given.
        """
        if side == "x":
            return list(set(self._edges[node].items) for node in range(self._nx))
        elif side == "y":
            neighbourhoods = [set() for _ in range(self._ny)]
            for x, neighbours in enumerate(self._edges):
                for y in neighbours:
                    neighbourhoods[y].add(x)
            return neighbourhoods
        else:
            raise ValueError(f"Side must be 'x' or 'y'; given option {side} not recognised.")

    def switch(self) -> bool:
        """Mutates the current hypergraph by swapping pairs of edges, without impacting the degree sequence.

        A switch is a general term for a small change in the structure of a graph, achieved by swapping small numbers
        of edges. Switches can take general forms,

        Returns:
            bool: If a switch was performed, then return True. If the switch was rejected, then return False.
                Switches are commonly rejected because they would create a duplicate edge.
        """
        # sample edges to switch using index for faster deletion
        x1, x2 = random.choices(range(self._nx), weights=self._degree_sequence["x"], k=2)
        y1, y2 = random.choice(self._edges[x1]), random.choice(self._edges[x2])

        if y1 in self._edges[x2] or y2 in self._edges[x1]:
            # no switch applied if it would create a duplicate edge
            return False

        # apply the switch
        self._edges[x1].replace(old=y1, new=y2, check=False)
        self._edges[x2].replace(old=y2, new=y1, check=False)

        return True
