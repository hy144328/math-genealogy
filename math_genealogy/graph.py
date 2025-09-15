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

import dataclasses
import typing

import networkx as nx

@dataclasses.dataclass(frozen=True)
class StammbaumNode:
    ident: int
    name: str
    year: typing.Optional[int]

class Stammbaum:
    def __init__(self):
        self.g = nx.DiGraph()

    def add(self, node: StammbaumNode):
        self.g.add_node(
            node.ident,
            name = node.name,
            year = node.year,
        )

    def __getitem__(self, ident: int) -> StammbaumNode:
        node = self.g.nodes[ident]
        return StammbaumNode(
            ident = ident,
            name = node["name"],
            year = node["year"],
        )

    def __contains__(self, ident: int) -> bool:
        return ident in self.g.nodes

    def _validate_node(self, ident: int):
        if ident not in self.g.nodes:
            raise KeyError(f"Unknown node: {ident}.")

    def _validate_edge(self, pred: int, succ: int):
        if pred == succ:
            raise ValueError(f"Self-ancestry is not allowed: {pred}.")

    def add_ancestors(
        self,
        ident: int,
        ancestors: typing.Sequence[int],
    ):
        self._validate_node(ident)

        for ancestor_id in ancestors:
            self._validate_node(ancestor_id)
            self._validate_edge(ident, ancestor_id)
            self.g.add_edge(ident, ancestor_id)

    def get_ancestors(self, ident: int) -> typing.List[int]:
        return list(self.g.successors(ident))

    def get_descendants(self, ident: int) -> typing.List[int]:
        return list(self.g.predecessors(ident))

    @property
    def nodes(self) -> typing.List[int]:
        return list(self.g.nodes)

    @property
    def edges(self) -> typing.List[typing.Tuple[int, int]]:
        return list(self.g.edges)

    def remove(self, ident: int):
        self.g.remove_node(ident)
