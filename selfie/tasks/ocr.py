#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Using a list of specimens' images, create a copy of their OCR-ed data.
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

import os, sys, argparse
import pandas as pd
from shutil import copyfile

from humain.constants import *
from humain.utils import *

if __name__ == '__main__':
	""" Using a list of specimens' images, create a copy of their OCR-ed data.
	"""
	parser = argparse.ArgumentParser("Using a list of specimens' images, create a copy of their OCR-ed data.")
	parser.add_argument('-id', '--ocr_input_dir', action="append", required=True, help="Directory with the OCR-ed data. Including the 'metrics' subdirectory.")
	parser.add_argument('-i', '--include', action="store", required=False, default=True, help="The files in specimen_lists will be copied when True and omitted when False.")
	parser.add_argument('-sl', '--specimens_list', action="store", required=True, help="TXT file with the list of specimens that will be OCR-ed (one per line).")
	parser.add_argument('-m', '--metric', action="append", required=True, help="One or more metrics that will be collected during the OCR execution.")	
	parser.add_argument('-od', '--output_dir', action="store", required=True, help="Directory where the OCR-ed values and metrics will be saved.")
	args = parser.parse_args()

	# Usage:
	# python3 ocr.py -id /home/ialzuru/Fall2019/HuMaIN_Simulator/datasets/aocr_herbs/ocr/gc-ocr -id /home/ialzuru/Fall2019/HuMaIN_Simulator/datasets/aocr_insects/ocr/gc-ocr -id /home/ialzuru/Fall2019/HuMaIN_Simulator/datasets/aocr_lichens/ocr/gc-ocr -i False -sl /home/ialzuru/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/specimen_list.txt -m duration -od /home/ialzuru/Fall2019/HuMaIN_Simulator/selfie/results/recorded_by/ocr

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
	#### INPUTS
	# args.ocr_input_dir
	for input_dir in args.ocr_input_dir:
		verify_dir( input_dir, 'The directory with the OCR-ed data (' + input_dir + ') was not found: ', parser, 1 )
		metrics_dir = input_dir + "/metrics"
		verify_dir( metrics_dir, 'The input metrics directory (' + metrics_dir + ') was not found: ', parser, 2 )
		for m_name in args.metric:
			metric_file = metrics_dir + "/" + m_name + ".csv"
			verify_file( metric_file, 'The metric file ' + metric_file + ' was not found in the metrics directory.', parser, 3 )
	# args.include
	arg_include = True
	if not (args.include.lower() in ['true', 'false']):
		print("\nERROR: Invalid value for the --include parameter. It must be True or False.\n")
		parser.print_help()
		sys.exit(4)
	else:
		if args.include.lower() == 'false':
			arg_include = False


	# args.specimens_list
	verify_file( args.specimens_list, 'The file with the list of specimens to OCR (' + args.specimens_list + ') was not found: ', parser, 5 )

	# args.output_dir
	verify_create_dir( args.output_dir, 'The output directory (' + args.output_dir + ') was not found and could not be created.', parser, 6 )
	verify_create_dir( args.output_dir + "/metrics", 'The metrics output directory (' + (args.output_dir  + "/metrics") + ') was not found and could not be created.', parser, 7 )
	
	################################################################################################################################
	# SPECIMENS SELECTION
	################################################################################################################################
	for input_dir in args.ocr_input_dir:
		# List of OCR-ed files in the input directory
		filenames = os.listdir( input_dir )
		ocred_files_list = list(f for f in filenames if f.endswith('.txt'))

		# List of files in the specimens list
		included_list = []
		with open(args.specimens_list, "r") as f:
			line = f.readline()
			while line:
				line = line.strip().replace('.jpg', '.txt')
				included_list += [line]
				line = f.readline()

		# Files to process
		ocred_files_set = set( ocred_files_list )
		included_set = set( included_list )
		selected_files_set = set()
		if arg_include:
			selected_files_set = included_set - ocred_files_set
		else:
			selected_files_set = ocred_files_set - included_set
		selected_files_list = list( selected_files_set )

		# Copy the OCR-ed files
		for filename in selected_files_list:
			copyfile(input_dir + "/" + filename, args.output_dir + "/" + filename)

		# Create the metric files and copy the correspondent values
		for m_name in args.metric:
			input_metric_file = input_dir + "/metrics/" + m_name + ".csv"
			df_m = pd.read_csv( input_metric_file, sep=',', names=['filename', 'metric_value'] )
			df_m = df_m.fillna('')
			# Copy just the right lines
			m_text = ""
			for index, row in df_m.iterrows():
				m_filename = row['filename'].replace('.jpg','.txt')
				if m_filename in selected_files_list:
					m_line = m_filename + "," + str(row['metric_value']) + "\n"
					m_text += m_line
			# Save the metric information (Incremental)
			output_metric_file = args.output_dir + "/metrics/" + m_name + ".csv"
			with open(output_metric_file, "a+") as f_m:
				f_m.write(m_text)
