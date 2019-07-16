#!/usr/bin/env python3
import ntpath
import numpy as np
import argparse
import csv
import matplotlib.pyplot as plt

# Create the bar graph
def create_graph():
    x_pos = [i for i, _ in enumerate(data_objects)]
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    ax.bar(x_pos, data_to_plot, color='green')
    if args.title:
        plt.title(args.title)
    fig.savefig('bar_graph_fig.png')


if __name__ == '__main__':
    """ Creates comparison table between the files inputted.
    """
    parser = argparse.ArgumentParser("Creates a comparison bar graph")
    parser.add_argument('-f', '--files', action="append",
                        required=True, help="Title of comparison table")
    parser.add_argument('-t', '--title', action="store",
                        required=False, help="Title for the comparison", type=str)
    parser.add_argument('-a', '--aggr', action="store", required=False,
                        help="Aggregation type sum or average, default is taken to be average", type=str)
    args = parser.parse_args()

    data_to_plot = []
    data_objects = []

    average = True
    if args.aggr.lower() == "sum":
        average = False

    # Read in all the files and calucate sum or average
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
        data_to_plot.append(sum)
        create_graph()
