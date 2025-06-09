import argparse
import numpy as np

nr_of_samples = 96
cluster_nr = 0
cluster_re_nr = 0
bins = set()
cluster = set()


PARSER = argparse.ArgumentParser(description='TBD')
PARSER.add_argument('-c', type=str, help='cluster file', required=True)
PARSER.add_argument('-q', type=str, help='quality file', required=False)
PARSER.add_argument('-o', type=str, help='output file', required=False)
ARGS = PARSER.parse_args()

# Read the quality file from CheckM2 to determine which bins to include
with open(ARGS.q) as f:
    for line in f:
        if line.split('\t')[0].isdigit():
            bins.add(int(line.split('\t')[0]))
nr_of_bins = len(bins)
bin_matrix = np.zeros((nr_of_bins, nr_of_samples), dtype=np.uint8)

# Read the unsplit bin-file from vamb. Collect all samples that appear in each bin in "cluster" set. Then modify the
# matrix "bin_matrix" accordingly.
with open(ARGS.c) as f:
    for line in f:
        if not line.split('\t')[0].isdigit():
            continue
        if int(line.split('\t')[0]) in bins:
            if int(line.split('\t')[0]) != cluster_nr:
                if cluster_nr > 0:
                    for item in cluster:
                        bin_matrix[cluster_re_nr][item] = 1
                    cluster_re_nr += 1
                cluster = set()
                cluster_nr = int(line.split('\t')[0])
            cluster.add(int(line.split('\t')[1].split('C')[0][1:]) - 1)
    for item in cluster:
        bin_matrix[cluster_re_nr][item] = 1
f.close()

with open(ARGS.o, 'w') as f:
    np.savetxt(f, bin_matrix, delimiter='\t', fmt='%d')
f.close()
