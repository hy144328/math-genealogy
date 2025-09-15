import pytest

import math_genealogy.graph

@pytest.fixture
def tree() -> math_genealogy.graph.Stammbaum:
    res = math_genealogy.graph.Stammbaum()
    res.add(math_genealogy.graph.StammbaumNode(0, "hans", 2020))
    return res

def test_stammbaum(
    tree: math_genealogy.graph.Stammbaum,
):
    assert 0 in tree

    assert 1 not in tree
    tree.add(
        math_genealogy.graph.StammbaumNode(1, name="matthew", year=2001),
    )
    assert 1 in tree

    assert 2 not in tree
    tree.add(
        math_genealogy.graph.StammbaumNode(2, name="luca", year=2013),
    )
    assert 2 in tree

    assert tree[0].name == "hans"
    assert tree[1].name == "matthew"
    assert tree[2].name == "luca"

    tree.add_ancestors(0, ancestors=[1, 2])

    with pytest.raises(ValueError):
        tree.add_ancestors(0, ancestors=[0])

    with pytest.raises(KeyError):
        tree.add_ancestors(0, ancestors=[-1])

    ancestors_0 = tree.get_ancestors(0)
    assert 1 in ancestors_0
    assert 2 in ancestors_0

    descendants_0 = tree.get_descendants(1)
    assert 0 in descendants_0
    assert 2 not in descendants_0

    tree.remove(2)

    assert 0 in tree.nodes
    assert 1 in tree.nodes
    assert 2 not in tree.nodes

    assert (0, 1) in tree.edges
    assert (0, 2) not in tree.edges
    assert (1, 2) not in tree.edges
    assert (0, 1) in tree.edges
