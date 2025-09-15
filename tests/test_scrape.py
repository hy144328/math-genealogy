import asyncio
import logging

import lxml.etree
import lxml.html
import pytest

import math_genealogy
import math_genealogy.graph
import math_genealogy.load
import math_genealogy.parse
import math_genealogy.scrape

logging.basicConfig()
math_genealogy_logger = logging.getLogger(math_genealogy.__name__)
math_genealogy_logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TestLoader(math_genealogy.load.Loader):
    d = {
        13700: "tests/karman.html",
        51374: "tests/prandtl.html",
        65163: "tests/liepmann.html",
        94381: "tests/marble.html",
        116101: "tests/candel.html",
        149678: "tests/juniper.html",
    }

    async def load_page(self, ident: int) -> lxml.html.HtmlElement:
        logger.debug(f"Opening HTML: {ident}.")
        with open(TestLoader.d[ident]) as f:
            html = f.read()
            logger.debug("Reading HTML.")
            return lxml.html.document_fromstring(html)

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
    asyncio.run(scraper.scrape(tree, 149678, max_level=3))

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
    asyncio.run(scraper.scrape(tree, 149678, max_level=3))
    scraper.prune(tree, max_level=2)

    assert 149678 in tree
    assert 116101 in tree
    assert 94381 in tree
    assert 13700 not in tree
    assert 65163 not in tree
    assert 51374 not in tree
