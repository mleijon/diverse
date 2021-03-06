#! /usr/bin/python3

import argparse
import os
import sys
from shutil import copyfile


def mk_mod_dict(name):
    """Reads an input file with a list of text file modifications, one per line. With  the format:
    row-nr,column_nr,new_character. A special case is deletion of a line, which is indicated by row_nr,d,. This
    function parses the file and create a dictionary with the row numbers as keys (starting with rwo zero) and a list
    tuples with (column_nr,new_character) for the character substitutions on each row. THe default input filename is
    'mod.txt'"""
    try:
        with open(name) as f:
            mod_dict = dict()
            lines = f.readlines()
            for li in lines:
                m = li.strip().split(',')
                if m[0] in mod_dict:
                    mod_dict[m[0]].append((m[1], m[2]))
                else:
                    mod_dict[m[0]] = [(m[1], m[2])]
        return mod_dict
    except FileNotFoundError:
        sys.exit('Modification file not found')


PARSER = argparse.ArgumentParser(description='String modification file')
PARSER.add_argument('-d', type=str, help='Input directory', required=True)
PARSER.add_argument('-m', type=str, help='modification file', default='mod.txt')
ARGS = PARSER.parse_args()

modifications = mk_mod_dict(ARGS.m)
try:
    with os.scandir(ARGS.d) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                tmpFile = open('modFile.tmp', 'w')
                with open(entry) as infile:
                    all_lines = infile.readlines()
                    line_nr = 0
                    for line in all_lines:
                        if str(line_nr) in modifications.keys():
                            if modifications[str(line_nr)][0][0] == 'd':
                                line_nr += 1
                                continue
                            else:
                                for mod in modifications[str(line_nr)]:
                                    line = line[:int(mod[0])] + mod[1] + \
                                              line[int(mod[0]) + 1:]
                        tmpFile.write(line)
                        line_nr += 1
                    tmpFile.close()
                    infile.close()
                    copyfile('modFile.tmp', entry)
                    os.remove('modFile.tmp')

except FileNotFoundError:
    sys.exit("'{}' not found".format(ARGS.d))
except NotADirectoryError:
    sys.exit("'{}' is not a directory".format(ARGS.d))



