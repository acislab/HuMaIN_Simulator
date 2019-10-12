#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Given the tsv file with the crowdsourced data from 3 users or more per 
#               image, generates a file with the three values in a single line.
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

##############################################################################################################################################################
if __name__ == '__main__':
	""" MAIN """
	# Read arguments
	parser = argparse.ArgumentParser("Given the tsv file with the crowdsourced data from 3 users or more per image, generates a file with the three values in a single line.")
	parser.add_argument('-i','--input_file',action="store", required=True, help="Text file with the crowdsourced data.")
	parser.add_argument('-t','--term',action="store", required=False, help="Name of the term.")
	parser.add_argument('-o','--output_file',action="store", required=True, help="Output text file with a single line per filename and the consensual values.")
	args = parser.parse_args()
	# Use:
	# python3 convert_crowd_one_line.py -i /home/ialzuru/Fall2019/HS_HITL/crowd/wdb_blueberries.tsv -t recordedBy -o /home/ialzuru/Fall2019/HS_HITL/crowd_recorded_by/wdb_blueberries.tsv

	##########################################################################################
	# The existence of the source file is verified
	if ( not os.path.isfile( args.input_file ) ):
		print('Error: Input data file does not exist.\n')
		parser.print_help()
		sys.exit(1)

	# Load the input data 
	df_input = pd.read_csv( args.input_file, sep='\t')
	df_input.fillna('', inplace= True)
	
	# Create the output dataframe
	df_rb = df_input[['filename', args.term]].copy()

	# Group by filename and save the values in the same line
	output_text = ""
	groupby = df_rb.groupby(["filename"])
	for filename, group in groupby:
		line = filename
		values_list = group[ args.term ].values.tolist()
		i = 0
		while i < len(values_list):
			line += "\t" + values_list[i]
			i = i + 1
		if i < 3:
			line += "\t"
			i = i + 1
		line += "\n"
		output_text += line

	# Save the new format in the output file
	with open( args.output_file, "w+") as f_o:
		f_o.write( output_text )
