# mypy: ignore-errors

import argparse
import logging
from pprint import pprint

from protein_annotator.annotations.annotator import (
    annotate_protein as annotate_p,
    annotate_site as annotate_s,
)
from protein_annotator.homologs import get_homologs

logger = logging.getLogger()


cli_parser = argparse.ArgumentParser()
subparsers = cli_parser.add_subparsers(dest="subcommand")


def argument(*name_or_flags, **kwargs):
    return (list(name_or_flags), kwargs)


def subcommand(args=None, parent=subparsers):
    args = args or []

    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)

    return decorator


@subcommand(
    [
        argument(
            "-q",
            "--query",
            type=str,
            required=True,
            help="FASTA file path or Uniprot Id",
        ),
        argument(
            "-db",
            type=str,
            required=True,
            help="NBCI database name",
        ),
        argument(
            "-t",
            "--threshold",
            type=int,
            default=40,
            help="Minimum identity percentage to be included in the results",
        ),
        argument(
            "-m",
            "--max-hits",
            default=10,
            type=int,
            help="Maximum number of hits",
        ),
    ]
)
def homologs(args):
    result = get_homologs(
        query=args.query,
        db=args.db,
        threshold=args.threshold,
        max_hits=args.max_hits,
    )
    pprint(result)


@subcommand(
    [
        argument(
            "-i",
            "--uniprot-id",
            type=str,
            required=True,
            help="Uniprot Id",
        ),
        argument(
            "-r",
            "--residue-number",
            type=int,
            help="Residue number to annotate",
        ),
        argument(
            "-u",
            "--uniprot-db",
            type=str,
            required=True,
            help="Uniprot DB path",
        ),
        argument(
            "-b",
            "--biolip-db",
            type=str,
            required=True,
            help="Biolip DB path",
        ),
    ]
)
def annotate_site(args):
    result = annotate_s(
        args.uniprot_id,
        args.residue_number,
        args.uniprot_db,
        args.biolip_db,
    )
    pprint(result)


@subcommand(
    [
        argument(
            "-i",
            "--uniprot-id",
            type=str,
            required=True,
            help="Uniprot Id",
        ),
        argument(
            "-u",
            "--uniprot-db",
            type=str,
            required=True,
            help="Uniprot DB path",
        ),
        argument(
            "-b",
            "--biolip-db",
            type=str,
            required=True,
            help="Biolip DB path",
        ),
    ]
)
def annotate_protein(args):
    result = annotate_p(
        args.uniprot_id,
        args.uniprot_db,
        args.biolip_db,
    )
    pprint(result)


def run() -> None:
    args = cli_parser.parse_args()
    if args.subcommand is None:
        cli_parser.print_help()
    else:
        args.func(args)
