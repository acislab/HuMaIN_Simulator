#!/usr/bin/env python3
import numpy as np
import csv, argparse, ntpath, sys
import matplotlib.pyplot as plt


# Create the bar graph
def create_graph():
    x_pos = [i for i, _ in enumerate(data_objects)]
    fig = plt.figure(1, figsize=(5, 4))
    plt.style.use('ggplot')  
    ax = fig.add_subplot(111)
    ax.bar(x_pos, data_to_plot, color='#B159D5', width=0.25, align = 'center')
    
    if args.title:
        plt.title(args.title)
    try:
        fig.savefig(args.output_file)
    except:
        print("\nERROR: The output image file was not created successfully. Please use a valid extension (.png) and path.\n")
        sys.exit(1)


# Read in all the files and calucate sum or average
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
        data_to_plot.append(sum)
        create_graph()

# Main
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

# Takes in single and multiple files
# Generates Useful graph for multiple files, for single file not uselful data visualization
# usage: python3 post-processing/comparison_bar_graph.py -f duration.csv -f duration.csv -f duration.csv -t Duration!!!! -a sum -o output_bar.png