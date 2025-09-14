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
import urllib.parse

import lxml.etree
import lxml.html

class Loader(abc.ABC):
    @abc.abstractmethod
    def load_page(self, ident: int) -> lxml.etree.ElementTree:  # pragma: no cover
        raise NotImplementedError()

class WebLoader(Loader):    # pragma: no cover
    BASE_URL = urllib.parse.urlparse("https://genealogy.math.ndsu.nodak.edu/id.php")

    def load_page(self, ident: int) -> lxml.etree.ElementTree:
        query = urllib.parse.urlencode({"id": ident})
        url = WebLoader.BASE_URL._replace(query=query)
        return lxml.html.parse(urllib.parse.urlunparse(url))
