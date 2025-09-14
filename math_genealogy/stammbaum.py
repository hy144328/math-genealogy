# Copyright (C) 2016  Hans Yu <hans.yu@outlook.de>
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

import typing

class Node:
    def __init__(
        self,
        ident: str,
        name: str,
        year: typing.Optional[int],
        parents: typing.Optional[typing.Sequence["Node"]],
    ):
        self.ident = ident
        self.name = name
        self.year = year
        self.parents = [*parents] if parents is not None else []

    def __str__(self):
        return f"{self.ident}, {self.name} ({self.year})"
