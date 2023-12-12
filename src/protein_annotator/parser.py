import re
from pathlib import Path

import httpx
from Bio import SeqIO

from protein_annotator.schemas import Protein


class InputParser:
    VALID_ID_REGEX = re.compile(r"[a-zA-Z0-9_]+")

    @classmethod
    def parse(cls, input_data: str) -> Protein:
        if input_data.endswith(".fasta"):
            return parse_fasta(input_data)
        elif cls.VALID_ID_REGEX.match(input_data):
            return parse_uniprot_id(input_data)
        else:
            raise ValueError(
                "The provided input must be a path to a fasta file or a uniprot id"
            )


ACCESSION_REGEX = re.compile(r"\|(?P<accession>[0-9A-Z_]*)(\.[0-9]?)?\|")


def get_accession(seq_id) -> str:
    search = ACCESSION_REGEX.search(seq_id)
    groups = search.groupdict() if search else {}
    try:
        return groups["accession"]
    except KeyError:
        accession, _ = seq_id.split(".", maxsplit=1)
        return accession
    except ValueError:
        raise ValueError("Can not retrieve accession id")


def parse_fasta(file_path: str) -> Protein:
    """Parsea un archivo FASTA y desensambla sus componentes

    Args:
      path: ruta del archivo

    Returns:
      un dict con los atributos id, descripcion y secuencia
    """
    if not Path(file_path).exists():
        raise Exception("Invalid file path")

    results = []
    for record in SeqIO.parse(file_path, "fasta"):
        results.append(
            Protein(
                accession=get_accession(record.id),
                description=record.description,
                sequence=str(record.seq),
            )
        )
    return results[0]


def get_data_from_description(desc: str) -> tuple[str, str]:
    splitted = desc.split(".", maxsplit=1)
    return (splitted[0], "") if len(splitted) < 2 else (splitted[0], splitted[1])


def parse_uniprot_id(uniprot_id: str) -> Protein:
    """Obtiene un dict con la secuencia y descripcion a partir de un uniprotID

    Args:
      uniprot_id: identificador uniprot

    Returns:
      un ProteinData con los atributos id, descripcion y secuencia
    """
    try:
        result = httpx.get(
            f"https://www.uniprot.org/uniprotkb/{uniprot_id}.json",
            follow_redirects=True,
        )
        result.raise_for_status()
        parsed_response = result.json()

        return Protein(
            parsed_response["uniProtkbId"],
            "",
            parsed_response["sequence"]["value"],
        )

    except Exception as e:
        raise Exception("Failed to retrieve protein details from Uniprot") from e
