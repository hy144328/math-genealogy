import asyncio
import tempfile

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
    asyncio.run(scraper.scrape(res, 149678, max_level=3))
    return res

@pytest.fixture
def printer() -> math_genealogy.viz.Printer:
    return math_genealogy.viz.DotPrinter()

def test_scrape(
    printer: math_genealogy.viz.Printer,
    tree: math_genealogy.graph.Stammbaum,
):
    with tempfile.TemporaryDirectory() as temp_dir:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".gv",
            dir=temp_dir,
            delete=False,
        ) as temp_file:
            printer.write(temp_file, tree)

        with open(temp_file.name) as f:
            lines = [
                line_it.strip()
                for line_it in f
            ]

        for node_it in [
            "149678",
            "116101",
            "94381",
            "13700",
            "65163",
        ]:
            assert any(
                line_it.startswith(f"{node_it}")
                for line_it in lines
            )

        for node_from, node_to in [
            (149678, 116101),
            (116101, 94381),
            (94381, 13700),
            (94381, 65163),
        ]:
            assert any(
                line_it.startswith(f"{node_from} -> {node_to}")
                for line_it in lines
            )
