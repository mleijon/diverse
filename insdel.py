#! /usr/bin/python3

import argparse
import os
import sys
from shutil import copyfile


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
                tmpfile = open('modfile.tmp', 'w')
                with open(entry) as infile:
                    all_lines = infile.readlines()
                    line_nr = 0
                    for line in all_lines:
                        newline = ''
                        if str(line_nr) in modifications.keys():
                            newline = line
                            for mod in modifications[str(line_nr)]:
                                if mod[0] != 'd':
                                    newline = newline[:int(mod[0])] + mod[1] + \
                                              newline[int(mod[0]) + 1:]
                            if mod[0] != 'd':
                                tmpfile.write(newline)
                        if newline == '':
                            tmpfile.write(line)
                        line_nr += 1
                    tmpfile.close()
                    infile.close()
                    copyfile('modfile.tmp', entry)
                    os.remove('modfile.tmp')

except FileNotFoundError:
    sys.exit("'{}' not found".format(ARGS.d))
except NotADirectoryError:
    sys.exit("'{}' is not a directory".format(ARGS.d))



