import argparse


PARSER = argparse.ArgumentParser(description='TBD')
PARSER.add_argument('-c', type=str, help='cluster file', required=True)
PARSER.add_argument('-q', type=str, help='quality file', required=True)
PARSER.add_argument('-o', type=str, help='output file', required=True)
ARGS = PARSER.parse_args()

with open(ARGS.c) as f:
