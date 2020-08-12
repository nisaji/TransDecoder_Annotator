import os
import sys
import glob
import codecs
import subprocess
import re
from Bio import SeqIO
from Bio.KEGG import REST
import time

# path = os.getcwd()
path = os.path.dirname(os.path.abspath(__file__))

ko_dict = {}
gene_list = []


def complete_file_check():
    os.chdir(path)
    # print(os.getcwd())
    os.chdir('../')
    home_dir = os.getcwd()
    # print(os.path.isdir('data'))
    if os.path.isdir('data') == True:
        os.chdir('./data')
        data_dir = os.getcwd()
        pep_files = glob.glob('*.complete.pep')
        gff3_files = glob.glob('*.genome.complete.gff3')
        cds_files = glob.glob('*.complete.cds')
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
        else:
            # print('All required Transdecoder files are exist')
            pep = pep_files[0]
            gff3 = gff3_files[0]
            cds = cds_files[0]
    else:
        print(f'No dir named "data" in {home_dir}')
    return{'pep': pep, 'gff3': gff3, 'cds': cds}


def make_ko_list():
    if os.path.isfile("./ko_list.txt") == True:
        f = open("./ko_list.txt", "r")
    else:
        data_dir = os.getcwd()
        print(f'No file named "ko_list" in {data_dir}')
    line = f.readline()
    while line:
        # print(line)
        match = re.search('K[0-9]{1,8}', line)
        if match is None:
            pass
        else:
            gene = line.split()[0]
            ko = line.split()[1]
            ko_dict[gene] = ko
            gene_list.append(gene)
        line = f.readline()
    f.close
    return


def annotate_ko2pep():
    pep = complete_outputs['pep']
    pep_ann = pep.replace('.complete.pep', '.ann.complete.pep')
    f = open(pep_ann, 'w')
    for record in SeqIO.parse(pep, 'fasta'):
        id_part = record.id
        gene_part = id_part.split(".")[0] + "." + id_part.split(".")[1]
        seq = record.seq
        if gene_part in gene_list:
            ko = ko_dict[gene_part]
            REST.kegg_get(ko)
            result = REST.kegg_list(ko).read()
            definition = re.split('\t', result)[1]
            definition = definition.rstrip('\r\n')
            print(">" + id_part + " " + ko + " " + definition, file=f)
            print(seq, file=f)
            time.sleep(0.1)
        else:
            print(">" + id_part, file=f)
            print(seq, file=f)


def annotate_ko2cds():
    cds = complete_outputs['cds']
    cds_ann = cds.replace('.complete.cds', '.ann.complete.cds')
    f = open(cds_ann, 'w')
    for record in SeqIO.parse(cds_ann, 'fasta'):
        id_part = record.id
        gene_part = id_part.split(".")[0] + "." + id_part.split(".")[1]
        seq = record.seq
        if gene_part in gene_list:
            ko = ko_dict[gene_part]
            REST.kegg_get(ko)
            result = REST.kegg_list(ko).read()
            definition = re.split('\t', result)[1]
            definition = definition.rstrip('\r\n')
            print(">" + id_part + " " + ko + " " + definition, file=f)
            print(seq, file=f)
            time.sleep(0.1)
        else:
            print(">" + id_part, file=f)
            print(seq, file=f)
    return


def annotate_ko2gff():
    gff_complete = complete_outputs['gff3']
    gff3 = open(gff_complete, "r")
    gff3_ann = gff_complete.replace('.complete.gff3', '.ann.complete.gff3')
    f = open(gff3_ann, 'w')
    gff = gff3.readline()
    while gff:
        if '#' not in gff:
            feature = re.split('\t', gff)[2]
            attributes = re.split('\t', gff)[8]
            if feature == 'gene':
                attributes_id = re.split('[=;]', attributes)[1]
                attributes_name = re.split('[=;]', attributes)[3]
                if attributes_id in ko_dict:
                    ko = ko_dict[attributes_id]
                    REST.kegg_get(ko)
                    result = REST.kegg_list(ko).read()
                    result = result.replace(';', '')
                    result = result.replace(',', '')
                    ann_gff = gff.replace(attributes_name, result)
                    ann_gff = re.sub('\n', '', ann_gff)
                    print(ann_gff, file=f)
                else:
                    ann_gff = gff.replace(attributes_name, attributes_id)
                    print(ann_gff, file=f)
                gff = gff3.readline()

            elif feature == 'mRNA':
                attributes_id = re.split('[=;]', attributes)[1]
                attributes_gene_id = attributes_id.split(
                    '.')[0] + '.' + attributes_id.split('.')[1]
                attributes_name = re.split('[=;]', attributes)[5]
                # print(attributes_gene_id)
                if attributes_gene_id in ko_dict:
                    ko = ko_dict[attributes_gene_id]
                    REST.kegg_get(ko)
                    result = REST.kegg_list(ko).read()
                    result = result.replace(';', '')
                    result = result.replace(',', '')
                    ann_gff = gff.replace(attributes_name, result)
                    ann_gff = re.sub('\n', '', ann_gff)
                    print(ann_gff, file=f)
                else:
                    ann_gff = gff.replace(attributes_name, attributes_id)
                    print(ann_gff, file=f)
                gff = gff3.readline()

            else:
                gff = re.sub('\n', '', gff)
                print(gff, file=f)
                gff = gff3.readline()
        else:
            gff = gff3.readline()

        time.sleep(0.05)
    return


complete_outputs = complete_file_check()
make_ko_list()
annotate_ko2pep()
annotate_ko2cds()
annotate_ko2gff()
