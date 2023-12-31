# Protein Annotator

## Setup

### Pre-requisites

Install blast tools:

- Ubuntu:

  ```shell
  sudo apt install ncbi-blast+
  ```

- MacOS:

  ```shell
  brew tap homebrew/science
  brew install ncbi-c++-toolkit
  brew install blast
  ```

Prepare a protein DB in your local drive with the NCBI tools if you want to run locally:

> In this example swissprot was already downloaded from <https://ftp.ncbi.nlm.nih.gov/blast/db/>.

```shell
makeblastdb -in swissprot -dbtype prot -parse_seqids
```

### Create venv

```shell
make install
```

### Activate venv

```shell
source .venv/bin/activate
```

### Run tests

```shell
make test
```

### Deactivate venv

```shell
deactivate
```

## Usage

### Bash command line

To see the general help run `protein_annotator -h`.

```shell
usage: protein_annotator [-h] {homologs,annotate_site,annotate_protein,download_db} ...

Provides serveral subcommands to retrieve homologs associated to a protein and make annotations

options:
  -h, --help            show this help message and exit

subcommands:
  To get more help, run protein_annotator <subcommand> -h

  {homologs,annotate_site,annotate_protein,download_db}
    homologs            Uses blast to retrieve a list of homolog proteins
    annotate_site       Annotates a given site using Uniprot and BioLip databases
    annotate_protein    Annotates a given protein using Uniprot and BioLip databases
    download_db         Downloads Uniprot or BioLip databases
```

For homologs help run `protein_annotator homologs -h`.

```shell
usage: protein_annotator homologs [-h] -q QUERY -db DB [-t THRESHOLD] [-m MAX_HITS] [-u UNIPROT_DB]

Uses blast to retrieve a list of homolog proteins

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        FASTA file path or Uniprot Id
  -db DB                NBCI database name
  -t THRESHOLD, --threshold THRESHOLD
                        Minimum identity percentage to be included in the results
  -m MAX_HITS, --max-hits MAX_HITS
                        Maximum number of hits
  -u UNIPROT_DB, --uniprot-db UNIPROT_DB
                        Uniprot DB path
```

Result Format

```python
[ (list)
  {
    'coverage': (float),
    'description': (str) homolog description,
    'e_value': (float),
    'id_percentage': (float) identity percentage,
    'sequence': (str) sequence associated with the homolog,
    'uniprot_id': (str) uniprot id associated with the homolog
  },
]
```

For site annotations help run `protein_annotator annotate_site -h`.

```shell
usage: protein_annotator annotate_site [-h] -i UNIPROT_ID [-r RESIDUE_NUMBER] -u UNIPROT_DB -b BIOLIP_DB

Annotates a given site using Uniprot and BioLip databases

options:
  -h, --help            show this help message and exit
  -i UNIPROT_ID, --uniprot-id UNIPROT_ID
                        Uniprot Id
  -r RESIDUE_NUMBER, --residue-number RESIDUE_NUMBER
                        Residue number to annotate
  -u UNIPROT_DB, --uniprot-db UNIPROT_DB
                        Uniprot DB path
  -b BIOLIP_DB, --biolip-db BIOLIP_DB
                        Biolip DB path
```

Result Format

```text
{
  "uniprot_id": (str) the uniprot id associated to the residue
  "biolip_annotation" : {
    "ligand": (str) protein ligand at the site,
    "residue": (str) the residue of the position indicated by the database,
    "residue_number": (str) the position of the residue,
    "sites": (str) the format of the position plus the residue according to biolip,
    "uniprot_id": (str) the uniprot id associated to the residue

  }
  "uniprot_annotation":{
    "ligand": (str) protein ligand at the site,
    "residue": (str) the residue of the position indicated by the database,
    "residue_number": (str) the position of the residue
  }
}
```

For protein annotations help run `protein_annotator annotate_protein -h`.

