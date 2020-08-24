import numpy.polynomial.polynomial as pol
from matplotlib import pyplot as plt
import linecache as lic
import argparse


def fig_plotter(ax, data1, data2, param_dict):
    out = ax.plot(data1, data2, **param_dict)
    return out


def read_rotorgene_data(input_file):

    def get_last_row():
        line = ' '
        count = 1
        while line != '':
            line = lic.getline(input_file, count)
            count += 1
        return count - 1

    def find_lastid():
        count = 1
        idrow = 0
        last_row = get_last_row()
        while count < last_row + 1:
            if 'ID' in lic.getline(input_file, count)[:5]:
                idrow = count
            count += 1
        return idrow

    def find_nr_cycles():
        ch = '*'
        row = find_lastid() + 2
        while ch not in {'', ' ', '\n'}:
            ch = lic.getline(input_file, row)[:1]
            row += 1
        nr_of_cycles = int((lic.getline(input_file, row - 2).split(';')[0].replace('"', '')))
        return nr_of_cycles

    data = dict()
    data_keys = ['Cycle']
    data_keys += lic.getline(input_file, find_lastid()
                             )[1:-2].split('";"')[1:]
    startrow_data = find_lastid() + 2
    nr_of_cycles = find_nr_cycles()
    for i in range(startrow_data, startrow_data + nr_of_cycles):
        line = lic.getline(input_file, i).replace(',', '.').replace('"', '').strip().split(';')
        print(line)
        for j in range(len(line)):
            data.setdefault(data_keys[j], []).append(float(line[j]))
    return data


def baseline_correct(uncorr_data):
    for sample in uncorr_data.keys():
        if sample == 'Cycle':
            continue
        for k in range(40):
            data_corrected.setdefault(sample, []).append(
                uncorr_data[sample][k] - pol.polyval(
                    uncorr_data['Cycle'][k], pol.polyfit(
                        uncorr_data['Cycle'][5:14],
                        uncorr_data[sample][5:14], 2, full=False)))
    return data_corrected


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Baseline correct data')
    PARSER.add_argument('-f', type=str, help='input datafile', required=True)
    ARGS = PARSER.parse_args()
    read_rotorgene_data(ARGS.f)
    data_corrected = dict()
    uncorr_data = read_rotorgene_data(ARGS.f)
    corr_data = baseline_correct(uncorr_data)
    samples = list(uncorr_data.keys())


fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Rispens Assay version 2')
fig_plotter(ax1, uncorr_data[samples[0]], corr_data[samples[1]], {'ls': '-'})
fig_plotter(ax2, uncorr_data[samples[0]], uncorr_data[samples[1]], {'ls': '-'})
for j in range(2, 6):
    fig_plotter(ax1, uncorr_data[samples[0]], corr_data[samples[j]],
                {'ls': '--'})
    fig_plotter(ax2, uncorr_data[samples[0]], uncorr_data[samples[j]],
                {'ls': '--'})
for j in range(6, len(samples) - 1):
    fig_plotter(ax1, uncorr_data[samples[0]], corr_data[samples[j]],
                {'ls': '-.'})
    fig_plotter(ax2, uncorr_data[samples[0]], uncorr_data[samples[j]],
                {'ls': '-.'})
fig_plotter(ax1, uncorr_data[samples[0]], corr_data[samples[8]],
            {'ls': 'dotted'})
fig_plotter(ax2, uncorr_data[samples[0]], uncorr_data[samples[8]],
            {'ls': 'dotted'})
for axis in (ax1, ax2):
    axis.legend(samples[1:], loc='lower left')
    axis.set(xlabel='Cycle')
    axis.set(ylabel='Fluorescence')
    axis.grid()
    axis.set_xlim([1, 40])
plt.show()
