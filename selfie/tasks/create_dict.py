#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Creates or augments a wordcount dictionary (eliminating all the special 
# 				characters) from some TSV (specimen, value) file
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

import os, sys, argparse, re
import pandas as pd

from humain.constants import *
from humain.utils import *

##############################################################################################################################################################
if __name__ == '__main__':
	""" Creates or augments a wordcount dictionary (eliminating all the special characters) from some TSV (specimen, value) file.
	""" 
	# Read arguments
	parser = argparse.ArgumentParser("Creates or augments a wordcount dictionary (eliminating all the special characters) from some TSV (specimen, value) file.")
	parser.add_argument('-i','--data_file',action="store", required=True, help="Input TSV file with the unnamed columns: 'specimen', 'value'.")
	parser.add_argument('-o','--dict_file',action="store", required=True, help="Name of the TSV dictionary file to generate. Unnamed columns: 'value', 'frequency'.")	
	args = parser.parse_args()
	# Usage example:
	# python3 created_dict.py -i /home/ialzuru/Fall2019/HuMaIN_Simulator/selfie/results/recorded_by_hitl/iteration_1/consensus/accepted/accepted.tsv -o /home/ialzuru/Fall2019/HuMaIN_Simulator/selfie/results/recorded_by_hitl/iteration_1/create_dict/dictionary.tsv

	##########################################################################################
	# PARAMETERS VERIFICATION
	# args.data_file
	verify_file( args.data_file, 'The data file (' + args.data_file + ') was not found.', parser, 1 )

	# args.dict_file
	dict_path = os.path.dirname( args.dict_file )
	verify_create_dir( dict_path, 'The directory for the dictionary file (' + dict_path + ') could not be created.', parser, 2 )
	verify_create_file( args.dict_file, 'The dictionary file (' + args.dict_file + ') cannot be created in the specified path.', parser, 3 )

	##########################################################################################
	# EXTRACT THE ITERATION NUMBER
	iteration_number = -1
	m = re.search('iteration_(.+?)/', args.dict_file)
	if m:
		iteration_str = m.group(1)
		try:
			iteration_number = int(iteration_str)
		except:
			print("ERROR: The iteration does not have an integer value (" + iteration_str + ").\n")
			sys.exit(4)
	else:
		print("ERROR: An iteration number was not found in the dictionary-file's path (" + args.dict_file + ").\n")
		sys.exit(5)

	if iteration_number < 1: 
		print("ERROR: The iteration number found in the path is invalid (" + str(iteration_number) + ").\n")
		sys.exit(6)

	##########################################################################################
	# LOADS THE PREVIOUS DICTIONARY (IF EXISTS)
	dictionary = {}
	if iteration_number > 1:
		previous_dict_file = args.dict_file.replace( "iteration_" + str(iteration_number-1), "iteration_" + str(iteration_number) )
		verify_file( previous_dict_file, 'The previous dictionary file could not be read (' + previous_dict_file + ').', None, 7 )
		df_dict = pd.read_csv( previous_dict_file, sep='\t', names = ['word', 'count'], encoding='utf8', dtype = {'word':str, 'count':int} )
		df_dict = df_dict.fillna('')
		for index, row in df_dict.iterrows():
			dictionary[ row['word'] ] = int(row['count'])

	##########################################################################################
	# Read the values from the input file
	df = pd.read_csv( args.data_file, sep='\t', names = ['specimen', 'value'], encoding='utf8', dtype = {'specimen':str, 'value':str} )
	df = df.fillna('')
	
	##########################################################################################	
	# Augment or create a dictionary with the values
	pattern = re.compile('[\W_]+')	
	for index, row in df.iterrows():
		value = str(row['value'])
		# Eliminate special characters and 2 spaces
		value = pattern.sub(' ', value.lower())
		value = value.replace('  ', ' ').replace('  ', ' ')
		if value == '':
			continue
		# The value if added or the count incremented
		if value in dictionary.keys():
			dictionary[ value ] = dictionary[ value ] + 1
		else:
			dictionary[ value ] = 1

	##########################################################################################
	# Save the dictionary to disk
	dict_text = ""
	for key in dictionary.keys():
		dict_text += key + "\t" + str(dictionary[key]) + "\n"
	#
	with open(args.dict_file, "w+") as f:
		f.write( dict_text )
