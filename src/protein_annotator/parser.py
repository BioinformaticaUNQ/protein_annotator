import re
from pathlib import Path
from typing import Optional

from Bio import SeqIO

from protein_annotator.annotations.dbs import (
    get_protein_from_uniprot_api,
    get_record_from_uniprot_db,
)
from protein_annotator.schemas import Protein


class InputParser:
    VALID_ID_REGEX = re.compile(r"[a-zA-Z0-9_]+")

    @classmethod
    def parse(cls, input_data: str, uniprot_db: Optional[str] = None) -> Protein:
        if input_data.endswith(".fasta"):
            return parse_fasta(input_data)
        elif cls.VALID_ID_REGEX.match(input_data):
            return parse_uniprot_id(input_data, uniprot_db)
        else:
            raise ValueError(
                "The provided input must be a path to a fasta file or a uniprot id"
            )


ACCESSION_REGEX = re.compile(r"\|(?P<accession>[0-9A-Z_]*)(\.[0-9]?)?\|")


def get_uniprot_id_from_accession(seq_id: str) -> str:
    search = ACCESSION_REGEX.search(seq_id)
    groups = search.groupdict() if search else {}
    try:
        return groups["accession"]
    except KeyError:
        accession, _ = seq_id.split(".", maxsplit=1)
        return accession
    except ValueError:
        raise ValueError("Can not retrieve accession id")


def validate_sequence(seq: str) -> None:
    NUCLEOTIDE_SEQUENCE = re.compile(r"^[ACGT]*$")
    if NUCLEOTIDE_SEQUENCE.match(seq):
        raise Exception("Sequences shoud be proteins. Nucleotide found instead")


def parse_fasta(file_path: str) -> Protein:
    """Parses a FASTA file with a unique registry

    Args:
      path: file path

    Returns:
      a protein object
    """
    if not Path(file_path).exists():
        raise ValueError("Invalid FASTA file path")

    record = SeqIO.read(file_path, "fasta")
    validate_sequence(str(record.seq))

    protein = Protein(
        uniprot_id=get_uniprot_id_from_accession(record.id),
        description=record.description,
        sequence=str(record.seq),
    )
    return protein


def parse_uniprot_id(uniprot_id: str, db_path: Optional[str] = None) -> Protein:
    """Get a dict with the sequence and description from a uniprotID

    Args:
      uniprot_id: uniprot identifier
      db_path (str): path to the local uniprot database file

    Returns:
      an instance of a Protein
    """
    if db_path:
        record = get_record_from_uniprot_db(uniprot_id, db_path)
    else:
        record = get_protein_from_uniprot_api(uniprot_id)

    return Protein(
        record.id,
        record.description,
        str(record.seq),
    )
