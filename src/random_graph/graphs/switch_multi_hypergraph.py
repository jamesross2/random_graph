"""Multi Hypergraph object.

In a hypergraph, edges are sets of vertices where each set may have size greater than 2. It has a degree sequence
(the number of edges connected to a vertex), but also an edge size sequence (the number of vertices contained within
each edge). This can be canonically represented using a bipartite graph, which is the approach that we use here.

A typical hypergraph has an edge set, but the canonical representation allows for multiple edges. Hence, we use the
multi-hypergraph object, which permits multiple edges.
"""

import copy
import itertools
import random
import typing

import random_graph.graphs
import random_graph.utils


class SwitchMultiHypergraph(object):
    def __init__(self, n: int, edges: typing.Iterable[typing.Set[int]]) -> None:
        """A new multi-hypergraph with given edges.

        A multi-hypergraph has a vertex set X and an edge set E, where very element of E is a set of vertices from X.
        This implementation of the multi-hypergraph is optimised specifically for fast iteration of the switch chain,
        and may be slow for other uses.

        Args:
            n: The number of vertices in X.
            edges: A sequence of edges (each edge consists of a subset of vertices).

        Raises:
            ValueError: if the given details are incompatible, for example if edges refer to non-existent nodes.
        """
        # check that arguments are valid
        edges = list(edges)
        if not random_graph.utils.valid_multi_hypergraph(n, edges):
            raise ValueError("Provided arguments are not a valid multi-hypergraph.")

        # store edges in fast access, quick testing type
        self._n = n
        self._m = len(edges)
        self._edges: typing.List[random_graph.utils.SampleSet] = [
            random_graph.utils.SampleSet() for _ in range(self._n)
        ]
        self._neighbourhoods: typing.List[random_graph.utils.SampleSet] = [
            random_graph.utils.SampleSet() for _ in range(self._m)
        ]
        for y, edge in enumerate(edges):
            for x in edge:
                self._edges[x].add(y)
                self._neighbourhoods[y].add(x)

        # store the degree sequence information (inefficient, but run once only)
        self._degree_sequence: typing.Tuple[int] = tuple(len(self._edges[n]) for n in range(self._n))
        self._edge_sizes: typing.Tuple[int] = tuple(len(self._neighbourhoods[n]) for n in range(self._m))
        self._cumulative_degrees: typing.Tuple[int] = tuple(itertools.accumulate(self._degree_sequence))

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m

    @property
    def edges(self) -> typing.Iterator[typing.Set[int]]:
        """Set of edges contained in the multi-hypergraph.

        Returns:
            An iterable of edges, each of which is a set of vertices with size given by self.edge_sizes.
        """
        return (set(self._neighbourhoods[x]) for x in range(self._m))

    @property
    def degree_sequence(self) -> typing.Tuple[int]:
        """The degree sequence is the number of edges connected to each vertex.

        Returns:
            The degree sequence.
        """
        return copy.deepcopy(self._degree_sequence)

    @property
    def edge_sizes(self) -> typing.Tuple[int]:
        """The edge sizes are the number of vertices within each edge.

        Returns:
            The edge sizes sequence.
        """
        return copy.deepcopy(self._edge_sizes)

    @staticmethod
    def from_degree_sequence(
        degree_sequence: typing.Sequence[int], edge_sequence: typing.Sequence[int]
    ) -> "SwitchMultiHypergraph":
        """Create a non-random multi-hypergraph with the given degree sequence.

        This instantiates a bipartite graph, using the degree sequence and edge sequence as the bipartite degree
        sequence. The result is a non-random multi-hypergraph graph. To sample a multi-hypergraph approximately
        uniformly at random, the switch chain can be applied, which is often rapidly converging.

        Args:
            degree_sequence: Degree sequence for vertices in X.
            edge_sequence: Sequence of edge sizes.

        Returns:
            A multi-hypergraph with the given degree sequence and edge sequence.

        Raises:
            ValueError: If the provided sequences are not graphical.
        """
        # argument checks
        if not random_graph.utils.bipartite_degree_sequence_graphical(degree_sequence, edge_sequence):
            raise ValueError("Degree sequence is not graphical.")

        # empty hypergraph returned immediately
        if len(degree_sequence) == 0:
            return SwitchMultiHypergraph(n=len(degree_sequence), edges=set())

        # use bipartite construction to create the multi-hypergraph
        bipartite_graph = random_graph.graphs.SwitchBipartiteGraph.from_degree_sequence(degree_sequence, edge_sequence)
        hypergraph_edges = bipartite_graph.neighborhoods("y")

        # convert to graph
        graph = SwitchMultiHypergraph(n=len(degree_sequence), edges=hypergraph_edges)
        return graph

    def to_bipartite_graph(self, shuffle_edges: bool = True) -> "SwitchBipartiteGraph":
        """Converts the current hypergraph object into a bipartite graph via canonical realisation.

        This chooses a labelling for the edges of the hypergraph, and uses this to create the associated
        bipartite graph. Note that because edges in the hypergraph are unlabelled (unlike the vertices in the bipartite
        graph), this can result in different outputs. Hence, we include an argument to shuffle the edges. If edges
        are shuffled, the resulting labelling is effectively random; if this is set to false, the labelling is
        non-random (which is useful if results are required to be identical between runs).

        Args:
            shuffle_edges: If True (the default), a random labelling is used on the edges to convert them into vertices.
                If False, the edges are sorted first.

        Returns:
            A switch bipartite graph representing the given hypergraph.
        """
        # get edges in desired order (this determines labelling)
        hyperedges = list(self.edges)
        if shuffle_edges:
            random.shuffle(hyperedges)
        else:
            hyperedges = sorted(tuple(sorted(edge)) for edge in hyperedges)

        bipartite_edges = [(x, y) for y, edge in enumerate(hyperedges) for x in edge]
        bipartite_graph = random_graph.graphs.SwitchBipartiteGraph(nx=self.n, ny=self.m, edges=bipartite_edges)
        return bipartite_graph

    def __eq__(self, other):
        # check degree sequence simply for speed
        # computing edges is relatively expensive (without referring to self._edge)
        return (
            self.n == other.n
            and self.m == other.m
            and self.degree_sequence == other.degree_sequence
            and self.edge_sizes == other.edge_sizes
            and list(self.edges) == list(other.edges)
        )

    def __str__(self):
        if self.n > 10:
            degrees = [str(d) for d in self._degree_sequence[:9]] + ["..."]
        else:
            degrees = [str(d) for d in self._degree_sequence]

        if self.m > 10:
            edge_sizes = [str(d) for d in self._edge_sizes[:9]] + ["..."]
        else:
            edge_sizes = [str(d) for d in self._edge_sizes]

        degrees = ", ".join(degrees)
        edge_sizes = ", ".join(edge_sizes)
        return f"Switch Multi-Hypergraph with n={self._n}, degrees=({degrees}), edge sizes=({edge_sizes})"

    def simple(self) -> bool:
        """Test whether the multi-hypergraph graph is simple.

        A multi-hypergraph is simple if no two edges are the same.

        Returns:
            True if the current multi-hypergraph is simple, False otherwise.
        """
        return random_graph.utils.all_unique(tuple(sorted(neighbourhood)) for neighbourhood in self.edges)

    def switch(self) -> bool:
        """Mutates the current multi-hypergraph by swapping pairs of vertices within edges.

        A switch is a general term for a small change in the structure of a graph, achieved by swapping small numbers
        of edges. Switches can take general forms, but this is one of the most basic and common switches.

        Returns:
            If a switch was performed, then return True. If the switch was rejected, then return False.
                Switches are commonly rejected because they would create a duplicate edge or loop.
        """
        # sample edges to switch using index for faster deletion
        x1, x2 = random.choices(range(self._n), cum_weights=self._cumulative_degrees, k=2)
        y1, y2 = random.choice(self._edges[x1]), random.choice(self._edges[x2])

        if y1 in self._edges[x2] or y2 in self._edges[x1]:
            # no switch applied if it would create a duplicate edge
            return False

        # apply the switch
        self._edges[x1].replace(old=y1, new=y2, check=False)
        self._edges[x2].replace(old=y2, new=y1, check=False)
        self._neighbourhoods[y1].replace(old=x1, new=x2, check=False)
        self._neighbourhoods[y2].replace(old=x2, new=x1, check=False)

        return True
