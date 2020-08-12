from Bio import SeqIO
import os
import sys
import glob
import codecs
import subprocess

# path = os.getcwd()
path = os.path.dirname(os.path.abspath(__file__))


def file_check():
    os.chdir(path)
    # print(os.getcwd())
    os.chdir('../')
    home_dir = os.getcwd()
    # print(os.path.isdir('data'))
    if os.path.isdir('data') == True:
        os.chdir('./data')
        data_dir = os.getcwd()
        pep_files = glob.glob('*.pep')
        gff3_files = glob.glob('*genome.gff3')
        cds_files = glob.glob('*.cds')
        fasta_files = glob.glob('*.fasta')
        if len(pep_files) == 0 or len(pep_files) > 1:
            print(f'No .pep file or 2 more .pep files in{data_dir}')
            sys.exit()
        if len(gff3_files) == 0 or len(gff3_files) > 1:
            print(
                f'No .genome.gff3 file or 2 more .genome.gff3 files in{data_dir}')
            sys.exit()
        if len(cds_files) == 0 or len(cds_files) > 1:
            print(f'No .cds file or 2 more .cds files in{data_dir}')
            sys.exit()
        if len(fasta_files) == 0 or len(fasta_files) > 1:
            print(f'No .fasta file or 2 more .fasta files in{data_dir}')
            sys.exit()
        else:
            # print('All required Transdecoder files are exist')
            pep = pep_files[0]
            gff3 = gff3_files[0]
            cds = cds_files[0]
            fasta = fasta_files[0]
    else:
        print(f'No dir named "data" in {home_dir}')
    return{'pep': pep, 'gff3': gff3, 'cds': cds, 'fasta': fasta}


def extract_complete_fasta():
    # transcripts.fasta file is not annotated as "completed" in TransDecoder,
    # Therefore, that file is extracted with annotated complete cds file in another function.
    fasta_list = [transdecoder_outputs['pep'],
                  transdecoder_outputs['cds']]
    for fasta in fasta_list:
        if "pep" in fasta:
            fasta_complete = fasta.replace('.pep', '.complete.pep')
            f = open(fasta_complete, 'w')
            for record in SeqIO.parse(fasta, 'fasta'):
                id_part = record.id
                desc_part = record.description
                seq = record.seq
                if 'type:complete' in desc_part:
                    fasta_seq = '>' + id_part + '\n' + seq
                    fasta_seq = str(fasta_seq)
                    # print(fasta_complete)
                    print(fasta_seq, file=f)
        if "cds" in fasta:
            fasta_complete = fasta.replace('.cds', '.complete.cds')
            f = open(fasta_complete, 'w')
            for record in SeqIO.parse(fasta, 'fasta'):
                id_part = record.id
                desc_part = record.description
                seq = record.seq
                if 'type:complete' in desc_part:
                    fasta_seq = '>' + id_part + '\n' + seq
                    fasta_seq = str(fasta_seq)
                    # print(fasta_complete)
                    print(fasta_seq, file=f)


def extract_complete_gff3():
    # print(os.getcwd()) /TransDecoder_Annotator/data
    gff3 = transdecoder_outputs['gff3']
    gff3_out = gff3.replace('.gff3', '.complete.gff3')
    # print(gff3) transcripts.fasta.transdecoder.genome.gff3
    subprocess.call(
        f'perl ../scripts/extract_complete_gff.pl {gff3} > {gff3_out}', shell=True)


transdecoder_outputs = file_check()
extract_complete_fasta()
extract_complete_gff3()
