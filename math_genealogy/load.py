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

import abc
import asyncio
import logging

import aiohttp
import lxml.etree
import lxml.html
import tenacity

logger = logging.getLogger(__name__)

class Loader(abc.ABC):
    @abc.abstractmethod
    async def load_page(self, ident: int) -> lxml.etree.Element:    # pragma: no cover
        raise NotImplementedError()

class WebLoader(Loader):    # pragma: no cover
    BASE_URL = "https://genealogy.math.ndsu.nodak.edu/id.php"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    @tenacity.retry(
        stop = tenacity.stop_after_attempt(10),
        wait = tenacity.wait_exponential(max=30),
        retry = tenacity.retry_if_exception_type(
            exception_types = (
                asyncio.TimeoutError,
                aiohttp.ClientResponseError,
            ),
        ),
        reraise = True,
        before_sleep = tenacity.before_sleep_log(logger, logging.WARNING),
    )
    async def load_page(self, ident: int) -> lxml.html.HtmlElement:
        logger.debug(f"Load {ident}.")
        async with self.session.get(WebLoader.BASE_URL, params={"id": ident}) as resp:
            html = await resp.text()
            logger.debug(f"Loaded {ident}.")

        return lxml.html.document_fromstring(html)
