from __future__ import annotations

import re
from pathlib import Path

import httpx
from Bio import SeqIO
from protein_annotator.annotations.dbs import get_protein_from_db

from protein_annotator.schemas import Protein


class InputParser:
    VALID_ID_REGEX = re.compile(r"[a-zA-Z0-9_]+")

    @classmethod
    def parse(cls, input_data: str, uniprot_db: str = None) -> Protein:
        if input_data.endswith(".fasta"):
            return parse_fasta(input_data)
        elif cls.VALID_ID_REGEX.match(input_data):
            return parse_uniprot_id(input_data, uniprot_db)
        else:
            raise ValueError(
                "The provided input must be a path to a fasta file or a uniprot id"
            )


ACCESSION_REGEX = re.compile(r"\|(?P<accession>[0-9A-Z_]*)(\.[0-9]?)?\|")


def get_accession(seq_id: str) -> str:
    search = ACCESSION_REGEX.search(seq_id)
    groups = search.groupdict() if search else {}
    try:
        return groups["accession"]
    except KeyError:
        accession, _ = seq_id.split(".", maxsplit=1)
        return accession
    except ValueError:
        raise ValueError("Can not retrieve accession id")

def validate_sequence(seq:any) -> None:
    NUCLEOTIDE_SEQUENCE = re.compile(r'^[ACGT]*$')
    if NUCLEOTIDE_SEQUENCE.match(str(seq)):
        raise Exception("Sequences shoud be proteins. Nucleotide found instead")


def parse_fasta(file_path: str) -> Protein:
    """Parses a FASTA file with a unique registry

    Args:
      path: file path

    Returns:
      a protein object
    """
    if not Path(file_path).exists():
        raise Exception("Invalid file path")

    results = []
    for record in SeqIO.parse(file_path, "fasta"):
        validate_sequence(record.seq)
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


def parse_uniprot_id(uniprot_id: str, uniprot_db: str = None) -> Protein:
    """Get a dict with the sequence and description from a uniprotID

    Args:
      uniprot_id: uniprot identifier

    Returns:
      a Protein object
    """
    if uniprot_db and not Path(uniprot_db).exists():
        raise Exception("Invalid uniprot db file path")
    if uniprot_db and Path(uniprot_db).exists():
        local_uniprot_result = get_protein_from_db(uniprot_id, uniprot_db)
        return Protein(
            local_uniprot_result.name,
            local_uniprot_result.description,
            str(local_uniprot_result.seq)
        ) or None
    else:
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
