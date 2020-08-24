import numpy.polynomial.polynomial as pol
from matplotlib import pyplot as plt
import linecache as lic
import argparse


def fig_plotter(ax, data1, data2, param_dict):
    out = ax.plot(data1, data2, **param_dict)
    return out


def get_dyes():
    dye_marker = 'Quantitative analysis of channel Cycling A.'
    dye_list = []
    li = lic.getline(ARGS.f, 1)
    i = 1
    while li != '':
        if dye_marker in li:
            dye_list.append((li[44:-11], i))
        i += 1
        li = lic.getline(ARGS.f, i)
    return dye_list


def get_last_row():
    line = ' '
    count = 1
    while line != '':
        line = lic.getline(ARGS.f, count)
        count += 1
    return count - 1


def find_lastid():
    count = 1
    idrow = 0
    last_row = get_last_row()
    while count < last_row + 1:
        if 'ID' in lic.getline(ARGS.f, count)[:5]:
            idrow = count
        count += 1
    return idrow


def find_nr_cycles():
    return get_last_row() - find_lastid() - 6


def read_rotorgene_data(input_file):

    data = dict()
    startrow_data = find_lastid() + 2
    nr_of_cycles = find_nr_cycles()
    for i in range(startrow_data, startrow_data + nr_of_cycles):
        line = lic.getline(input_file, i).replace(',', '.').replace('"', '').strip().split(';')
        for j in range(len(line)):
            data.setdefault(samples[j], []).append(float(line[j]))
    return data


def baseline_correct(uncorr_data):
    for sample in uncorr_data.keys():
        if sample == 'Cycle':
            continue
        for k in range(40):
            print(pol.polyval(
                    uncorr_data[samples[0]][k], pol.polyfit(
                        uncorr_data[samples[0]][0:5],
                        uncorr_data[sample][0:5], 1, full=False)))
            print(pol.polyfit(
                        uncorr_data[samples[0]][0:5],
                        uncorr_data[sample][0:5], 1, full=False))
            data_corrected.setdefault(sample, []).append(
                uncorr_data[sample][k] - pol.polyval(
                    uncorr_data[samples[0]][k], pol.polyfit(
                        uncorr_data[samples[0]][0:20],
                        uncorr_data[sample][0:20], 1, full=False)))
        #exit()
    return data_corrected


samples = []
linestyles = []
if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Baseline correct data')
    PARSER.add_argument('-f', type=str, help='input datafile', required=True)
    PARSER.add_argument('-l', action='store_true', help='switch for reading '
                                                        'labels from'
                                                        'labels.csv')
    ARGS = PARSER.parse_args()
    names_lines = []
    if ARGS.l:
        with open('labels.csv') as fi:
            names_lines += fi.read().split(',')
            samples = [x.split(';')[0] for x in names_lines]
            linestyles = [x.split(';')[1] for x in names_lines]
    else:
        samples += lic.getline(ARGS.f, find_lastid()
                               ).replace('"', '').strip().split(';')[1:]
        linestyles += '-'*len(samples)
    read_rotorgene_data(ARGS.f)
    data_corrected = dict()
    uncorr_data = read_rotorgene_data(ARGS.f)
    corr_data = baseline_correct(uncorr_data)
    if len(get_dyes()) == 1:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Rispens Assay version 3')
    elif len(get_dyes()) == 2:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Rispens Assay version 3')
    for j in range(1, len(samples)):
        fig_plotter(ax1, uncorr_data[samples[0]], corr_data[samples[j]],
                    {'ls': linestyles[j]})
        fig_plotter(ax2, uncorr_data[samples[0]], uncorr_data[samples[j]],
                    {'ls': linestyles[j]})
    for axis in (ax1, ax2):
        axis.set(title=get_dyes()[0][0])
        axis.legend(samples[1:], loc='best')
        axis.set(xlabel='Cycle')
        axis.set(ylabel='Fluorescence')
        axis.grid()
        axis.set_xlim([1, find_nr_cycles()])
    plt.show()
