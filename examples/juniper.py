#!/usr/bin/env python3

import asyncio
import logging
import os.path

import aiohttp

import math_genealogy
import math_genealogy.graph
import math_genealogy.load
import math_genealogy.parse
import math_genealogy.scrape
import math_genealogy.viz

logging.basicConfig()
math_genealogy_logger = logging.getLogger(math_genealogy.__name__)
math_genealogy_logger.setLevel(logging.INFO)

TIMEOUT_SECONDS = 30
MAX_LEVEL = 3
POOL_SIZE = 5
ROOT_ID = 149678
STUDENTS = [
    ("Simon Rees", 2009),
    ("Gary Chandler", 2010),
    ("Larry Li", 2011),
    ("Iain Waugh", 2013),
    ("Ubaid Qadri", 2013),
    ("Karthik Kashinath", 2013),
    ("Vikrant Gupta", 2014),
    ("Giulio Ghirardo", 2015),
    ("Luca Magri", 2015),
    ("Alessandro Orchini", 2016),
    ("Nicholas Jamieson", 2018),
    ("José Aguilar Perez", 2019),
    ("Jack Brewster", 2019),
]

async def main():
    client_timeout = aiohttp.ClientTimeout(TIMEOUT_SECONDS)

    async with aiohttp.TCPConnector(limit_per_host=POOL_SIZE) as conn:
        async with aiohttp.ClientSession(connector=conn, timeout=client_timeout) as session:
            loader = math_genealogy.load.WebLoader(session)
            parser = math_genealogy.parse.Parser()
            scraper = math_genealogy.scrape.Scraper(loader, parser)
            printer = math_genealogy.viz.DotPrinter()

            tree = math_genealogy.graph.Stammbaum()
            await scraper.scrape(tree, ROOT_ID, max_level=MAX_LEVEL)
            scraper.prune(tree, max_level=MAX_LEVEL)

            for student_ct, (name_it, year_it) in enumerate(STUDENTS):
                tree_node = math_genealogy.graph.StammbaumNode(
                    -student_ct,
                    name = name_it,
                    year = year_it,
                )
                tree.add(tree_node)
                tree.add_ancestors(-student_ct, [ROOT_ID])

            root, _ = os.path.splitext(__file__)
            with open(".".join([root, "gv"]), "w") as f:
                printer.write(f, tree)

if __name__ == "__main__":
    asyncio.run(main())
