#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import shutil

FTP = "ftp://ftp.ncbi.nlm.nih.gov/blast/db/"
LOG = "wgetlog.txt"
home = str(Path.home())
PARSER = argparse.ArgumentParser(description='download blast database files')
PARSER.add_argument('-f', type=str, help='output directory', default=home + '/wgetout/')
PARSER.add_argument('-b', type=str, help='basename', default='nt')
ARGS = PARSER.parse_args()
if os.path.isdir(ARGS.f):
    shutil.rmtree(ARGS.f)
os.mkdir(ARGS.f)
os.chdir(ARGS.f)
print('reading the number of {}-files at {}...'.format(ARGS.b, FTP))
command= 'wget -q ' + FTP + ARGS.b + '.*.tar.gz.md5'
os.system(command)
nr_of_files = len([name for name in os.listdir('.') if os.path.isfile(name)])
print('{} {}-files found'.format(nr_of_files, ARGS.b))
for i in range(nr_of_files):
    file = ARGS.b +'.' + str(i).zfill(2) + '.tar.gz'
    command = 'wget ' + FTP + file
    os.system(command)

