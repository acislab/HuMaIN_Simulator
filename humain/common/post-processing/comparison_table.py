#!/usr/bin/env python3
import ntpath
import numpy as np
import argparse
import csv
import matplotlib.pyplot as plt
import pandas as pd


def create_table():
    new_dataset = np.column_stack(data_to_plot)
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    df = pd.DataFrame(new_dataset, columns=data_objects)
    ax.table(cellText=df.values, colLabels=df.columns)
    # fig.tight_layout()
    fig.savefig('comparison_table.png')
    # plt.show()


if __name__ == '__main__':
    """ Creates comparison table between the files inputted.
    """
    parser = argparse.ArgumentParser("Creates a comparison bar graph")
    parser.add_argument('-f', '--files', action="append",
                        required=True, help="Title of comparison table")
    parser.add_argument('-t', '--title', action="store",
                        required=False, help="Title for the comparison", type=str)
    parser.add_argument('-a', '--aggr', action="store", required=True,
                        help="Aggregation type sum or average", type=str)
    args = parser.parse_args()

    data_to_plot = []
    data_objects = []

    average = False
    if args.aggr == "average":
        average = True

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
        data_to_plot.append(str(sum))
    create_table()
