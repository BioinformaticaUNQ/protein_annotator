import gzip
import pathlib
from io import StringIO

import httpx
from Bio import SeqIO
from Bio.SeqIO.SwissIO import SwissIterator
from Bio.SeqRecord import SeqRecord
from tqdm import tqdm


def get_protein_from_uniprot_api(uniprot_id: str) -> SeqRecord:
    try:
        result = httpx.get(
            f"https://www.uniprot.org/uniprotkb/{uniprot_id}.xml",
            follow_redirects=True,
        )
        result.raise_for_status()

        found_record = SeqIO.read(StringIO(result.text), "uniprot-xml")
        return found_record

    except Exception as e:
        raise Exception(
            f"Protein associated with the uniprot id {uniprot_id} was not found"
        ) from e


def get_record_from_uniprot_db(uniprot_id: str, db_path: str) -> SeqRecord:
    if not pathlib.Path(db_path).exists():
        raise ValueError("Invalid uniprot db file path")

    with gzip.open(db_path, "rb") as handle:
        try:
            records: SwissIterator = SeqIO.parse(handle, "swiss")
            found_record = next(
                record
                for record in tqdm(
                    records,
                    desc="Searching for protein in local Uniprot DB",
                    unit="rows",
                )
                if record.id == uniprot_id
            )
            return found_record
        except Exception as e:
            raise ValueError(
                f"Protein associated with the uniprot id {uniprot_id} was not found"
            ) from e


def download_file(path_to_download: str, url: str, file_name: str) -> pathlib.Path:
    file_path = pathlib.Path(path_to_download) / file_name
    if file_path.exists():
        raise ValueError("File already exists")
    if file_path.is_dir():
        raise ValueError("File name must not be a directory")

    try:
        with open(file_path, "wb") as file_out:
            with httpx.stream(
                method="GET", url=url, follow_redirects=True, timeout=60
            ) as response:
                response.raise_for_status()

                file_size = int(response.headers.get("Content-Length", 0))
                desc = f"Downloading: {url}"

                for chunk in tqdm(
                    iterable=response.iter_raw(1),
                    desc=desc,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    total=file_size,
                ):
                    file_out.write(chunk)

        return file_path
    except Exception as e:
        file_path.unlink()
        raise Exception(f"Error while downloading file {url}: {e}") from e


def download_uniprot_db(path: str) -> None:
    download_file(
        path,
        "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz",
        "uniprot_sprot.dat.gz",
    )


def download_biolip_db(path: str) -> None:
    download_file(
        path,
        "https://zhanggroup.org/BioLiP/download/BioLiP.txt.gz",
        "BioLiP.txt.gz",
    )
