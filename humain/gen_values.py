#!/usr/bin/env python3

##########################################################################################
# Developers: 	Aditi Malladi and Icaro Alzuru
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Generates values for each file in a given directory or generates a value
# 				for each filename in a input csv
##########################################################################################
# Copyright 2019    Advanced Computing and Information Systems (ACIS) Lab - UF
#                   (https://www.acis.ufl.edu/)
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file 
# except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the 
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
# either express or implied. See the License for the specific language governing permissions 
# and limitations under the License.
##########################################################################################

import os, sys, argparse, random, csv
from humain.utils import *

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
	# python3 ~/Fall2019/HuMaIN_Simulator/humain/gen_values.py -d ~/Fall2019/HS_HITL/ocr/bio01 -e txt -g 20.3,19.7 -o ~/Fall2019/HuMaIN_Simulator/datasets/bioset10/crowd/metrics/bio01_1.csv
	
	# File can take input of file or directory of files
	# File input should be of the format filename, value where the delimiter used is ","

	################################################################################################################################
	# ARGUMENTS VALIDATIONS

	# args.constant, args.range, args.gauss
	if (not (args.constant or args.range or args.gauss)):
		print( "\nERROR: The distribution to generate the random values was not specified.\n" )
		sys.exit( 3 )

	# args.output_file
	verify_create_file( args.output_file, 'The output file could not be created.', parser, 4 )

	################################################################################################################################
	# Verify and extract filenames from file/directory
	filename_list = []

	if os.path.isdir(args.directory):
		# verify dir
		verify_dir( args.directory, "The input directory was not found.", parser, 1 )
		# verify ext
		if not verify_dir_ext( args.directory, args.extension ):
			print( "\nERROR: There are no files with extension " + args.extension + " in the source directory (" + args.directory + ").\n" )
			sys.exit( 2 )

		filenames = os.listdir(args.directory)
		filename_list = list(f for f in filenames if f.endswith('.txt'))
	else:
		# verify file
		verify_file(args.directory, "The input file was not found.", parser, 1)
		# verify extension
		verify_file_ext(args.directory, args.extension)
		#extract filename list
		with open(args.directory, newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter='\t')
			for row in spamreader:
				filename_list.append(row[0])
	
	# Number of files
	n = len(filename_list)
	print("Number of files found:", n)


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
