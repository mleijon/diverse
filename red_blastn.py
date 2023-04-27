import os
import argparse

PARSER = argparse.ArgumentParser(description='TBD')
PARSER.add_argument('-d', type=str, help='Input directory', required=True)
PARSER.add_argument('-o', type=str, help='organism', required=True)
ARGS = PARSER.parse_args()

for file in [x for x in os.listdir(ARGS.d) if x.endswith('blastn') and not os.path.isdir(os.path.join(ARGS.d, x))]:
    data = dict()
    if os.path.getsize(os.path.join(ARGS.d, file)) == 0:
        continue
    out_filename = file.split('.')[0] + '.bln'
    out_file = open(os.path.join(ARGS.d, out_filename), 'w')
    current_sacc = ''
    current_query = ''
    with open(os.path.join(ARGS.d, file)) as f:
        for line in f.readlines():
            hit = line.strip().split('\t')
            if hit[0] != current_query:
                data[hit[0]] = [hit[1:]]
                current_query = hit[0]
                current_sacc = hit[1]
            elif hit[1] != current_sacc:
                data[hit[0]].append(hit[1:])
                current_sacc = hit[1]
            else:
                continue
        rm_keys = set()
        for key in data.keys():
            if ARGS.o.upper() not in [x.upper() for x in data[key][0][2].split() + data[key][0][3].split()]:
                rm_keys.add(key)
        for key in rm_keys:
            del data[key]
        for key in data.keys():
            out_file.writelines(key + '\n')
            for hit in range(len(data[key])):
                out_file.writelines('{}\t{}\t{}\t{}\n'.format(data[key][hit][0], data[key][hit][1],
                                                              data[key][hit][2], data[key][hit][3]))
            out_file.writelines('\n')
        out_file.close()
        f.close()
