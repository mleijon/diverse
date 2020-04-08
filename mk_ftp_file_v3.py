#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import shutil
import threading


def transfer(com):
    os.system(com)
    return


FTP = "ftp://ftp.ncbi.nlm.nih.gov/blast/db/"
LOG = "wgetlog.txt"
home = str(Path.home())
PARSER = argparse.ArgumentParser(description='download blast database files')
PARSER.add_argument('-f', type=str, help='output directory',
                    default=home + '/wgetout/')
PARSER.add_argument('-b', type=str, help='basename', default='nt')
ARGS = PARSER.parse_args()
if os.path.isdir(ARGS.f):
    shutil.rmtree(ARGS.f)
os.mkdir(ARGS.f)
os.chdir(ARGS.f)
print('Getting the number of {}-files at {}...'.format(ARGS.b, FTP))
command = 'wget -q -nc ' + FTP + ARGS.b + '.*.tar.gz.md5'
thread = threading.Thread(target=transfer(command))
thread.start()
thread.join()
nr_of_files = len([name for name in os.listdir('.') if os.path.isfile(name)])
print('{} {}-files found'.format(nr_of_files, ARGS.b))
for i in range(nr_of_files):
    file = ARGS.b + '.' + str(i).zfill(2) + '.tar.gz'
    print('\rProcessing: {} ({}/{})'.format(file, i + 1, nr_of_files), end='', flush=True)
    command = 'wget -nc -q ' + FTP + file + '; md5sum -c ' \
              + file + '.md5 >> wget.log; tar -xzf ' + file +'; rm ' + file
    thread = threading.Thread(target=transfer(command))
    thread.start()
    thread.join()
