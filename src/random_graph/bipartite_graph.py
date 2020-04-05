"""Bipartite Graph objects.

Bipartite graphs can be used to represent hypergraphs (and multihypergraphs, more generally), and can
be more convenient computationally to work with,
"""

import collections
import random
import typing

import numpy

NodeType = typing.TypeVar("NodeType", int, str)


class SwitchBipartiteGraph(object):
    def __init__(
        self,
        nodes_x: typing.Union[int, typing.List[NodeType]],
        nodes_y: typing.Union[int, typing.List[NodeType]],
        edges: typing.Sequence[typing.Tuple[NodeType, NodeType]],
    ) -> None:
        """A new bipartite graph with given nodes and degrees.

        A bipartite graph has a vertex set consisting of disjoint subsets X and Y, such that all edges are between
        one node in X and one node in Y. Note that this implementation is designed specifically for fast mutation
        using a switch chain.

        Args:
            nodes_x: If an integer, constructs this many empty nodes. If a sequence of nodes, uses the nodes
            nodes_y: If an integer, constructs this many empty nodes. If a sequence of nodes, uses the nodes
            edges: A sequence of edges (each edge consists of a pair of nodes)

        Raises:
            ValueError: if the given details are incompatible, for example if edges refer to non-existent nodes.

        References:
            TODO: A switch chain for... CGreenhill et al
            TODO: Kannan Tetali Vempala
        """
        # create degree information
        self.nodes: typing.Dict[str, typing.List[NodeType]] = {}
        for nodes, node_name in zip((nodes_x, nodes_y), ("x", "y")):
            if isinstance(nodes, int):
                node_values = list(range(nodes))
            else:
                node_values = nodes
            self.nodes[node_name] = node_values

        # check that edges are valid
        edges = list(edges)
        if len(set(edges)) < len(edges):
            raise ValueError("Not all edges are unique.")
        edges_valid_nodes = [edge[0] in self.nodes["x"] and edge[1] in self.nodes["y"] for edge in edges]
        if not all(edges_valid_nodes):
            bad_indices = numpy.where(not valid for valid in edges_valid_nodes)
            bad_edge = edges[bad_indices[0][0]]
            raise ValueError(f"Provided edge {bad_edge} does not appear in nodes.")

        # store edges in prescribed format
        self.edges = [tuple(edge) for edge in edges]

    @property
    def order(self):
        """Number of vertices in X.

        Returns:
            An integer for the number of vertices.
        """
        return len(self.nodes["x"])

    @property
    def m(self):
        """Number of edges in bipartite graph.

        Returns:
            An integer for the number of edges.
        """
        return len(self.edges)

    @property
    def simple(self) -> bool:
        """Test whether the bipartite graph is H-simple.

        A bipartite graph is H-simple bipartite if no two nodes from Y have the same neighbourhood in X. Equivalently,
        a bipartite graph is H-simple if and only if it represents a simple hypergraph.

        Returns:
            True if the current bipartite graph is H-simple, False otherwise.
        """
        neighbourhoods: typing.Dict[str, typing.List[typing.List[NodeType]]] = self.neighbourhoods()
        hyperedges = len(self.nodes["y"])
        unique_hyperedges = len(set(tuple(sorted(nhood)) for nhood in (neighbourhoods["y"])))
        return hyperedges == unique_hyperedges

    def __eq__(self, other):
        return self.nodes == other.nodes and sorted(self.edges) == sorted(other.edges)

    def neighbourhoods(self) -> typing.Dict[str, typing.List[typing.List[NodeType]]]:
        """Get the neighbourhoods of all nodes.

        Returns:
            A dictionary with the same structure as self.nodes, with lists containing the neighbourhoods of each vertex.
        """
        neighbourhoods: typing.Dict[str, typing.List[typing.List[NodeType]]]
        neighbourhoods = {
            "x": [[] for _ in range(len(self.nodes["x"]))],
            "y": [[] for _ in range(len(self.nodes["y"]))],
        }
        for edge in self.edges:
            neighbourhoods["x"][edge[0]].append(edge[1])
            neighbourhoods["y"][edge[1]].append(edge[0])

        return neighbourhoods

    def remove_edge(
        self, edge: typing.Optional[typing.Tuple[NodeType, NodeType]] = None, index: typing.Optional[int] = None,
    ) -> None:
        """Remove an edge from the current graph.

        Either the edge or the index must be provided. If both are provided, then only the index will be used, and
        the edge will be ignored (silently).

        Args:
            edge: the edge to be removed.
            index: the index of the edge to be removed.

        Raises:
            ValueError: if neither the edge nor the index is given.
        """
        if index is not None:
            self.edges.pop(index)
        elif edge is not None:
            self.edges.remove(edge)
        else:
            raise ValueError("Either edge or index must be provided.")

    def add_edge(self, edge: typing.Tuple[NodeType, NodeType], test: bool = True) -> None:
        """Add an edge to the current graph.

        Args:
            edge: The edge to be added.
            test: Set to False to skip validity checking; only advised for optimisation.

        Raises:
            ValueError: if the edge cannot be inserted, or is impossible. Skipped if `test` parameter is False.
        """
        # check that edge is valid
        if test:
            if edge in self.edges:
                raise ValueError("Cannot insert duplicate edge.")
            if edge[0] not in self.nodes["x"] or edge[1] not in self.nodes["y"]:
                raise ValueError(f"Provided edge {edge} does not appear in nodes.")

        self.edges.append(tuple(edge))

    def switch(self) -> bool:
        """Mutates the current hypergraph by swapping pairs of edges, without impacting the degree sequence.

        A switch is a general term for a small change in the structure of a graph, achieved by swapping small numbers
        of edges. Switches can take general forms,

        Returns:
            bool: If a switch was performed, then return True. If the switch was rejected, then return False.
                Switches are commonly rejected because they would create a duplicate edge.
        """
        # sample edges to switch using index for faster deletion
        i0, i1 = random.choices(range(self.m), k=2)
        edges_in = [
            (self.edges[i1][0], self.edges[i0][1]),
            (self.edges[i0][0], self.edges[i1][1]),
        ]

        # check that edges can be put into graph
        if any(edge in self.edges for edge in edges_in):
            # duplicate edges disallowed; do not mutate
            return False

        # be sure to remove edges so that index is unaffected
        for index in sorted((i0, i1), reverse=True):
            self.remove_edge(index=index)
        for edge in edges_in:
            self.add_edge(edge=edge, test=False)

        return True
