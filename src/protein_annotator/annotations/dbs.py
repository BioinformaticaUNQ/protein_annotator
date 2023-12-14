import gzip
import logging
import pathlib
from io import StringIO
from tqdm import tqdm
import httpx
from Bio import SeqIO, SwissProt
from Bio.SeqIO.SwissIO import SwissIterator
from Bio.SeqRecord import SeqRecord
from Bio.SwissProt import Record
from tqdm import tqdm

logger = logging.getLogger()


def get_protein_from_api(uniprod_id: str) -> Record:
    response = httpx.get(f"https://rest.uniprot.org/uniprotkb/{uniprod_id}?format=txt")
    record = SwissProt.read(StringIO(response.text))
    return record


def get_protein_from_db(uniprod_id: str, db_path: str) -> SeqRecord:
    found_record = None
    with gzip.open(db_path, "rb") as handle:
        try:
            records: SwissIterator = SeqIO.parse(handle, "swiss")
            found_record = next(
                (record for record in tqdm(records, desc="procesando uniprot") if record.id == uniprod_id), None
            )
            return found_record
        except Exception:
            return found_record


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
        logger.exception(f"Error while downloading file {url}")
        file_path.unlink()
        raise e


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
