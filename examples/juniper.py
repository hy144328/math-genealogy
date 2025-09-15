#!/usr/bin/env python3

import os.path

import math_genealogy.graph
import math_genealogy.load
import math_genealogy.parse
import math_genealogy.scrape
import math_genealogy.viz

ROOT_ID = 149678

loader = math_genealogy.load.WebLoader()
parser = math_genealogy.parse.Parser()
scraper = math_genealogy.scrape.Scraper(loader, parser)
printer = math_genealogy.viz.DotPrinter()

tree = math_genealogy.graph.Stammbaum()
scraper.scrape(tree, ROOT_ID, max_level=3)
scraper.prune(tree, max_level=3)

for student_ct, (name_it, year_it) in enumerate([
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
]):
    tree.add(math_genealogy.graph.StammbaumNode(-student_ct, name=name_it, year=year_it))
    tree.add_ancestors(-student_ct, [ROOT_ID])

root, _ = os.path.splitext(__file__)
with open(".".join([root, "gv"]), "w") as f:
    printer.write(f, tree)
