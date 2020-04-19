import pytest

import random_graph.utils


def test_init():
    sampler = random_graph.utils.SampleSet(range(10))
    assert all(x in sampler for x in range(10))
    assert "a" not in sampler
    assert 15 not in sampler
    assert -1 not in sampler
    assert len(sampler) == 10
    assert list(x for x in sampler) == list(range(10))

    with pytest.raises(ValueError, match="Duplicate items"):
        random_graph.utils.SampleSet([1, 1, 1])


def test_transform():
    sampler = random_graph.utils.SampleSet("abcdefg")
    sampler.replace("a", "A")
    sampler.replace("b", "B")
    sampler.replace("c", "C")
    assert len(sampler) == 7
    assert "a" not in sampler
    assert "A" in sampler
    assert "b" not in sampler
    assert "B" in sampler
    assert "c" not in sampler
    assert "C" in sampler
    assert "d" in sampler
    assert "D" not in sampler

    # try bad replacements
    with pytest.raises(ValueError, match="Item already present"):
        sampler.add("f")
    with pytest.raises(ValueError, match="Item already present"):
        sampler.replace("g", "e")

    # try adding and removing instead of replacement
    sampler.remove("A")
    sampler.remove("d")
    assert len(sampler) == 5
    assert "A" not in sampler
    assert "d" not in sampler

    sampler.add("x")
    sampler.add("Y")
    assert len(sampler) == 7
    assert all(letter in sampler for letter in "BCefgxY")


def test_sampling():
    sampler = random_graph.utils.SampleSet(range(5))
    for _ in range(10):
        assert sampler.choice() in list(range(5))
