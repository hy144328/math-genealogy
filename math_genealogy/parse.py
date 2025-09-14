# Copyright (C) 2025  Hans Yu <hans.yu@outlook.de>
#
# This file is part of MathDjinn.
#
# MathDjinn is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MathDjinn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MathDjinn.  If not, see <http://www.gnu.org/licenses/>.

import re
import typing
import urllib.parse

import lxml.etree
import lxml.html

BASE_URL = urllib.parse.urlparse("https://genealogy.math.ndsu.nodak.edu/id.php")

def load_page(ident: int) -> lxml.etree.ElementTree:    # pragma: no cover
    query = urllib.parse.urlencode({"id": ident})
    url = BASE_URL._replace(query=query)
    return lxml.html.parse(urllib.parse.urlunparse(url))

def parse_name(page: lxml.etree.ElementTree) -> str:
    e = page.find(".//h2")
    assert e is not None
    assert e.text is not None
    return e.text.strip()

RE_YEAR = re.compile(r"[^0-9]([0-9]{4})$")

def parse_year(page: lxml.etree.ElementTree) -> typing.Optional[int]:
    return next(
        (
            int(match_it.group(1))
            for span_it in page.findall(".//span")
            if span_it.tail is not None
            and (match_it := RE_YEAR.search(span_it.tail))
        ),
        None,
    )

RE_ADVISOR_URL = re.compile(r"^id.php\?id=([0-9]+)$")

def parse_advisors(page: lxml.etree.ElementTree) -> typing.List[int]:
    res: typing.List[int] = []

    for p_it in page.findall(".//p"):
        if p_it.text is None:   # pragma: no cover
            continue

        if not p_it.text.startswith("Advisor"):
            continue

        a_it = p_it.find("./a")
        assert a_it is not None

        href_it = a_it.get("href")
        assert href_it is not None

        mat_it = RE_ADVISOR_URL.search(href_it)
        assert mat_it is not None

        res.append(int(mat_it.group(1)))

    return res
