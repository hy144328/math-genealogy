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

import asyncio
import logging
import sys
import typing

import math_genealogy.graph
import math_genealogy.load
import math_genealogy.parse

logger = logging.getLogger(__name__)

class Scraper:
    def __init__(
        self,
        loader: math_genealogy.load.Loader,
        parser: math_genealogy.parse.Parser,
        no_workers: int = 5,
    ):
        self.loader = loader
        self.parser = parser
        self.no_workers = no_workers

    async def scrape(
        self,
        tree: math_genealogy.graph.Stammbaum,
        root: int,
        max_level: int = sys.maxsize,
    ):
        logger.debug("Start scraping.")

        q: asyncio.LifoQueue[typing.Tuple[int, int, typing.Sequence[int]]] = asyncio.LifoQueue()
        logger.debug("Initializing queue.")
        await q.put((root, 0, []))

        logger.debug("Creating tasks.")
        tasks = [
            asyncio.create_task(self._scrape_worker(tree, q, max_level))
            for _ in range(self.no_workers)
        ]

        logger.debug("Joining tasks.")
        await q.join()

        logger.debug("Cancelling tasks.")
        for task_it in tasks:
            task_it.cancel()

        logger.debug("Gathering tasks.")
        await asyncio.gather(*tasks, return_exceptions=True)

        logger.debug("Finish scraping.")

    async def _scrape_worker(
        self,
        tree: math_genealogy.graph.Stammbaum,
        q: asyncio.Queue[typing.Tuple[int, int, typing.Sequence[int]]],
        max_level: int,
    ):
        while True:
            try:
                logger.debug(f"Popping queue: {q.qsize()}.")
                ident_it, level_it, descendants = await q.get()
            except asyncio.CancelledError as e:
                logger.debug("Queue closed.")
                raise e

            if level_it > max_level:
                logger.debug(f"Skip {ident_it} because {level_it} > {max_level}.")
                q.task_done()
                continue

            if ident_it in tree:
                logger.debug(f"Skip {ident_it} because repeated.")

                for descendant_it in descendants:
                    logger.info(f"From {descendant_it} to {ident_it}.")
                    tree.add_ancestors(descendant_it, [ident_it])

                q.task_done()
                continue

            logger.info(f"Loading and parsing page: {ident_it}.")
            page = await self.loader.load_page(ident_it)

            name = self.parser.parse_name(page)
            year = self.parser.parse_year(page)
            ancestors = self.parser.parse_advisors(page)

            node = math_genealogy.graph.StammbaumNode(ident_it, name=name, year=year)
            tree.add(node)

            for descendant_it in descendants:
                logger.info(f"From {descendant_it} to {ident_it}.")
                tree.add_ancestors(descendant_it, [ident_it])

            for ancestor_it in reversed(ancestors):
                await q.put((ancestor_it, level_it + 1, [ident_it]))

            q.task_done()

    def prune(
        self,
        tree: math_genealogy.graph.Stammbaum,
        max_level: int,
    ):
        heights = self._calculate_heights(tree)

        for node_it, height_it in heights.items():
            if height_it > max_level:
                logger.debug(f"Remove {node_it} of height {height_it}.")
                tree.remove(node_it)

    def _calculate_heights(
        self,
        tree: math_genealogy.graph.Stammbaum,
    ) -> typing.Dict[int, int]:
        res = {}

        for node_it in tree.nodes:
            self._calculate_heights_rec(tree, node_it, res)

        return res

    def _calculate_heights_rec(
        self,
        tree: math_genealogy.graph.Stammbaum,
        root: int,
        acc: typing.MutableMapping[int, int],
    ):
        if root in acc:
            return

        descendants = tree.get_descendants(root)

        for descendant_it in descendants:
            self._calculate_heights_rec(
                tree,
                descendant_it,
                acc,
            )

        acc[root] = max(
            (acc[descendant_it] for descendant_it in descendants),
            default = -1,
        ) + 1
