#!/usr/bin/env python3
import os, sys, argparse
import random

from utils import *

# Assign a constant value to each file
def constant_value( value, n ):
	values = []
	try:
		values = [ float(value) ] * n
	except ValueError:
		print( "\nERROR: The specified constant value could not be converted to float.\n" )
		sys.exit( 6 )
	return(values)

# Generate a random value within a given range
def range_value( value, n ):
	values = []
	start, end = None, None
	try:
		start, end = [float(x) for x in value.split(',')]
	except ValueError:
		print( "\nERROR: A , was not found or the values or the range could not be converted to float.\n" )
		sys.exit( 7 )

	dif = end - start
	for j in range(n): 
		values.append( start + (dif * random.random()) ) 
	return values 

# Generate random value using Gaussian Distribution
def gauss_value( value, n ):
	values = []
	mean, sigma = None, None
	try:
		mean, sigma = [float(x) for x in value.split(',')]
	except ValueError:
		print( "\nERROR: A , was not found or the mean and sigma values could not be converted to float.\n" )
		sys.exit( 7 )
	
	for j in range(n): 
		values.append( random.gauss(mean, sigma) ) 
	return values 


if __name__ == '__main__':
	""" Generate random values for the files in a directory.
	"""
	parser = argparse.ArgumentParser("Generate random values for the files in a directory.")
	parser.add_argument('-d', '--directory', action="store", required=True, help="Directory with data files")
	parser.add_argument('-e', '--extension', action="store", required=True, help="Extension of the files to consider. e.g.: txt, tsv")
	parser.add_argument('-c', '--constant', action="store", required=False, help="Enter the constant value", type=float)
	parser.add_argument('-r', '--range', action="store", required=False, help="Generate value at random. Enter range min,max", type=str)
	parser.add_argument('-g', '--gauss', action="store", required=False, help="Generate value at random using the Gaussian distribution. Enter mean,sigma", type=str)
	parser.add_argument('-o', '--output_file', action="store", required=True, help="File with the list of files and randomly generated values.")
	args = parser.parse_args()
	# Usage:
	# python3 ./gen_values.py -d ~/Summer2019/HuMaIN_Simulator/datasets/aocr_insects/ocr/ocropus -e txt -g 3,0.2 -o ~/test.csv

	################################################################################################################################
	# ARGUMENTS VALIDATIONS

	# args.directory 
	verify_dir( args.directory, "The input directory was not found.", parser, 1 )

	# args.extension
	if not verify_dir_ext( args.directory, args.extension ):
		print( "\nERROR: There are no files with extension " + args.extension + " in the source directory (" + args.directory + ").\n" )
		sys.exit( 2 )

	# args.constant, args.range, args.gauss
	if (not (args.constant or args.range or args.gauss)):
		print( "\nERROR: The distribution to generate the random values was not specified.\n" )
		sys.exit( 3 )

	# args.output_file
	verify_create_file( args.output_file, 'The output file could not be created.', parser, 4 )

	################################################################################################################################
	# Create the list of files to process
	filenames = os.listdir(args.directory)
	filename_list = list(f for f in filenames if f.endswith('.txt'))
	# Number of files
	n = len(filename_list)

	################################################################################################################################
	# Get the list of values
	values_list = []
	if args.constant:
		# print("Constant", args.constant)
		values_list = constant_value( args.constant, n )
	elif args.range:
		# print("Random: ", args.random)
		values_list = range_value( args.range, n )
	elif args.gauss:
		# print("Random: ", args.gauss)
		values_list = gauss_value( args.gauss, n)

	if len(values_list) != n:
		print( "\nERROR: Incomplete generation of the random values.\n" )
		sys.exit( 5 )

	################################################################################################################################
	# Save the values in the file
	file_text = ""
	for i in range(n):
		file_text += filename_list[i] + ", " + str(values_list[i]) + "\n"

	with open( args.output_file, "w+" ) as f:
		f.write( file_text )
