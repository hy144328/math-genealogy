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
import typing

import math_genealogy.graph

class Printer(abc.ABC):
    @abc.abstractmethod
    def print(
        self,
        f: typing.TextIO,
        tree: math_genealogy.graph.Stammbaum,
    ):
        raise NotImplementedError()

class DotPrinter(Printer):
    def print(
        self,
        f: typing.TextIO,
        tree: math_genealogy.graph.Stammbaum,
    ):
        f.write("digraph Stammbaum {\n")
        f.write("rankdir = BT;\n")
        f.write("node [shape=box, style=rounded];\n")
        f.write("\n")

        for node_it in tree.nodes:
            f.write(f"{node_it} [\"{tree[node_it].name}\"];\n")
        f.write("\n")

        for node_from, node_to in tree.edges:
            f.write(f"{node_from} -> {node_to} [dir=back];\n")
        f.write("\n")

        f.write("}\n")
