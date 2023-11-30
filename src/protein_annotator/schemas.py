from dataclasses import dataclass

@dataclass
class ProteinData:
    id: str
    description: str
    sequence: str
    input: str | object | None