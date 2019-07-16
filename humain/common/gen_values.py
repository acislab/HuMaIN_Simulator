#!/usr/bin/env python3
import argparse
import random
import os
from constants import *

# Create file
# TODO: Change the destination directory of where the output file should be stored
def create_file(filename):
    open(os.path.join(PROJECTS_DIR, filename), 'w+')

# Assign a constant value to each file
def constant_value(value):
    create_file("random_value.txt")
    f = open("random_value.txt", "w+")
    for i in range(len(filename_list)):
        f.write(filename_list[i]+", %f\r\n" % value)
    f.close()


# Generate a random value within a given range
def range_value(value):
    arg_list = value.split(",")
    # get list of integers
    arg_list = [int(x) for x in arg_list]
    create_file("random_value.txt")
    f = open("random_value.txt", "w+")
    for i in range(len(filename_list)):
        f.write(filename_list[i]+", %f\r\n" % (random.uniform(arg_list[0], arg_list[1])))
    f.close()


# Generate random value using Gaussian Distribution
def gauss_value(value):
    arg_list = value.split(",")
    # get list of integers
    arg_list = [int(x) for x in arg_list]
    create_file("random_value.txt")
    f = open("random_value.txt", "w+")
    for i in range(len(filename_list)):
        f.write(filename_list[i]+", %f\r\n" % (random.gauss(arg_list[0], arg_list[1])))
    f.close()


if __name__ == '__main__':
    """ Creates a new file and copies into a new file if required.
    """
    parser = argparse.ArgumentParser("Creates a new project file.")
    parser.add_argument('-c', '--constant', action="store",
                        required=False, help="Enter the constant value", type=float)
    parser.add_argument('-r', '--range', action="store",
                        required=False, help="Generate value at random. Enter range min,max", type=str)
    parser.add_argument('-g', '--gauss', action="store",
                        required=False, help="Generate value at random using the Gaussian distribution. Enter mean,sigma", type=str)
    parser.add_argument('-d', '--directory', action="store",
                        required=True, help="Directory with data files")
    args = parser.parse_args()

    # Create the list of files to process
    filenames = os.listdir(args.directory)
    filename_list = list(f for f in filenames if f.endswith('.txt'))

    if args.constant:
        # print("Constant", args.constant)
        constant_value(args.constant)
    elif args.random:
        # print("Random: ", args.random)
        range_value(args.range)
    elif args.gauss:
        # print("Random: ", args.gauss)
        gauss_value(args.gauss)