```shell
usage: protein_annotator annotate_protein [-h] -i UNIPROT_ID -u UNIPROT_DB -b BIOLIP_DB

Annotates a given protein using Uniprot and BioLip databases

options:
  -h, --help            show this help message and exit
  -i UNIPROT_ID, --uniprot-id UNIPROT_ID
                        Uniprot Id
  -u UNIPROT_DB, --uniprot-db UNIPROT_DB
                        Uniprot DB path
  -b BIOLIP_DB, --biolip-db BIOLIP_DB
                        Biolip DB path
```

Result Format

```text
{
  "uniprot_id": (str) the uniprot id associated to the protein
  "biolip_annotations": [ (list, can contain several)
    {
      "ligand": (str) protein ligand at the site,
      "residue": (str) the residue of the position indicated by the database,
      "residue_number": (str) the position of the residue,
      "sites": (str) the format of the position plus the residue according to biolip,
      "uniprot_id": (str) the uniprot id associated to the residue
    },
  ],
  "uniprot_annotations": [ (list, can contain several)
    {
      "ligand": (str) protein ligand at the site,
      "residue_number": (str) interval of the sequence in which it links with the residue format:[start:end], eg '[95:110]'
    },
  ]
}
```

For retrieving DBs help, run `protein_annotator download_db -h`.

```shell
usage: protein_annotator download_db [-h] -n {uniprot,biolip} -p PATH

Downloads Uniprot or BioLip databases

options:
  -h, --help            show this help message and exit
  -n {uniprot,biolip}, --db-name {uniprot,biolip}
                        DB Name
  -p PATH, --path PATH  DB Path
```

### Examples

```shell
(.venv) ➜  protein_annotator git:(main) protein_annotator homologs -q Q8I6R7 -db swissprot
Remote execution of blastp for protein.sequence='DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGYGGGGYGGGYGGGYGGGKYKG' db='swissprot' threshold=40 max_hits=10
[{'coverage': 100.0,
  'description': 'RecName: Full=Acanthoscurrin-2; Flags: Precursor '
                 '[Acanthoscurria gomesiana]',
  'e_value': 7.56499e-40,
  'id_percentage': 100.0,
  'sequence': 'DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGYGGGGYGGGYGGGYGGGKYKG',
  'uniprot_id': 'Q8I6R7'},
 {'coverage': 100.0,
  'description': 'RecName: Full=Acanthoscurrin-1; Flags: Precursor '
                 '[Acanthoscurria gomesiana]',
  'e_value': 5.70266e-37,
  'id_percentage': 98.0,
  'sequence': 'DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGGYGGGGGYGGGYGGGYGGGKYKG',
  'uniprot_id': 'Q8I948'}]
```

## In your Python project

### Homologs with local blastp execution and a DB in stored your drive

Given the sequence stored as a FASTA file:

```fasta
>sp|P99998|CYC_PANTR Cytochrome c OS=Pan troglodytes OX=9598 GN=CYCS PE=1 SV=2
MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIW
GEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE
```

**Important**: the FASTA file must contain a valid Uniprot Id in the header and must fall into one of the following templates:

- `>xx|YYYYYY.V|zzz` it will only match `YYYYYY`, `zzz` will be used as description
- `>YYYYYY.zzz` it will only match `YYYYYY`, `zzz` will be used as description

