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

### Deactivate venv

```shell
deactivate
```

## Usage

### Bash command line

To see the general help run `protein_annotator -h`.

```shell
usage: protein_annotator [-h] {homologs,annotate_site,annotate_protein,download_db} ...

positional arguments:
  {homologs,annotate_site,annotate_protein,download_db}

options:
  -h, --help            show this help message and exit
```

For homologs help run `protein_annotator homologs -h`.

```shell
usage: protein_annotator homologs [-h] -q QUERY -db DB [-t THRESHOLD] [-m MAX_HITS]

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        FASTA file path or Uniprot Id
  -db DB                NBCI database name
  -t THRESHOLD, --threshold THRESHOLD
                        Minimum identity percentage to be included in the results
  -m MAX_HITS, --max-hits MAX_HITS
                        Maximum number of hits
```

For site annotations help run `protein_annotator annotate_site -h`.

```shell
usage: protein_annotator annotate_site [-h] -i UNIPROT_ID [-r RESIDUE_NUMBER] -u UNIPROT_DB -b BIOLIP_DB

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

For protein annotations help run `protein_annotator annotate_protein -h`.

```shell
usage: protein_annotator annotate_protein [-h] -i UNIPROT_ID -u UNIPROT_DB -b BIOLIP_DB

options:
  -h, --help            show this help message and exit
  -i UNIPROT_ID, --uniprot-id UNIPROT_ID
                        Uniprot Id
  -u UNIPROT_DB, --uniprot-db UNIPROT_DB
                        Uniprot DB path
  -b BIOLIP_DB, --biolip-db BIOLIP_DB
                        Biolip DB path
```

For retrieving DBs help, run `protein_annotator download_db -h`.

```shell
usage: protein_annotator download_db [-h] -n {uniprot,biolip} -p PATH

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

```python
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
