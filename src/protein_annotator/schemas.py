from argparse import Namespace
from dataclasses import dataclass, field


class Args(Namespace):
    db: str
    query: str
    threshold: int
    max_hits: int


@dataclass
class Sequence:
    accession: str
    description: str
    sequence: str


@dataclass
class Hit:
    accession: str = field(init=False)
    description: str
    sequence: str
    coverage: float
    e_value: float
    id_percentage: float

    def __post_init__(self) -> None:
        try:
            self.accession, _ = self.description.split(".", maxsplit=1)
        except ValueError:
            raise ValueError("La descripción del hit no contiene un ID válido.")
