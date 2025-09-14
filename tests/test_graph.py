import pytest

import math_genealogy.graph

@pytest.fixture
def g() -> math_genealogy.graph.Stammbaum:
    res = math_genealogy.graph.Stammbaum()
    res.add(math_genealogy.graph.StammbaumNode(0, "hans", 2020))
    return res

def test_stammbaum(
    g: math_genealogy.graph.Stammbaum,
):
    assert 0 in g

    assert 1 not in g
    g.add(
        math_genealogy.graph.StammbaumNode(1, name="matthew", year=2001),
    )
    assert 1 in g

    assert 2 not in g
    g.add(
        math_genealogy.graph.StammbaumNode(2, name="luca", year=2013),
    )
    assert 2 in g

    assert g[0].name == "hans"
    assert g[1].name == "matthew"
    assert g[2].name == "luca"

    g.add_ancestors(0, ancestors=[1, 2])

    with pytest.raises(ValueError):
        g.add_ancestors(0, ancestors=[0])

    with pytest.raises(KeyError):
        g.add_ancestors(0, ancestors=[-1])

    ancestors_0 = g.get_ancestors(0)
    assert 1 in ancestors_0
    assert 2 in ancestors_0
