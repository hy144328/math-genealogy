import lxml.etree
import lxml.html
import pytest

import math_genealogy.parse

@pytest.fixture
def parser() -> math_genealogy.parse.Parser:
    return math_genealogy.parse.Parser()

@pytest.fixture
def page() -> lxml.etree.ElementTree:
    return lxml.html.parse("tests/juniper.html")

def test_parse_name(
    parser: math_genealogy.parse.Parser,
    page: lxml.etree.ElementTree,
):
    assert parser.parse_name(page) == "Matthew P. Juniper"

def test_parse_year(
    parser: math_genealogy.parse.Parser,
    page: lxml.etree.ElementTree,
):
    assert parser.parse_year(page) == 2001

def test_parse_advisors(
    parser: math_genealogy.parse.Parser,
    page: lxml.etree.ElementTree,
):
    assert parser.parse_advisors(page) == [116101]
