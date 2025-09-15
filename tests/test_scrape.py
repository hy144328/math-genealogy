import lxml.etree
import lxml.html
import pytest

import math_genealogy.graph
import math_genealogy.load
import math_genealogy.parse
import math_genealogy.scrape

class TestLoader(math_genealogy.load.Loader):
    d = {
        13700: "tests/karman.html",
        51374: "tests/prandtl.html",
        65163: "tests/liepmann.html",
        94381: "tests/marble.html",
        116101: "tests/candel.html",
        149678: "tests/juniper.html",
    }

    def load_page(self, ident: int) -> lxml.html.HtmlElement:
        with open(TestLoader.d[ident]) as f:
            return lxml.html.document_fromstring(f.read())

@pytest.fixture
def loader() -> math_genealogy.load.Loader:
    return TestLoader()

@pytest.fixture
def parser() -> math_genealogy.parse.Parser:
    return math_genealogy.parse.Parser()

@pytest.fixture
def scraper(
    loader: math_genealogy.load.Loader,
    parser: math_genealogy.parse.Parser,
) -> math_genealogy.scrape.Scraper:
    return math_genealogy.scrape.Scraper(loader, parser)

@pytest.fixture
def tree() -> math_genealogy.graph.Stammbaum:
    return math_genealogy.graph.Stammbaum()

def test_scrape(
    scraper: math_genealogy.scrape.Scraper,
    tree: math_genealogy.graph.Stammbaum,
):
    scraper.scrape(tree, 149678, [], level=0, max_level=3)

    assert 149678 in tree
    assert 116101 in tree
    assert 94381 in tree
    assert 13700 in tree
    assert 65163 in tree
    assert 51374 not in tree

def test_prune(
    scraper: math_genealogy.scrape.Scraper,
    tree: math_genealogy.graph.Stammbaum,
):
    scraper.scrape(tree, 149678, [], level=0, max_level=3)
    scraper.prune(tree, max_level=2)

    assert 149678 in tree
    assert 116101 in tree
    assert 94381 in tree
    assert 13700 not in tree
    assert 65163 not in tree
    assert 51374 not in tree
