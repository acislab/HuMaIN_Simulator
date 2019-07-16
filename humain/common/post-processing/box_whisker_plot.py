#!/usr/bin/env python3
import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
# agg backend is used to create plot as a .png file
mpl.use('agg')


def plot_box_whisker(data_to_plot):
    # # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))
    # # Create an axes instance
    ax = fig.add_subplot(111)
    # Create the boxplot - filled color
    bp = ax.boxplot(data_to_plot, patch_artist=True)
    # Save the figure
    fig.savefig('box_plot_fig.png', bbox_inches='tight')


if __name__ == '__main__':
    """ Creates a box whisker plot.
    """
    parser = argparse.ArgumentParser("Creates a box whisker plot.")
    parser.add_argument('-f', '--files', action="append",
                        required=True, help="Files to import values from")
    args = parser.parse_args()

    data_to_plot = []

    for f in args.files:
        values = []
        with open(f, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                values.append(row[1])
            values = np.array(values).astype(np.float)
        data_to_plot.append(values)

    plot_box_whisker(data_to_plot)
