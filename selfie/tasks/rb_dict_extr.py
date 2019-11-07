#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Extraction of the term, via brute-force, using a dictionary. Every file is 
# 				scanned and every dictionary entry searched in its content.
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

import os, sys, argparse, re, codecs, time
import pandas as pd

from humain.constants import *
from humain.utils import *

##############################################################################################################################################################
if __name__ == '__main__':
	""" Extraction of the Recorded-by term using a dictionary. """
	# Read arguments
	parser = argparse.ArgumentParser("Extraction of the term via brute-force, using a dictionary.")
	parser.add_argument('-i','--input_dir',action="store", required=True, help="Directory with the text files to be scanned.")
	parser.add_argument('-d','--dict_file',action="store", required=True, help="Dictionary file.")
	parser.add_argument('-t','--threshold',action="store", required=False, type=int, default=1, help="Minimum count registered in the dictionary for an entry to be accepted.")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted values and rejected specimens will be saved")
	args = parser.parse_args()
	
	# Usage example:
	# python3 ~/Summer2019/HuMaIN/rb_dict_extr.py -i ~/Fall2019/HuMaIN_Simulator/selfie/results/recorded_by/ocr -d ~/Fall2019/HuMaIN_Simulator/selfie/results/recorded_by/rb_create_dict/dictionary.tsv -o ~/Fall2019/HuMaIN_Simulator/selfie/results/recorded_by/rb_dict_extr
	
	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
	#### INPUTS
	# args.input_dir
	verify_dir( args.input_dir, 'The directory of the text files (' + args.input_dir + ') was not found: ', parser, 1 )	
	# args.dict_file
	verify_file( args.dict_file, 'The dictionary file (' + args.dict_file + ') was not found: ', parser, 2 )	
	# args.threshold
	threshold = 1
	try:
		threshold = int(args.threshold)
		if (threshold < 0):
			raise ValueError('Invalid threshold value.')
	except:
		print('Error: The threshold specified value is invalid.\n')
		parser.print_help()
		sys.exit(3)

	#### OUTPUTS
	# Output directory: args.output_dir
	verify_create_dir( args.output_dir, 'The output directory could not be created.', parser, 4 )
	# Output subdirectories for the accepted values and rejected specimens
	verify_create_dir( args.output_dir + "/accepted", 'The output directory for the accepted values could not be created.', parser, 5 )
	verify_create_dir( args.output_dir + "/rejected", 'The output directory for the specimens of unknown term value could not be created.', parser, 6 )
	# Output files
	output_accepted_file = args.output_dir + "/accepted/accepted.tsv"
	output_rejected_file = args.output_dir + "/rejected/rejected.txt"
	verify_create_file( output_accepted_file, 'The output file, for the extracted values, could not be created.', parser, 7 )
	verify_create_file( output_rejected_file, 'The output file of rejected specimens, could not be created.', parser, 8 )
	# Metric folders
	verify_create_dir( args.output_dir + "/accepted/metrics", 'The output metrics directory for the accepted values could not be created.', parser, 9 )
	verify_create_dir( args.output_dir + "/rejected/metrics", 'The output metrics directory for the rejected specimens could not be created.', parser, 10 )
			
	##########################################################################################		
	# Load the dictionary
	df_dict = pd.read_csv( args.dict_file, sep='\t', names = ['entry', 'count'] )
	df_dict.fillna('', inplace= True)
	dict_entries = []
	for index, row in df_dict.iterrows():
		if (int(row['count']) >= threshold):
			dict_entries.append( row['entry'] )

	################################################################################################################################
	# Read the specimens files that will be processed
	filenames = os.listdir( args.input_dir )
	filename_list = list(f for f in filenames if f.endswith('.txt'))

	text_accept = ""
	text_reject = ""
	text_duration_accept = ""
	text_duration_reject = ""
	
	for src_file in filename_list:
		start_time = time.time()

		# Read the content of the text file, coverting to unicode
		f = codecs.open(args.input_dir + "/" + src_file, encoding='utf-8', mode='r')
		data = f.read().replace('\n', ' ').replace('  ', ' ').lower()
		f.close()

		# Eliminate special characters
		pattern = re.compile('[\W_]+')
		data_lower = pattern.sub(' ', data)

		found = False
		value = ""
		for entry in dict_entries:
			if entry in data_lower:
				text_accept += src_file + "\t" + entry + "\n"
				text_duration_accept += src_file + ',' + str(time.time() - start_time) + '\n'
				found = True
				break

		if not found:
			text_reject += src_file + '\n'
			text_duration_reject += src_file + ',' + str(time.time() - start_time) + '\n'
	
	# Write the accepted value to the output file
	with open( output_accepted_file, "w+" ) as f_a:
		f_a.write( text_accept )	

	# Write the duration of the accepted values
	with open( args.output_dir + "/accepted/metrics/duration.csv", "w+" ) as f_ad:
		f_ad.write( text_duration_accept )

	# Write the rejected specimens to the output file
	with open( output_rejected_file, "w+" ) as f_r:
		f_r.write( text_reject )	

	# Write the duration of the rejected specimens
	with open( args.output_dir + "/rejected/metrics/duration.csv", "w+" ) as f_rd:
		f_rd.write( text_duration_reject )				
