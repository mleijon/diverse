#! /usr/bin/python3

import argparse
import os
import sys


def mk_mod_dict(name):
    """

    :param name:
    :return:
    """
    try:
        infile = open(name)
    except FileNotFoundError:
        sys.exit('Modification file not found')
    mod_dict = dict()
    with open(ARGS.m) as infile:
        lines = infile.readlines()
        for line in lines:
            mod = line.strip().split(',')
            if mod[0] in mod_dict:
                mod_dict[mod[0]].append((mod[1], mod[2]))
            else:
                mod_dict[mod[0]] = [(mod[1], mod[2])]
    infile.close()
    return mod_dict


PARSER = argparse.ArgumentParser(description='String modification file')
PARSER.add_argument('-d', type=str, help='Input directory', required=True)
PARSER.add_argument('-m', type=str, help='modification file', default='mod.txt')
ARGS = PARSER.parse_args()

modifications = mk_mod_dict(ARGS.m)
try:
    with os.scandir(ARGS.d) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                tmpfile = open('modfile.tmp','w')
                with open(it) as infile:
                    all_lines = infile.readlines()

except FileNotFoundError:
    sys.exit("'{}' not found".format(ARGS.d))
except NotADirectoryError:
    sys.exit("'{}' is not a directory".format(ARGS.d))



