import lxml.etree
import lxml.html
import pytest

import math_genealogy.parse

@pytest.fixture
def page() -> lxml.etree.ElementTree:
    return lxml.html.parse("tests/juniper.html")

def test_parse_name(page: lxml.etree.ElementTree):
    assert math_genealogy.parse.parse_name(page) == "Matthew P. Juniper"

def test_parse_year(page: lxml.etree.ElementTree):
    assert math_genealogy.parse.parse_year(page) == 2001

def test_parse_advisors(page: lxml.etree.ElementTree):
    assert math_genealogy.parse.parse_advisors(page) == [116101]
