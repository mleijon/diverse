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
    print(dye_list)
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

    dye_data = dict()
    data = dict()
    nr_of_cycles = find_nr_cycles()
    for dye in get_dyes():
        startrow_data = dye[1] + 4
        for i in range(startrow_data, startrow_data + nr_of_cycles):
            line = lic.getline(input_file, i).replace(',', '.').replace('"', '').strip().split(';')
            for j in range(len(line) - 1):
                dye_data.setdefault(samples[j], []).append(float(line[j]))
        data.update({dye[0]: dye_data})
        dye_data = {}
    return data


def baseline_correct(uncorr_data, bl_def):
    data_corr = dict()
    for sample in uncorr_data.keys():
        if sample == 'Cycle':
            continue
        for k in range(40):
            data_corr.setdefault(sample, []).append(
                uncorr_data[sample][k] - pol.polyval(
                    uncorr_data[samples[0]][k], pol.polyfit(
                        uncorr_data[samples[0]][bl_def[0]:bl_def[1]],
                        uncorr_data[sample][bl_def[0]:bl_def[1]], bl_def[2], full=False)))
    return data_corr


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
    uncorr_data = read_rotorgene_data(ARGS.f)
    corrected_data = dict()
    i = 0
    baseline_definition = dict()
    baseline_definition[get_dyes()[0][0]] = (3, 15, 1)
    #baseline_definition[get_dyes()[1][0]] = (3, 15, 1)
    for key in uncorr_data.keys():
        corrected_data.update({key: baseline_correct(uncorr_data[key],
                                                     baseline_definition[key])})
    if len(get_dyes()) == 1:
        fig, axs = plt.subplots(1, 2)
        for j in range(1, len(samples) - 1):
            fig_plotter(axs[1], uncorr_data[get_dyes()[0][0]][samples[0]],
                        corrected_data[get_dyes()[0][0]][samples[j]],
                        {'ls': linestyles[j]})
            fig_plotter(axs[0], uncorr_data[get_dyes()[0][0]][samples[0]],
                        uncorr_data[get_dyes()[0][0]][samples[j]],
                        {'ls': linestyles[j]})
        axs[0].set_title(get_dyes()[0][0] + ' (uncorrected)')
        axs[1].set_title(get_dyes()[0][0] + ' (corrected)')
    elif len(get_dyes()) == 2:
        fig, axs = plt.subplots(2, 2)
        for j in range(1, len(samples)):
            for dye in range(len(get_dyes())):
                fig_plotter(axs[dye, 1], uncorr_data[get_dyes()[dye][0]][samples[0]],
                            corrected_data[get_dyes()[dye][0]][samples[j]],
                            {'ls': linestyles[j]})
                fig_plotter(axs[dye, 0], uncorr_data[get_dyes()[dye][0]][samples[0]],
                            uncorr_data[get_dyes()[dye][0]][samples[j]],
                            {'ls': linestyles[j]})
                axs[dye, 0].set_title(get_dyes()[dye][0] + ' (uncorrected)')
                axs[dye, 1].set_title(get_dyes()[dye][0] + ' (corrected)')
    else:
        exit('More than two dyes not suppported')
    for axis in axs.flat:
        axis.legend(samples[1:], prop={'size': 7})
        axis.set(xlabel='Cycle')
        axis.set(ylabel='Fluorescence')
        axis.grid()
        axis.set_xlim([1, find_nr_cycles()])
    fig.suptitle('Rispens Assay version 2')
    fig.tight_layout(pad=0.1)
    plt.show()
