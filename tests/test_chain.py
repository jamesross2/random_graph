from random_graph import chain, graphs


def test_init():
    # test empty version
    g = graphs.SwitchBipartiteGraph(17, 19, [])
    resampler = chain.Chain(g)
    assert isinstance(resampler, chain.Chain)

    # repeat for a graph with edges
    g = graphs.SwitchBipartiteGraph(5, 20, ((x, y) for x in range(5) for y in range(4 * x, 4 * x + 4)))
    resampler = chain.Chain(g)
    assert isinstance(resampler, chain.Chain)


def test_mcmc():
    # repeat for a graph with edges
    g = graphs.SwitchBipartiteGraph(5, 20, ((x, y) for x in range(5) for y in range(4 * x, 4 * x + 4)))
    resampler = chain.Chain(g)

    # check that invariant properties are unchanged by MCMC iteration
    results = resampler.mcmc()
    assert results == []
    assert g.nx == 5
    assert g.ny == 20
    assert len(g.neighbourhoods("x")) == 5
    assert len(g.neighbourhoods("y")) == 20
    assert all(list(len(neighbourhood) == 4 for neighbourhood in g.neighbourhoods("x")))
    assert all(len(neighbourhood) == 1 for neighbourhood in g.neighbourhoods("y"))

    # check that callback works also
    results = resampler.mcmc(callback=lambda g: g.simple(), iterations=100, call_every=5, burn_in=10)
    assert len(results) == 20
    assert all(isinstance(r, bool) for r in results)
