#!/usr/bin/python


with open('svaresult.txt') as fii, open('svaresultt.txt', 'w') as fio:
    for line in fii:
        fio.write(line.replace(' No hit', '\tNo hit', 1))


