import logging
from io import StringIO

from Bio.Blast import NCBIWWW, NCBIXML
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast.Record import Blast

from protein_annotator.schemas import Args, Hit

logger = logging.getLogger()


def run(args: Args) -> list[Hit]:
    blastp_command = NcbiblastpCommandline(
        db="../swissprot",
        query=args.query,
        # max_target_seqs=5,  # n hits
        out="out.xml",
        outfmt=5,  # Blast XML
    )
    logger.info(f"Executing command: {blastp_command}")

    stdout, stderr = blastp_command()  # noqa

    # Versión web, se queda esperando y nunca termina
    # blast_result = NCBIWWW.qblast(
    #     "blastp",
    #     args.db,
    #     parsed_input.protein.sequence,
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
            hits.append(
                Hit(
                    description=alignment.hit_def,
                    sequence=hsp.sbjct,
                    coverage=len(hsp.sbjct) / len(hsp.query) * 100,
                    e_value=hsp.expect,
                    id_percentage=round(hsp.identities / hsp.align_length, 2) * 100,
                )
            )
    return hits
