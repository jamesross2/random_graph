"""Approximate uniform sampling for graphs with given degree sequence.

This is a lightweight and fast package for sampling graphs (of various
types) with a given degree sequence. Other models for sampling random
graphs such as the Erdos-Renyi random graph model, the Barabási–Albert
model or the Watts and Strogatz model, all sample graphs from families
with a range of degree sequences. By contrast, this package samples
graphs with a prescribed degree sequence.

The sampling scheme uses a
switch chain to sample bipartite graphs approximately uniformly at
random. This works by initialising the chain with a non-random starting
state (a graph created using something like the Havel-Hakimi algorithm,
or an analogue for other graph types). The chain then applies a number
of 'switches', each of which swaps the endpoints of a pair of edges. As
long as switches that produce non-simple properties (such as multiple
edges or loops) are rejected, the result is another graph from the same
class and with the same degree sequence as the original. Applying the
switches iteratively results in a Markov chain that is reversible and
has the uniform distribution as its stationary distribution. Hence,
after sufficiently many switches (Markov chain transitions), the result
is a graph sampled approximately uniformly. Moreover, the chain is
rapidly converging for a wide range of degree sequences (so that the
total variation distance between the uniform distribution and the
sampling distribution approaches epsilon in time O(log(n) * log(1 /
epsilon)).

For basic usage, we recommend using the sample_* family of
functions, which return the edges of a graph with the desired degree
sequence. For more advanced usage, users can initialise their own graph
object, and apply switches manually. We note that all graph classes have
been optimised for the switch chain in particular, and are probably
unsuited for other operations. For users who wish to analyse the
resulting graphs further, we highly recommend the networkx package.
"""

from . import graphs, toolbox
from .chain import Chain
from .sample import sample_bipartite_graph, sample_directed_graph, sample_multi_hypergraph, sample_simple_graph
