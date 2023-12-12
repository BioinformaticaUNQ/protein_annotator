import argparse
import logging
from pprint import pprint

from protein_annotator.homologs import get_homologs
from protein_annotator.schemas import Args

logger = logging.getLogger()


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        required=True,
        help="FASTA file path or Uniprot Id",
    )
    parser.add_argument(
        "-db",
        type=str,
        required=True,
        help="NBCI database name",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=40,
        help="Minimum identity percentage to be included in the results",
    )
    parser.add_argument(
        "-m",
        "--max-hits",
        default=10,
        type=int,
        help="Maximum number of hits",
    )
    args = parser.parse_args(namespace=Args)

    homologs = get_homologs(
        query=args.query,
        db=args.db,
        threshold=args.threshold,
        max_hits=args.max_hits,
    )

    pprint(homologs)
