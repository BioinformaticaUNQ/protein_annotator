from argparse import Namespace
from dataclasses import dataclass


class Args(Namespace):
    db: str
    query: str
    threshold: int
    max_hits: int


@dataclass(frozen=True)
class Protein:
    accession: str
    description: str
    sequence: str


@dataclass(frozen=True)
class Hit:
    coverage: float
    description: str
    e_value: float
    id_percentage: float
    sequence: str
    accession: str
