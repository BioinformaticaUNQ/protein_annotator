import argparse
import logging
from pprint import pprint

from protein_annotator.blast import run_blast
from protein_annotator.parser import InputParser
from protein_annotator.schemas import Args

logger = logging.getLogger()


def run_cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-db",
        type=str,
        # required=True,
        help="Nombre de la base de datos NBCI",
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
        "-m",
        "--max-hits",
        default=5,
        type=int,
        help="Número máximo de hits",
    )
    # parser.add_argument("-w", "--web", help="Buscar online")
    args: Args = parser.parse_args(namespace=Args)

    sequence = InputParser.parse(args.query)  # noqa (temporary)

    hits = run_blast(args)

    pprint(hits)
