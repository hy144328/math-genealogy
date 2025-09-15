import pytest

import math_genealogy.graph
import math_genealogy.load
import math_genealogy.parse
import math_genealogy.scrape
import math_genealogy.viz

import tests.test_scrape

@pytest.fixture
def loader() -> math_genealogy.load.Loader:
    return tests.test_scrape.TestLoader()

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
def tree(
    scraper: math_genealogy.scrape.Scraper,
) -> math_genealogy.graph.Stammbaum:
    res = math_genealogy.graph.Stammbaum()
    scraper.scrape(res, 149678, [], level=0, max_level=3)
    return res

@pytest.fixture
def printer() -> math_genealogy.viz.Printer:
    return math_genealogy.viz.DotPrinter()

def test_scrape(
    printer: math_genealogy.viz.Printer,
    tree: math_genealogy.graph.Stammbaum,
):
    with open("tests/juniper.gv", "w") as f:
        printer.write(f, tree)
