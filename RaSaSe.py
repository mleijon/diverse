#!/usr/bin/python
""""Random selection of samples from farms. Assumes a two column ascii-file as input. Column 1 should contain
    sample IDs and column 2 farm IDs"""

import argparse
import random

PARSER = argparse.ArgumentParser(description='Random selection of samples from farms. Assumes a two column ascii-file\
                                              as input. Column 1 should contain sample IDs and column 2 farm IDs.')
PARSER.add_argument('-f', type=str, help='Input list of items', required=True)
PARSER.add_argument('-s', type=int, help='Sample size', required=True)
PARSER.add_argument('-m', type=int, help='Farm sample multiplicity', default=1)
PARSER.add_argument('-mf', action='store_true', help='Force the farm sample multiplicity')
ARGS = PARSER.parse_args()
itemlist = []
samplelist = []
farms = dict()
farmset = set()
farmset_sel = set()

if ARGS.s % ARGS.m != 0 and ARGS.mf:
    print('sample size not a multiple of multiplicity. Exits.')
    exit(0)
with open(ARGS.f) as fi:
    for line in fi:
        itemlist.append(tuple(line.split()))
        if line.split()[1] not in farms.keys():
            farms.update({line.split()[1]: 0})
if ARGS.mf:
    for farm in farms:
        if len([x for x in itemlist if x[1] == farm]) >= ARGS.m:
            farmset.add(farm)
    try:
        farmset_sel = random.sample(farmset, ARGS.s//ARGS.m)
    except ValueError:
        print('Cannot sample - too little data.')
        print('Try to decrease multiplicity or remove the force multiplicity switch "-mf"')
        exit(0)
    itemlist = [x for x in itemlist if x[1] in farmset_sel]

while len(samplelist) < ARGS.s:
    if len(itemlist) == 0:
        print('Can only sample %d items' % len(samplelist))
        exit(0)
    else:
        sample = random.sample(itemlist, 1)[0]
        farms[sample[1]] += 1
        itemlist.remove(sample)
        samplelist.append(sample)
        itemlist[:] = [x for x in itemlist if not farms[x[1]] >= ARGS.m]
samplelist.sort(key=lambda tup: tup[1])
print(samplelist)
with open('selected_samples.txt', 'w') as fi:
    for item in samplelist:
        fi.write('%s\t%s\n' % (item[0], item[1]))

