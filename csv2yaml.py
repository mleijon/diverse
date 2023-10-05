import argparse
PARSER = argparse.ArgumentParser(description='TBD.')
PARSER.add_argument('-i', type=str, help='input csv-file',
                    required=True)
PARSER.add_argument('-o', type=str, help='output yaml-file',
                    required=True)
ARGS = PARSER.parse_args()

samples = list()

with open(ARGS.i) as f:
    for line in f.readlines()[1:]:
        samples.append(line.strip().split(";"))

with open(ARGS.o,"w") as f:
    f.writelines(["---\n", "# Metadata for 16S samples from VISSG/NORSE/OTTE\n"])
    for item in samples:
        f.write("{}:\n".format(item[0]))
        f.write("  farm: {}\n".format(item[1]))
        f.write("  set: {}\n".format(item[2]))
        f.write("  pigid: {}\n".format(item[3]))
        f.write("  weekaw: {}\n".format(item[4]))
        f.write("  pwd: {}\n".format(item[5].lower()))
        f.write("  zink: {}\n".format(item[6].lower()))
        f.write("  healthy: {}\n".format(item[7].lower()))

