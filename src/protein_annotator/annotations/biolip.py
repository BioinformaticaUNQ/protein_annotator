from typing import Any, Callable, Dict, Hashable, List

import pandas as pd
from tqdm import tqdm


def _skip_none_and_update_progress_bar(bar: tqdm) -> Callable[[int], bool]:  # type: ignore
    def update_progress_bar(x: int) -> bool:
        bar.update(1)
        return False

    return update_progress_bar


def _load_dataframe_from_csv(path: str) -> pd.DataFrame:
    with tqdm(desc="Loading local BioLip DB", unit="rows") as bar:
        df = pd.read_csv(
            path,
            sep="\t",
            lineterminator="\n",
            compression="gzip",
            skiprows=_skip_none_and_update_progress_bar(bar),
            usecols=[4, 8, 17],
            names=[
                "NAid",
                "NA1",
                "NA2",
                "NA3",
                "ligand",
                "NA4",
                "NA5",
                "NA6",
                "sites",
                "NA7",
                "NA8",
                "NA9",
                "NA10",
                "NA11",
                "NA12",
                "NA13",
                "NA14",
                "uniprot_id",
                "NA15",
                "NA16",
                "NA17",
            ],
        )
        return df


def annotate_site_biolip(
    uniprot_id: str,
    residue_number: int,
    path: str,
) -> Dict[Hashable, Any]:
    """Annotates site using BioLip

    Args:
        uniprot_id (str): Uniprot protein id
        residue_number (int): position in sequence
        path (str): path to the database file

    Returns:
        Dict[str, Any]: annotated site
    """

    if not path or not uniprot_id or not residue_number:
        raise ValueError("Invalid parameters")

    df = _load_dataframe_from_csv(path)

    # filters dataframe by uniprot id
    result = df.loc[df["uniprot_id"] == str(uniprot_id)]

    if result.empty:
        return {}

    # splits the "sites" column into "residue" and "residue_number"
    result = result.assign(sites=df["sites"].str.split()).explode("sites")
    result[["residue", "residue_number"]] = result["sites"].str.extract(
        r"([A-Z])([000-999].+|[0-9]|[000-999].+|[0000-9999].+)"
    )

    # searches for ligands at the given redidue number (position)
    ret = result.loc[result["residue_number"] == str(residue_number)]

    if ret.empty:
        return {}

    annotations = ret.drop_duplicates().to_dict(orient="records")
    if not annotations:
        return {}
    return annotations[0]


def annotate_biolip(uniprot_id: str, path: str) -> List[Dict[Hashable, Any]]:
    """Annotates the protein associated to the Uniprot ID

    Args:
        uniprot_id (str): Uniprot protein id
        path (str): path to the database file

    Returns:
        List[Dict[str, Any]]: annotated protein
    """

    if not path or not uniprot_id:
        raise ValueError("Invalid parameters")

    df = _load_dataframe_from_csv(path)

    # filters dataframe by uniprot id
    result = df.loc[df["uniprot_id"] == str(uniprot_id)]

    if result.empty:
        return []

    # splits the "sites" column into "residue" and "residue_number"
    result = result.assign(sites=df["sites"].str.split()).explode("sites")
    result[["residue", "residue_number"]] = result["sites"].str.extract(
        r"([A-Z])([000-999].+|[0-9]|[000-999].+|[0000-9999].+)"
    )

    if result.empty:
        return []

    annotations = result.drop_duplicates().to_dict(orient="records")
    return annotations
