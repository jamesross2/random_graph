# Random Bipartite Graphs with Given Degree Sequence

[![Build Status](https://img.shields.io/travis/jamesross2/random_graph/master?logo=travis&style=flat-square)](https://travis-ci.org/jamesross2/random_graph?style=flat-square)
[![Code Coverage](https://img.shields.io/codecov/c/github/jamesross2/random_graph?logo=codecov&style=flat-square&label=codecov)](https://codecov.io/gh/jamesross2/random_graph)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=black&style=flat-square)](https://github.com/psf/black)

This is a fast, lightweight package for sampling random graphs.
It uses the 'switch chain' (a Markov Chain Monte Carlo process) to generate a graph approximately uniformly at random 
from the state space. Unlike other random graph paradigms (such as Erdos-Renyi random graphs), the switch chain samples
from a set of random graphs with known degree sequence. This makes it applicable to a different set of problems.


# Quick: I just want a random graph!

Here's the most basic way to use the package. To begin with, make sure that 
the package is installed in your environment.

```bash
pip install git+https://github.com/jamesross2/random_graph
```


Get a random graph from the package with the following gist.

```python
import random_graph

# specify degree sequence we wish to impose
dx = [20] * 5 + [10] * 50  # total 600
dy = [3] * 200

# sample a bipartite graph, approximately uniformly at random, from all graphs with given degree sequence
# MCMC occurs under the hood
edges = random_graph.sample_bipartite_graph(dx, dy)
```

The output `edges` is a set of `(x, y)` vertex pairs. For further graph operations, we recommend the excellent 
[`NetworkX`](https://github.com/networkx/networkx) package. Outputs from our graph sampling package can easily be 
converted into NetworkX `Graph` objects as follows:

```python
import networkx as nx

# create explicit vertex names
vx = ["x" + str(x) for x in range(len(dx))]
vy = ["y" + str(y) for y in range(len(dy))]

# create an empty graph 
B = nx.Graph()
 
# add named vertices and edges using named vertices
B.add_nodes_from(vx, bipartite=0)
B.add_nodes_from(vy, bipartite=1)
B.add_edges_from([(vx[x], vy[y]) for (x, y) in edges])
```

Currently, the number of MCMC iterations is simply set to a default value (which can be specified in the `sample_*` 
call). To ensure that the sampling distribution is sufficiently close to uniform, we refer to the convergence
formula calculated in our references. This is an ongoing item of work.


# Example application

This package was originally developed to count hypergraphs! Look at our 
[experiments](./experiments) folder for some simple projects that make use of the switch chain.


# Under the hood




# Contributing

We would love your contribution--anything from a [bug report](https://github.com/jamesross2/random_graph/issues/new) to a pull request!


## Getting started

We recommend working in a virtual environment for package development. 

```bash
python -m pip install --upgrade pip virtualenv
python -m virtualenv .venv
.venv/bin/python -m pip install -r requirements.txt

# be sure to work inside the virtual environment when working on the package:
source .venv/bin.activate
deactivate
```

Better yet, use [`direnv`](https://direnv.net/) to automatically activate your virtual environment.
After making changes, apply the package formatting rules and check that the package still passes the tests:

```bash
make help  # check allowable make commands for more information
make format
make test
tox  # check that package passes tests on all tox versions
```

That's it!


## Features to build

We would like to add all of the following to our project:

* An implementation of the [Gale-Ryser theorem](https://en.wikipedia.org/wiki/Gale%E2%80%93Ryser_theorem),
to test whether a provided degree sequence is graphical (and we can reliably initialise graphs of given 
degree sequences),
* Asymptotic testing to build a 'suggested runtime' feature for various
degree sequences,
* Command line hooks so that non-Python users can leverage the package directly, and
* Support to transform the final graph into a [`NetworkX`](https://github.com/networkx/networkx) object.
