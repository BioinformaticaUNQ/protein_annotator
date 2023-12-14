from typing import Any, Dict, Hashable, List
from tqdm import tqdm
import pandas as pd


def _load_dataframe_from_csv(path: str) -> pd.DataFrame:
    #tqdm.pandas(desc='procesando bd BioliP')
    with tqdm(desc="cargando base de datos BioLip") as bar:    
        df = pd.read_csv(
            path,
            sep="\t",
            lineterminator="\n",
            compression="gzip",
            skiprows= lambda x: bar.update(1) and False,
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
    path: str, uniprot_id: str, residue_number: int
) -> Dict[Hashable, Any]:
    if not path or not uniprot_id or not residue_number:
        raise Exception("Invalid parameters")

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


def annotate_biolip(path: str, uniprot_id: str) -> List[Dict[Hashable, Any]]:
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
