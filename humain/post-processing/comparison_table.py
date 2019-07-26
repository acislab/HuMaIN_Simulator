#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import csv
import argparse
import ntpath


def table_plot():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    y = np.column_stack(data_to_plot)
    col_labels = args.column

    # Draw table
    plt.title(args.title, fontsize=24)
    the_table = plt.table(cellText=y,
                          colWidths=[0.2] * 3,
                          colLabels=col_labels,
                          loc='center', cellLoc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(20)
    the_table.scale(3, 3)

    # Removing ticks and spines enables you to get the figure only with table
    plt.tick_params(axis='x', which='both', bottom=False,
                    top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', right=False,
                    left=False, labelleft=False)
    for pos in ['right', 'top', 'bottom', 'left']:
        plt.gca().spines[pos].set_visible(False)
    plt.savefig(args.output_file, bbox_inches='tight', pad_inches=0.05)


def read_files():
    for f in args.files:
        data_objects.append(ntpath.basename(f).split(".")[0])
        sum = 0
        value = 0
        with open(f, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                sum = sum + float(row[1])
                value = value + 1
        if average:
            sum = sum / value
        # print(ntpath.basename(f), sum)
        sum = round(sum, 4)
        data_to_plot.append(str(sum))
    table_plot()
    # trual()


if __name__ == '__main__':
    """ Creates comparison table between the files inputted.
    """
    parser = argparse.ArgumentParser("Creates a comparison bar graph")
    parser.add_argument('-f', '--files', action="append",
                        required=True, help="Files to generate table from")
    parser.add_argument('-c', '--column', action="append",
                        required=True, help="Column name to appear in the file table (to be inputted in the same order as the files)")
    parser.add_argument('-t', '--title', action="store",
                        required=False, help="Title for the comparison", type=str)
    parser.add_argument('-a', '--aggr', action="store", required=False,
                        help="Aggregation type sum or average, default is taken to be average", type=str)
    parser.add_argument('-o', '--output_file', action="store", required=True,
                        help="File with the list of files and randomly generated values.")

    args = parser.parse_args()
    data_to_plot = []
    data_objects = []

    average = True
    if args.aggr and args.aggr.lower() == "sum":
        average = False
    read_files()


# Takes csv files with file names and single row with value sepearted by "," delimiter
# Can take multiple files
# usage: python3 post-processing/comparison_table.py -f duration.csv -f duration.csv -t HelloWorld -o output.png
# python3 post-processing/comparison_table.py -f duration.csv -f duration.csv -c Event_Date -c Test -t HelloWorld -o ~/Desktop/HuMaIN_Simulator/selfie/output.png