```python
from pprint import pprint

from protein_annotator.homologs import get_homologs

homologs = get_homologs(query="query.fasta", db="../swissprot")
pprint(homologs)
#> Local execution of blastp for query='query.fasta' db='../swissprot' threshold=40 max_hits=10
#> [{'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c [Pan troglodytes] >sp|P99999.2| '
#>                  'RecName: Full=Cytochrome c [Homo sapiens] >sp|Q5RFH4.3| '
#>                  'RecName: Full=Cytochrome c [Pongo abelii] >sp|Q6WUX8.3| '
#>                  'RecName: Full=Cytochrome c [Gorilla gorilla gorilla]',
#>   'e_value': 1.31049e-73,
#>   'id_percentage': 100.0,
#>   'sequence': 'MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE',
#>   'uniprot_id': 'P99998'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c [Macaca mulatta] >sp|Q52V08.3| '
#>                  'RecName: Full=Cytochrome c [Macaca sylvanus]',
#>   'e_value': 6.65513e-73,
#>   'id_percentage': 99.0,
#>   'sequence': 'MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGITWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE',
#>   'uniprot_id': 'P00002'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c [Trachypithecus cristatus]',
#>   'e_value': 5.93421e-71,
#>   'id_percentage': 97.0,
#>   'sequence': 'MGDVEKGKKILIMKCSQCHTVEKGGKHKTGPNHHGLFGRKTGQAPGYSYTAANKNKGITWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE',
#>   'uniprot_id': 'Q7YR71'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c [Ateles sp.]',
#>   'e_value': 1.47609e-70,
#>   'id_percentage': 95.0,
#>   'sequence': 'MGDVEKGKRIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQASGFTYTEANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE',
#>   'uniprot_id': 'P00003'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c [Oryctolagus cuniculus]',
#>   'e_value': 1.19533e-67,
#>   'id_percentage': 91.0,
#>   'sequence': 'MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLHGLFGRKTGQAVGFSYTDANKNKGITWGEDTLMEYLENPKKYIPGTKMIFAGIKKKDERADLIAYLKKATNE',
#>   'uniprot_id': 'P00008'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c [Saimiri sciureus]',
#>   'e_value': 1.73615e-67,
#>   'id_percentage': 92.0,
#>   'sequence': 'MGDVEKGKRIFIQKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAAGFTYTEANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKGEREDLIAYLKKATNE',
#>   'uniprot_id': 'Q52V10'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c, somatic [Mus musculus] '
#>                  '>sp|P62898.2| RecName: Full=Cytochrome c, somatic [Rattus '
#>                  'norvegicus]',
#>   'e_value': 3.78515e-67,
#>   'id_percentage': 91.0,
#>   'sequence': 'MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLHGLFGRKTGQAAGFSYTDANKNKGITWGEDTLMEYLENPKKYIPGTKMIFAGIKKKGERADLIAYLKKATNE',
#>   'uniprot_id': 'P62897'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c [Macropus giganteus]',
#>   'e_value': 5.20405e-67,
#>   'id_percentage': 90.0,
#>   'sequence': 'MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLNGIFGRKTGQAPGFTYTDANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFAGIKKKGERADLIAYLKKATNE',
#>   'uniprot_id': 'P00014'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c [Hippopotamus amphibius]',
#>   'e_value': 1.17256e-66,
#>   'id_percentage': 90.0,
#>   'sequence': 'MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLHGLFGRKTGQSPGFSYTDANKNKGITWGEETLMEYLENPKKYIPGTKMIFAGIKKKGERADLIAYLKQATNE',
#>   'uniprot_id': 'P00007'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Cytochrome c [Bos taurus] >sp|P62895.2| '
#>                  'RecName: Full=Cytochrome c [Sus scrofa] >sp|P62896.2| '
#>                  'RecName: Full=Cytochrome c [Ovis aries]',
#>   'e_value': 1.72185e-66,
#>   'id_percentage': 90.0,
#>   'sequence': 'MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGFSYTDANKNKGITWGEETLMEYLENPKKYIPGTKMIFAGIKKKGEREDLIAYLKKATNE',
#>   'uniprot_id': 'P62894'}]
```

### Homologs with remote blastp execution and Uniprot ID

```python
from pprint import pprint

from protein_annotator.homologs import get_homologs

homologs = get_homologs(query="Q8I6R7", db="swissprot")
pprint(homologs)
#> Remote execution of blastp for protein.sequence='DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGYGGGGYGGGYGGGYGGGKYKG' db='swissprot' threshold=40 max_hits=10
#> [{'coverage': 100.0,
#>   'description': 'RecName: Full=Acanthoscurrin-2; Flags: Precursor '
#>                  '[Acanthoscurria gomesiana]',
#>   'e_value': 7.56499e-40,
#>   'id_percentage': 100.0,
#>   'sequence': 'DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGYGGGGYGGGYGGGYGGGKYKG',
#>   'uniprot_id': 'Q8I6R7'},
#>  {'coverage': 100.0,
#>   'description': 'RecName: Full=Acanthoscurrin-1; Flags: Precursor '
#>                  '[Acanthoscurria gomesiana]',
#>   'e_value': 5.70266e-37,
#>   'id_percentage': 98.0,
#>   'sequence': 'DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGGYGGGGGYGGGYGGGYGGGKYKG',
#>   'uniprot_id': 'Q8I948'}]
```

