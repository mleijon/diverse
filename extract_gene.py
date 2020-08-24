import pandas as pd
import os
import argparse
from fasta import FastaList

DATA_COL = 3


def find_gene_row():
    at_end = False
    row = 0
    while not at_end:
        try:
            if df.iat[row, 2] == ARGS.g:
                return row
            else:
                row += 1
        except:
            at_end = True


PARSER = argparse.ArgumentParser(description='TBD')
PARSER.add_argument('-d', type=str, help='Excel file Input directory',
                    required=True)
PARSER.add_argument('-fd', type=str, help='fasta file Input directory',
                    required=True)
PARSER.add_argument('-g', type=str, help='gene to extract', required=False)
ARGS = PARSER.parse_args()
output = open(ARGS.fd + '\\' + ARGS.g + '.fa', 'w')
for item in os.listdir(ARGS.d):
    filename = ARGS.d + '\\' + item
    data = pd.read_excel(filename)
    df = pd.DataFrame(data, dtype=str)
    gene_row = find_gene_row()
    if not df.iat[gene_row, DATA_COL] == '-':
        fastaname = ARGS.fd + '\\' + item.replace('.xlsx', '.ffn')[5:]
        fl = FastaList(fastaname)
        for seq in fl.seq_list:
            orf = seq.strip().split('\n')[0].split('\t')[0][1:]
            isolate = seq.strip().split('\n')[0].split('|')[1]
            length = seq.strip().split('\n')[0].split('len=')[1]
            seq = seq.split('\n')[1] + '\n'
            if orf == df.iat[gene_row, DATA_COL]:
                id = '>' + orf + '|' + isolate + '|len=' + length + '\n'
                output.write(id + seq)
print('Done')
output.close()



