# mypy: ignore-errors

import argparse
from pprint import pprint

from protein_annotator.annotations.annotator import (
    annotate_protein as annotate_p,
    annotate_site as annotate_s,
)
from protein_annotator.annotations.dbs import download_biolip_db, download_uniprot_db
from protein_annotator.homologs import get_homologs

cli_parser = argparse.ArgumentParser(
    description=(
        "Provides serveral subcommands to retrieve homologs associated "
        "to a protein and making annotations"
    ),
)
subparsers = cli_parser.add_subparsers(
    dest="subcommand",
    description="To get more help, run protein_annotator <subcommand> -h",
)


def argument(*name_or_flags, **kwargs):
    return (list(name_or_flags), kwargs)


def subcommand(args=None, parent=subparsers):
    args = args or []

    def decorator(func):
        name = func.__name__
        description = func.__doc__

        parser = parent.add_parser(
            name,
            description=description,
            help=description,
        )

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
        argument(
            "-u",
            "--uniprot-db",
            type=str,
            help="Uniprot DB path",
        ),
    ]
)
def homologs(args):
    """Uses blast to retrieve a list of homolog proteins"""
    try:
        result = get_homologs(
            query=args.query,
            db=args.db,
            threshold=args.threshold,
            max_hits=args.max_hits,
            uniprot_db=args.uniprot_db,
        )
        pprint(result)
    except Exception as e:
        print(e)


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
    """Annotates a given site using Uniprot and BioLip databases"""
    try:
        result = annotate_s(
            args.uniprot_id,
            args.residue_number,
            args.uniprot_db,
            args.biolip_db,
        )
        pprint(result)
    except Exception as e:
        print(e)


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
    """Annotates a given protein using Uniprot and BioLip databases"""
    try:
        result = annotate_p(
            args.uniprot_id,
            args.uniprot_db,
            args.biolip_db,
        )
        pprint(result)
    except Exception as e:
        print(e)


@subcommand(
    [
        argument(
            "-n",
            "--db-name",
            type=str,
            required=True,
            choices=["uniprot", "biolip"],
            help="DB Name",
        ),
        argument(
            "-p",
            "--path",
            type=str,
            required=True,
            help="DB Path",
        ),
    ]
)
def download_db(args):
    """Downloads Uniprot or BioLip databases"""
    if args.db_name == "uniprot":
        download_uniprot_db(args.path)
    elif args.db_name == "biolip":
        download_biolip_db(args.path)
    else:
        raise ValueError("DB Name is not supported")


def run() -> None:
    args = cli_parser.parse_args()
    if args.subcommand is None:
        cli_parser.print_help()
    else:
        args.func(args)