### Annotations

```python
from pprint import pprint

from protein_annotator.annotations import annotator, dbs

dbs.download_biolip_db("../")
dbs.download_uniport_db("../")

site_annotations = annotator.annotate_site(
    "P05067",
    147,
    "../uniprot_sprot.dat.gz",
    "../BioLiP.txt.gz",
)
pprint(site_annotations)
#> {'biolip_annotation': {'ligand': 'BU4',
#>                        'residue': 'C',
#>                        'residue_number': '147',
#>                        'sites': 'C147',
#>                        'uniprot_id': 'P05067'},
#>  'uniprot_annotation': {'ligand': 'Cu(2+)',
#>                         'residue': 'H',
#>                         'residue_number': '147'},
#>  'uniprot_id': 'P05067'}

annotations = annotator.annotate_protein(
    "P05067",
    "../uniprot_sprot.dat.gz",
    "../BioLiP.txt.gz",
)
pprint(annotations)
#> {'biolip_annotations': [{'ligand': 'CU',
#>                          'residue': 'H',
#>                          'residue_number': '17',
#>                          'sites': 'H17',
#>                          'uniprot_id': 'P05067'},
#>                         {'ligand': 'CU',
#>                          'residue': 'H',
#>                          'residue_number': '21',
#>                          'sites': 'H21',
#>                          'uniprot_id': 'P05067'},
#>                         {'ligand': 'CU',
#>                          'residue': 'Y',
#>                          'residue_number': '38',
#>                          'sites': 'Y38',
#>                          'uniprot_id': 'P05067'},
#>                         ...
#>                         {'ligand': 'peptide',
#>                          'residue': 'V',
#>                          'residue_number': '18',
#>                          'sites': 'V18',
#>                          'uniprot_id': 'P05067'},
#>                         {'ligand': 'peptide',
#>                          'residue': 'I',
#>                          'residue_number': '31',
#>                          'sites': 'I31',
#>                          'uniprot_id': 'P05067'},
#>                         {'ligand': 'peptide',
#>                          'residue': 'I',
#>                          'residue_number': '32',
#>                          'sites': 'I32',
#>                          'uniprot_id': 'P05067'}],
#>  'uniprot_annotations': [{'ligand': 'heparin', 'residue_number': '[95:110]'},
#>                          {'ligand': 'Cu(2+)', 'residue_number': '[146:147]'},
#>                          {'ligand': 'Cu(2+)', 'residue_number': '[150:151]'},
#>                          {'ligand': 'Cu(2+)', 'residue_number': '[167:168]'},
#>                          {'ligand': 'Zn(2+)', 'residue_number': '[182:183]'},
#>                          {'ligand': 'Zn(2+)', 'residue_number': '[185:186]'},
#>                          {'ligand': 'Zn(2+)', 'residue_number': '[186:187]'},
#>                          {'ligand': 'Cu(2+)', 'residue_number': '[676:677]'},
#>                          {'ligand': 'Zn(2+)', 'residue_number': '[676:677]'},
#>                          {'ligand': 'Cu(2+)', 'residue_number': '[680:681]'},
#>                          {'ligand': 'Zn(2+)', 'residue_number': '[680:681]'},
#>                          {'ligand': 'Cu(2+)', 'residue_number': '[683:684]'},
#>                          {'ligand': 'Zn(2+)', 'residue_number': '[683:684]'},
#>                          {'ligand': 'Cu(2+)', 'residue_number': '[684:685]'},
#>                          {'ligand': 'Zn(2+)', 'residue_number': '[684:685]'}],
#>  'uniprot_id': 'P05067'}
```
