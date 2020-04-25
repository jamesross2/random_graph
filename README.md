# Random Bipartite Graphs with Given Degree Sequence

[![Build Status](https://img.shields.io/travis/jamesross2/random_graph/master?logo=travis&style=flat-square)](https://travis-ci.org/jamesross2/random_graph?style=flat-square)
[![Code Coverage](https://img.shields.io/codecov/c/github/jamesross2/random_graph?logo=codecov&style=flat-square&label=codecov)](https://codecov.io/gh/jamesross2/random_graph)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=black&style=flat-square)](https://github.com/psf/black)

This is a fast, lightweight, Python package for sampling random graphs. It is designed to generate graphs with a 
given degree sequence approximately uniformly at random. It does this for as quickly as possible, for as many degree 
sequences as possible. 


## Package highlights

The `random_graph` package is appropriate for sampling a random graph when a specific degree sequence is required. It is 
optimised for simplicity and speed, and efficiently scales to very large graphs. It presents a set of simple functions 
for standard usage, and more advanced functionality for advanced users.

The sampling algorithm itself is a non-trivial Markov Chain Monte Carlo process (naive sampling algorithms tend to have
exponential algorithmic complexity, and do not scale to even moderately sized problems). Given a degree sequence (or 
bipartite degree sequence), the sampling algorithm first creates a non-random graph with the given degree sequence 
(greedily, and deterministically). It then applies small random transformations ('switches') to the graph. After 
sufficiently many switches, the result is a new graph with the required degree sequence, sampled from the set of all 
possible graphs approximately uniformly at random (well, pseudo-random).

The implementation used here is space and time efficient. On a basic laptop CPU, this package can sample a random graph 
in under a second (it computes well over 100,000 switch operations per second), even for graphs with large numbers of 
nodes and edges. The algorithmic complexity of each iteration is constant relative to the number of edges in the graph, 
and the memory requirements grow linearly with the number of edges in the graph, allowing the package to efficiently 
scale to very large graphs.

 For users wishing to sample graphs 
_without_ any restriction on degree sequence (such as Erdős–Rényi sampling), the very helpful 
[`NetworkX`](https://github.com/networkx/networkx) package is one of many excellent alternatives. We also recommend the 
`NetworkX` package for users wishing to further manipulate the randomly sampled graph.


## Usage

This package has been optimised specifically for the purpose of sampling graphs via the switch chain; for other 
requirements we recommend the [`NetworkX`](https://github.com/networkx/networkx) package. The convenient top-level 
functions of the package are `sample_graph` and `sample_bipartite_graph`, with the graph objects themselves placed into
a submodule (to maintain the simplicity of the package). However, for users who desire more control over the sampling 
process, it is more than possible to refer to lower-level classes and functions. These are surfaced in the submodules 
`graphs`, `chain`, and `toolbox`, all of which present helpful interfaces to more complex sampling problems. 

### Getting started

To begin with, make sure that the package is installed in your environment.

```bash
pip install git+https://github.com/jamesross2/random_graph
```

Next, we need to decide on a degree sequence. We can then sample a random graph from the package using the 
`sample_bipartite_graph` or `sample_graph` functions.

```python
import random_graph

# specify degree sequence we wish to impose
dx = [20] * 5 + [10] * 50  # 600 edges in total
dy = [3] * 200

# sample a bipartite graph, approximately uniformly at random, from all graphs with given degree sequence
# MCMC occurs under the hood
edges = random_graph.sample_bipartite_graph(dx, dy)
```

When sampling a bipartite graph (as above), the resulting `edges` object above is a set of `(x, y)` vertex pairs. For 
standard usage, this edge set is most likely the object of interest. For advanced users with specific requirements, it
is possible to apply switch operations to graph objects manually: check the section on advanced usage. 


### Advanced usage

Advanced users may wish to estimate the distribution of some random variable within the state space, such as the 
diameter or number of triangles of a graph. This is straightforward to estimate with the help of a callback function
applied during the resampling stage. Below, we give an example of estimating the proportion of bipartite graphs that are
incidence graphs of simple hypergraphs. 

```python
import random
import random_graph

# setting the random seed will ensure reproducible results
random.seed(708251)

# create a basic graph from a given degree sequence
dx = [100, 90, 80] * 10
dy = [5] * 540
graph = random_graph.graphs.SwitchBipartiteGraph.from_degree_sequence(dx, dy)

# sample the graph, including callback every so often
resampler = random_graph.Chain(graph)
callback_history = resampler.mcmc(iterations=int(1e6), callback=lambda g: g.simple(), call_every=100, burn_in=int(1e6))

# calculate proportion of sampled graphs that are simple
simple_frac = sum(callback_history) / len(callback_history)
print(f"Proportion of sampled graphs that were H-simple: {100*simple_frac:.1f}%")

# Proportion of sampled graphs that were H-simple: 36.7%
```

The resulting `history` object now contains the MCMC sampling results of our callback function. Using more advanced 
callbacks (such as custom classes that store intermediate states, for example), allows for sufficiently complex sampling
schemes to be employed.

Currently, the number of MCMC iterations is simply set to a default value (which can be specified in the `sample_*` 
call). We hope to add functionality for estimating the number of iterations required to achieve sufficient convergence
to the uniform distribution for a given degree sequence. 


### Integration with NetworkX

For further graph operations with graphs (such as spanning trees, subgraphs, or neighbourhoods), we recommend the 
excellent [`NetworkX`](https://github.com/networkx/networkx) package. Outputs from our graph sampling package can easily
be converted into NetworkX `Graph` objects using the below code.

```python
import random_graph
import networkx as nx

# sample a basic bipartite graph approximately uniformly at random
n, d, r = 20, 100, 4
m = (n * d) // r
edges = random_graph.sample_bipartite_graph([d] * n, [r] * m)

# create explicit vertex names for NetworkX
vx = [f"x{nx}" for nx in range(n)]
vy = [f"y{ny}" for ny in range(m)]

# create an empty graph 
graph = nx.Graph()

# add named vertices and edges using named vertices
graph.add_nodes_from(vx, bipartite=0)
graph.add_nodes_from(vy, bipartite=1)
graph.add_edges_from([(vx[nx], vy[ny]) for (nx, ny) in edges])
```

The resulting `graph` is a NetworkX bipartite graph with the desired vertex and edge sets. 


### More examples

This package was originally developed to count hypergraphs! Look at our [experiments](./experiments) folder for some 
simple projects that make use of the switch chain.


## Sampling algorithm and efficiency

### Switch chain

The sampling process uses a Markov Chain Monte Carlo (MCMC) process called the 'switch chain'. This chain returns a 
graph from the set of all graphs with the desired degree sequence, by applying random transformations to a graph 
repeatedly. Each transformation (or 'switch') swaps the end points of a pair of edges. The chain is defined in such a 
way that its unique stationary distribution is uniform, and that it converges to this distribution rapidly (i.e. as a 
logarithmic function of the state space size). Hence, the number of iterations grows only polynomially as a function of 
the number of edges, despite the number of graphs growing exponentially. (We are working on an automatic estimation 
process for the number of iterations required.)


### Speed

On a basic laptop CPU, this package can sample a random graph in under a second (it computes well over 100,000 switch 
operations per second), even for graphs with large numbers of nodes and edges. This allows for random graphs to be 
generated efficiently and at scale. Moreover, the speed per iteration has constant algorithmic complexity as a function 
of graph size and the number of edges. Hence, the sampling speed increases only as a function of the number of switches 
applied, and not of the graph itself, making the implementation very scalable to large graphs. 


## Contributing

We would love your contribution--anything from a [bug report](https://github.com/jamesross2/random_graph/issues/new) to a pull request!


### Setting up

We recommend working in a virtual environment for package development. Use [`direnv`](https://direnv.net/) to 
automatically activate your virtual environment.

```bash
# set up virtual environment, install required packages, and install random_graph
python -m pip install --upgrade pip virtualenv
python -m virtualenv .venv

# use direnv to activate the virtual environment whenever you are in the working directory
echo "source .venv/bin.activate > .envrc"
direnv allow

# install packages into new (activated) virtual environment
pip install -r requirements.txt
pip install -e .
```

All tests should be completed within the virtual environment, to ensure consistency. We test with tox, so any version of
Python3.6+ should work fine.


### Features to build

We would like to add all of the following to our project:

* Asymptotic testing to build a 'suggested runtime' feature for various
degree sequences.
* Automatically produce warnings when degree sequences that are not rapidly mixing are provided.
* Command line hooks so that non-Python users can leverage the package directly.
* Extension to simple graphs, directed graphs, and hypergraphs.


### Testing

After making changes, apply the package formatting rules and check that the package still passes the tests. This is 
achieved easily with the help of our Makefile.

```bash
make help  # check allowable make commands for more information
make format
make test
tox  # check that package passes tests on all tox versions
```

That's it! We would love your contributions or suggestions.

## References

Greenhill, C. (2014, December). The switch Markov chain for sampling irregular graphs. In _Proceedings of the 
twenty-sixth annual acm-siam symposium on discrete algorithms_ (pp. 1564-1572). Society for Industrial and Applied 
Mathematics.

Erdős, P. L., Mezei, T. R., Miklós, I., & Soltész, D. (2018). Efficiently sampling the realizations of bounded, 
irregular degree sequences of bipartite and directed graphs. _PloS one_, 13(8).

Erdös, P. L., Miklós, I., & Soukup, L. (2010). Towards random uniform sampling of bipartite graphs with given degree 
sequence. arXiv preprint arXiv:1004.2612.
