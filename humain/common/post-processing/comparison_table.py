#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os, sys, csv, argparse, ntpath


def create_table():
    new_dataset = np.column_stack(data_to_plot)
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    df = pd.DataFrame(new_dataset, columns=data_objects)
    ax.table(cellText=df.values, colLabels=df.columns)
    if args.title:
        plt.title(args.title)
    try:
        fig.savefig(args.output_file)
    except:
        print("\nERROR: The output image file was not created successfully. Please use a valid extension (.png) and path.\n")
        sys.exit(1)


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
        print(ntpath.basename(f), sum)
        data_to_plot.append(str(sum))
    create_table()


if __name__ == '__main__':
    """ Creates comparison table between the files inputted.
    """
    parser = argparse.ArgumentParser("Creates a comparison bar graph")
    parser.add_argument('-f', '--files', action="append", required=True, help="Title of comparison table")
    parser.add_argument('-t', '--title', action="store", required=False, help="Title for the comparison", type=str)
    parser.add_argument('-a', '--aggr', action="store", required=False, help="Aggregation type sum or average, default is taken to be average", type=str)
    parser.add_argument('-o', '--output_file', action="store", required=True, help="File with the list of files and randomly generated values.")

    args = parser.parse_args()
    data_to_plot = []
    data_objects = []

    average = True
    if args.aggr and args.aggr.lower() == "sum":
        average = False
    read_files()


# Takes csv files with file names and single row with value sepearted by "," delimiter
# Can take multiple files
# usage: python3 common/post-processing/comparison_table.py -f duration.csv -f duration.csv -t HelloWorld -o output.png
