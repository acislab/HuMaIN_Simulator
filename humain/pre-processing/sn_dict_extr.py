#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Extraction of the scientific name using a dictionary. Every file is 
# 				scanned and every pair of words compared to the dictionary entries.
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

import os, sys, re, codecs, time
import argparse, numpy
import pandas as pd

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

##############################################################################################################################################################
if __name__ == '__main__':
	""" Extraction of the scientific name using a dictionary. Every file is scanned and every pair of words compared to the dictionary entries. """
	# Read arguments
	parser = argparse.ArgumentParser("Extraction of the scientific name using a dictionary. Every file is scanned and every pair of words compared to the dictionary entries.")
	parser.add_argument('-i','--input_dir',action="store", required=True, help="Directory with the text files to e scanned.")
	parser.add_argument('-d','--dictionary',action="store", required=True, help="Dictionary file.")
	parser.add_argument('-t','--threshold',action="store", required=False, type=float, default=0.85, help="Minimum similarity for a word to be accepted when compared to dictionary words.")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted scientific names and rejected specimens will be saved")
	args = parser.parse_args()
	# Usage example:
	# python3 ~/Fall2019/HuMaIN/sn_dict_extr.py -i ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/ocr/ocropus -d ~/Fall2019/HuMaIN_Simulator/datasets/dictionary/d_all.txt -o ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_dict_extr/ocropus
	# python3 ~/Fall2019/HuMaIN/sn_dict_extr.py -i ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/ocr/gc-ocr -d ~/Fall2019/HuMaIN_Simulator/datasets/dictionary/d_all.txt -o ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_dict_extr/gc-ocr
	# python3 ~/Fall2019/HuMaIN/sn_dict_extr.py -i ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/ocr/tesseract -d ~/Fall2019/HuMaIN_Simulator/datasets/dictionary/d_all.txt -o ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_dict_extr/tesseract
	
	##########################################################################################
	# Arguments Validations
	if ( not os.path.isdir( args.input_dir ) ):
		print('Error: The directory of the text files was not found.\n')
		parser.print_help()
		sys.exit(1)
	
	if ( not os.path.isfile( args.dictionary ) ):
		print('Error: Dictionary file does not exist.\n')
		parser.print_help()
		sys.exit(2)

	threshold = 0.85
	try:
		threshold = float(args.threshold)
		if (threshold < 0.0) or (threshold > 1.0):
			raise ValueError('Invalid threshold value.')
	except:
		print('Error: The threshold specified value is invalid.\n')
		parser.print_help()
		sys.exit(3)

	# Verifiy creation of the output folder
	if not os.path.exists( args.output_dir ):
		try:
			os.makedirs( args.output_dir )  
		except:
			print('Error: The destination directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(4)	

	if not os.path.exists( args.output_dir + "/accepted" ):
		try:
			os.makedirs( args.output_dir + "/accepted" )  
		except:
			print('Error: The "accepted" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(5)	
	
	if not os.path.exists( args.output_dir + "/rejected" ):
		try:
			os.makedirs( args.output_dir + "/rejected" )  
		except:
			print('Error: The "rejected" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(6)	

	if not os.path.exists( args.output_dir + "/accepted/metrics" ):
		try:
			os.makedirs( args.output_dir + "/accepted/metrics" )  
		except:
			print('Error: The "accepted/metrics" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(7)	

	if not os.path.exists( args.output_dir + "/rejected/metrics" ):
		try:
			os.makedirs( args.output_dir + "/rejected/metrics" )  
		except:
			print('Error: The "rejected/metrics" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(8)

	# Verify the creation of the accepted and rejected files
	accepted_file = args.output_dir + "/accepted/accepted.tsv"
	try:
		f = open(accepted_file, "w+") 
		f.close() 
	except:
		print( "\nERROR: The accepted file could not be created.\n" )
		parser.print_help()
		sys.exit(9)

	rejected_file = args.output_dir + "/rejected/rejected.tsv"
	try:
		f = open(rejected_file, "w+") 
		f.close() 
	except:
		print( "\nERROR: The rejected_file file could not be created.\n" )
		parser.print_help()
		sys.exit(10)
		
	##########################################################################################		
	# Load the dictionary
	df_dict = pd.read_csv( args.dictionary, sep=',', names = ['first', 'second'] )
	df_dict.fillna('', inplace= True)

	##########################################################################################
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
		firstname = ''
		for secondname in data_lower.split():
			if ( (len(firstname)>4) and (len(secondname)>4) ): # two long words
			
				for idx, dict_entry in df_dict.iterrows():	
					sim1 = 1.0 - normalized_damerau_levenshtein_distance( firstname, dict_entry['first'] )
					if ( sim1 > threshold ):
						sim2 = 1.0 - normalized_damerau_levenshtein_distance( secondname, dict_entry['second'] )
						if ( sim2 > threshold ):
							text_accept += src_file + "\t" + firstname + " " + secondname + "\t" + dict_entry['first'] + " " + dict_entry['second'] + "\n"
							text_duration_accept += src_file + ',' + str(time.time() - start_time) + '\n'
							found = True
							break
			
			firstname = secondname
			if found:
				break
		
		if not found:
			text_reject += src_file + '\n'
			text_duration_reject += src_file + ',' + str(time.time() - start_time) + '\n'
	
	# Write the Scientific Name candidate to the output file
	with open( accepted_file, "w+" ) as f_a:
		f_a.write( text_accept )	

	# Write the duration of the accepted values
	with open( args.output_dir + "/accepted/metrics/duration.csv", "w+" ) as f_ad:
		f_ad.write( text_duration_accept )

	# Write the rejected specimens to the output file
	with open( rejected_file, "w+" ) as f_r:
		f_r.write( text_reject )	

	# Write the duration of the rejected specimens
	with open( args.output_dir + "/rejected/metrics/duration.csv", "w+" ) as f_rd:
		f_rd.write( text_duration_reject )				
