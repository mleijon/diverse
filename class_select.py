import os
import argparse
from collections import defaultdict

data = defaultdict(None)
bact_species = ['Pseudomonas aeruginosa', 'Escherichia coli',
                'Salmonella enterica', 'Lactobacillus fermentum',
                'Enterococcus faecalis' 'staphylococcus auerus',
                'Listeria monocytogenes', 'Bacillus Subtilis']
euca_species = ['Saccharomyces cerevisiae', 'Cryptococcus neoformans']

PARSER = argparse.ArgumentParser(description='TBD.')
PARSER.add_argument('-id', type=str, help='Directory for input data',
                    required=True)
PARSER.add_argument('-od', type=str, help='Directory for output data',
                    required=True)
PARSER.add_argument('-e', type=str, help='list of extraction methods',
                    required=True)
PARSER.add_argument('-m', type=str, help='type of microbe', required=True)
ARGS = PARSER.parse_args()
bact_lst = [name for name in os.listdir(ARGS.id) if
               os.path.isfile(ARGS.id + name) and name.upper().endswith(
                   'BACTERIA.TXT')]
euca_lst = [name for name in os.listdir(ARGS.id) if
               os.path.isfile(ARGS.id + name) and name.upper().endswith(
                   'EUCARYOTA.TXT')]
summary_lst = [name for name in os.listdir(ARGS.id) if
               os.path.isfile(ARGS.id + name) and name.upper().endswith(
                   'SUMMARY' + '.TXT')]
for file_name in summary_lst:
    sample_nr = int(file_name.split('_')[0])
    data[sample_nr] = {}
    file = ARGS.id + file_name
    with open(file) as f:
        data[sample_nr]['nr_of_reads'] = f.readlines()[0].split(':')[1].strip()
for item in bact_species:
    genus_count = species_count = 0
    for file_name in bact_lst:
        sample_nr = int(file_name.split('_')[0])
        file = ARGS.id + file_name
        with open(file) as f:
            for lines in f.readlines()[1:]:
                org = lines.strip().split('\t')[0].strip()
                nr_of_org = int(lines.strip().split('\t')[1].strip())
                print(org, nr_of_org)