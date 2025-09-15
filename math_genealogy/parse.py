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

import logging
import re
import typing

import lxml.etree
import lxml.html

logger = logging.getLogger(__name__)

class Parser:
    RE_ADVISOR_URL = re.compile(r"^id.php\?id=([0-9]+)$")
    RE_YEAR = re.compile(r"[^0-9]([0-9]{4})$")

    @staticmethod
    def parse_name(page: lxml.etree.Element) -> str:
        e = page.find(".//h2")

        if e is None:   # pragma: no cover
            raise KeyError("Page has no header.")

        assert e.text is not None
        return e.text.strip()

    @staticmethod
    def parse_year(page: lxml.etree.Element) -> typing.Optional[int]:
        year = None

        spans = page.findall(".//span")
        if len(spans) == 0: # pragma: no cover
            raise KeyError("Page has no span.")

        for span_it in spans:
            if span_it.tail is None:    # pragma: no cover
                continue

            match_it = Parser.RE_YEAR.search(span_it.tail)
            if match_it is None:
                continue

            year = int(match_it.group(1))
            break

        if year is None:    # pragma: no cover
            logger.warning("Page has no year.")

        return year

    @staticmethod
    def parse_advisors(page: lxml.etree.Element) -> typing.List[int]:
        res: typing.List[int] = []

        ps = page.findall(".//p")
        if len(ps) == 0:    # pragma: no cover
            raise KeyError("Page has no paragraphs.")

        for p_it in ps:
            if p_it.text is None:   # pragma: no cover
                continue

            if not p_it.text.startswith("Advisor"):
                continue

            as_it = p_it.findall("./a")
            if len(as_it) == 0:    # pragma: no cover
                raise KeyError("Advisor has no URL.")

            for a_it in as_it:
                href_it = a_it.get("href")
                assert href_it is not None

                mat_it = Parser.RE_ADVISOR_URL.search(href_it)
                if mat_it is None:  # pragma: no cover
                    raise ValueError(f"Advisor URL does not match: {href_it}.")

                res.append(int(mat_it.group(1)))

        if len(res) == 0:   # pragma: no cover
            logger.warning("Page has no advisors.")

        return res
