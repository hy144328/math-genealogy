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
import sys
import typing

import math_genealogy.graph
import math_genealogy.parse

logger = logging.getLogger(__name__)

def grow(
    tree: math_genealogy.graph.Stammbaum,
    root: int,
    descendants: typing.Sequence[int],
    level: int = 0,
    max_level: int = sys.maxsize,
):
    if level > max_level:
        return

    if root in tree:
        logger.debug(f"Skip {root}.")

        for descendant_it in descendants:
            logger.info(f"From {descendant_it} to {root}.")
            tree.add_ancestors(descendant_it, [root])

        return

    page = math_genealogy.parse.load_page(root)
    name = math_genealogy.parse.parse_name(page)
    year = math_genealogy.parse.parse_year(page)

    node = math_genealogy.graph.StammbaumNode(root, name=name, year=year)
    tree.add(node)

    for descendant_it in descendants:
        logger.info(f"From {descendant_it} to {root}.")
        tree.add_ancestors(descendant_it, [root])

    ancestors = math_genealogy.parse.parse_advisors(page)
    for ancestor_it in ancestors:
        grow(
            tree,
            ancestor_it,
            [root],
            level = level+1,
            max_level = max_level,
        )
