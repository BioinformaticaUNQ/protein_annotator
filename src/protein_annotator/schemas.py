from dataclasses import dataclass


@dataclass(frozen=True)
class Protein:
    accession: str
    description: str
    sequence: str
