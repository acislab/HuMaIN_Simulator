#!/usr/bin/env python3
import argparse, csv, sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
# agg backend is used to create plot as a .png file
mpl.use('agg')


def plot_box_whisker(data_to_plot):
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_to_plot, patch_artist=True)
    try:
        fig.savefig(args.output_file, bbox_inches='tight')
    except:
        print("\nERROR: The output image file was not created successfully. Please use a valid extension for an image (e.g .png) and path.\n")
        sys.exit(1)


def read_files():
    for f in args.files:
        values = []
        with open(f, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                temp = 0
                for val in row[1:]:
                    temp = temp + float(val)
                values.append(temp)
            values = np.array(values).astype(np.float)
        data_to_plot.append(values)

    plot_box_whisker(data_to_plot)


if __name__ == '__main__':
    """ Creates a box whisker plot. Takes input of .csv files sepearted by "," delimiter.
    """
    parser = argparse.ArgumentParser("Creates a box whisker plot.")
    parser.add_argument('-f', '--files', action="append",
                        required=True, help="Files to import values from")

    parser.add_argument('-o', '--output_file', action="store",
                        required=True, help="Output box plot image to be saved")
    args = parser.parse_args()

    data_to_plot = []

    # Can pass one or multiple files to combine
    # Can pass files with multiple rows - all values of each row will be added before generating box plot
    read_files()


# usage: python3 common/post-processing/box_whisker_plot.py -f duration_multiple.csv
# usage: python3 common/post-processing/box_whisker_plot.py -f duration.csv
# usage: python3 common/post-processing/box_whisker_plot.py -f duration.csv -f duration_multiple.csv
