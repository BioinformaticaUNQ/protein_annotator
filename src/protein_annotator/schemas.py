from dataclasses import dataclass


@dataclass(frozen=True)
class Protein:
    uniprot_id: str
    description: str
    sequence: str
