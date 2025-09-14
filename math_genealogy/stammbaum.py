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
