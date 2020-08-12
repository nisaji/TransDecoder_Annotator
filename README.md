# TransDecoder Annotator
KAAS annotation for TransDecoder outputs

### Description
TransDecoder Annotator is an annotation tool for TransDecoderoutputs.
This tool outputs the file annotated with KEGG for the output files (.pep, .cds, .genome.gff3) of TranDecoder. Therefore, using this tool makes it easier to understand the functions of proteins and genes found by TransDecoder.

### Requirement
####  Install Biopython with conda
##### Setup miniconda (if already installed, skip this installation)
```
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh

bash Miniconda2-latest-Linux-x86_64.sh

ls ~/ 
# if miniconda2 is displaied, conda install is completed.

source ~/.bashrc

conda -h 
```

##### Setup biopython (if already installed, skip this installation)
```
# add channnel "conda-forge"
conda config --add channels conda-forge 

conda install -c conda-forge biopython
```

### Usage
1. git clone https://github.com/nisaji/TransDecoder_Annotator.git

2. place TransDecoder outputs like this.
```
./TransDecoder_Annotator
├── data
│   ├── ko_list.txt
│   ├── transcripts.fasta
│   ├── transcripts.fasta.transdecoder.cds
│   ├── transcripts.fasta.transdecoder.genome.gff3
│   └── transcripts.fasta.transdecoder.pep
└── scripts
    ├── annotator.py
    ├── extract_complete_gff.pl
    └── extract_completes.py
```

3. Run extract_complete.py
```
cd /Trnasdecoder_Annotator
python ./scripts/extract_complete.py
```
this script output `.complete.cds`, `.complete.pep`, `.genome.complete.gff3` in `/data`.

4. Run KAAS 
* This process need `.complete.pep`.
* Access [KAAS](https://www.genome.jp/kegg/kaas/)
* Run KAAS Job request(BBH or SBH)
* in **Query sequences (in multi-FASTA)**, chose **File upload** and upload .complete.pep file.
* Run **Compute**
* When KAAS is finished, Download result(txt) and name as **ko_list.txt** and place in `./TransDecoder_annotator/data/`

5. Run annotator.py
```
cd /Trnasdecoder_Annotator
python ./scripts/extract_complete.py
```
this script output `.complete.ann.cds`, `.complete.ann.pep`, `.complete.ann.gff3`.



