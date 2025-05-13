import re
import os
import numpy as np
import matplotlib.pyplot as plt


def read_last_lines(filename, num_lines):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return lines[-num_lines:]
    except FileNotFoundError:
        return f"Error: File '{filename}' not found."
    except Exception as e:
        return f"An error occurred: {e}"


def split_string_multiple_separators(text, separators):
    regex_pattern = '|'.join(map(re.escape, separators))
    return re.split(regex_pattern, text)


def list_files_recursive(path):
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_paths.append(file_path)
    return file_paths


def plot_figure(method1, method1_name, method2, method2_name):
    values1 = method1.get(1)
    values2 = method2.get(1)

    fig, ax = plt.subplots()
    ax.axline((0, 0), slope=1, color='gray')
    ax.scatter(values1, values2, s=5)
    max_lim = np.asarray(values1 + values2).max()
    plt.xlim(xmax=max_lim, xmin=0)
    plt.ylim(ymax=max_lim, ymin=0)
    fig.set_size_inches([10, 10])
    plt.xlabel(method1_name)
    plt.ylabel(method2_name)
    plt.savefig(directory + method1_name + '_vs_' + method2_name + '_1.png')


BASELINE = {}
BILINEAR = {}
HYBRID = {}
ORIGINPLUS = {}

directory = 'transformers/'
files = list_files_recursive(directory)

num_lines = 60
for file in files:
    if file.__contains__('.out'):
        print(file)
        last_lines = read_last_lines(file, num_lines)

        positions = []
        radii = []
        separators = ['(', ',', ')']
        for line in last_lines:
            _, position, radius, _ = split_string_multiple_separators(line, separators)
            positions.append(int(position))
            radii.append(float(radius))

        if file.__contains__('baseline'):
            if file.__contains__('1'):
                BASELINE[1] = radii
            elif file.__contains__('2'):
                BASELINE[2] = radii
            elif file.__contains__('3'):
                BASELINE[3] = radii
        elif file.__contains__('bilinear'):
            if file.__contains__('1'):
                BILINEAR[1] = radii
            elif file.__contains__('2'):
                BILINEAR[2] = radii
            elif file.__contains__('3'):
                BILINEAR[3] = radii
        elif file.__contains__('hybrid'):
            if file.__contains__('1'):
                HYBRID[1] = radii
            elif file.__contains__('2'):
                HYBRID[2] = radii
            elif file.__contains__('3'):
                HYBRID[3] = radii
        elif file.__contains__('originPlus'):
            if file.__contains__('1'):
                ORIGINPLUS[1] = radii
            elif file.__contains__('2'):
                ORIGINPLUS[2] = radii
            elif file.__contains__('3'):
                ORIGINPLUS[3] = radii


plot_figure(BASELINE, 'baseline', BILINEAR, 'bilinear')
plot_figure(BASELINE, 'baseline', ORIGINPLUS, 'originPlus')
plot_figure(BASELINE, 'baseline', HYBRID, 'hybrid')

plot_figure(ORIGINPLUS, 'originPlus', BILINEAR, 'bilinear')
plot_figure(HYBRID, 'hybrid', BILINEAR, 'bilinear')
plot_figure(HYBRID, 'hybrid', ORIGINPLUS, 'originPlus')


print('done')
