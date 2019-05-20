#! /usr/bin/python

import argparse
import os
PARSER = argparse.ArgumentParser(description='String modification')
PARSER.add_argument('-d', type=str, help='Input file directory', required=True)
PARSER.add_argument('-m', type=int, help='Farm sample multiplicity', default=1)
PARSER.add_argument('-mf', action='store_true', help='Force the farm sample multiplicity')
ARGS = PARSER.parse_args()