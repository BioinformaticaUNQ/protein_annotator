import argparse
import logging
from io import StringIO

from Bio.Blast import NCBIWWW, NCBIXML
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast.Record import Blast

from protein_annotator.schemas import ProteinData
from protein_annotator.tools import (
    get_fasta_from_uniprot,
    is_fasta,
    is_uniprot_id,
    parse_fasta,
)

logger = logging.getLogger()


class InputParser:
    ##
    def __init__(self, input: str) -> None:
        self.protein = self.parse_input(input)

    def parse_sequence(self, input: str):
        pass

    def parse_input(self, input: str) -> ProteinData:
        if is_fasta(input):
            return parse_fasta(input)
        elif is_uniprot_id(input):
            return get_fasta_from_uniprot(input)
        else:
            raise Exception(
                "Input provided must be a path to a fasta file or a uniprot id"
            )

    def __str__(self) -> str:
        return f"{self.sequence}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-db",
        type=str,
        # required=True,
        help="Base de datos NBCI",
    )
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        required=True,
        help="Ruta del archivo FASTA or Uniprot Id",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=40,
        help="Puntaje mínimo para ser incluido en la búsqueda",
    )
    parser.add_argument(
        "-n",
        "--n-hits",
        default=5,
        type=int,
        help="Número de hits",
    )
    # parser.add_argument("-w", "--web", help="Buscar online")
    args = parser.parse_args()

    annotator = InputParser(args.query)

    blastp_command = NcbiblastpCommandline(
        db="../swissprot",
        query=annotator.protein.input,
        max_target_seqs=5,  # n hits
        out="out.xml",
        outfmt=5,  # Blast XML
    )
    logger.info(f"Executing command: {blastp_command}")

    stdout, stderr = blastp_command()

    # Versión web, se queda esperando y nunca termina
    # blast_result = NCBIWWW.qblast(
    #     "blastp",
    #     args.db,
    #     annotator.protein.sequence,
    #     threshold=40,
    #     hitlist_size=5,
    #     format_type="XML",
    # )

    query_result = ""
    with open("out.xml", "r") as f:
        file = f.read()
        query_result = StringIO(file)

    blast: Blast = NCBIXML.read(query_result)

    hits = []
    for alignment in blast.alignments:
        for hsp in alignment.hsps:
            hit = {
                "sequence": hsp.sbjct,
                "coverage": len(hsp.sbjct) / len(hsp.query) * 100,
                "e_value": hsp.expect,
                "id_percentage": round(hsp.identities / hsp.align_length, 2) * 100,
            }
            hits.append(hit)

    print(hits)


if __name__ == "__main__":
    main()
