#!/usr/bin/python
#testfi = open('test.txt', 'w')
readfi = open('foodPT2018.fastq')
salfi = open('salhits.txt')
nosalfi = open('non_salhits.txt')
svaresult = open('svaresult.txt', 'w')
namelist = []
sallist = []
nosallist = []
for line in readfi:
    if line[0:8] == '@fpt2018':
        namelist.append(line[8:].lstrip('0').strip())
for line in salfi:
    sallist.append(line.split()[0][7:].lstrip('0'))
for line in nosalfi:
    nosallist.append(line.split()[0][7:].lstrip('0'))
salfi.seek(0)
nosalfi.seek(0)
current_nosal = nosalfi.readline()
current_nosal_nr = int(current_nosal.split()[0][7:].lstrip('0'))
current_sal = salfi.readline()
current_sal_nr = int(current_sal.split()[0][7:].lstrip('0'))
eof_sal = False
eof_nosal = False
for count in namelist:
    if count in sallist and not eof_sal:
        svaresult.write(current_sal)
        sallist.remove(count)
        current_sal = salfi.readline()
        if current_sal == '':
            eof_sal = True
        else:
            current_sal_nr = int(current_sal.split()[0][7:].lstrip('0'))
        continue
    if count in nosallist and not eof_nosal:
        svaresult.write(current_nosal)
        nosallist.remove(count)
        current_nosal = nosalfi.readline()
        if current_nosal == '':
            eof_nosal = True
        else:
            current_nosal_nr = int(current_nosal.split()[0][7:].lstrip('0'))
        continue
    if (count not in sallist) and (count not in nosallist):
        svaresult.write('fpt2018'+str(count).zfill(8)+' No hit\n')
salfi.close()
nosalfi.close()
svaresult.close()