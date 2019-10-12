#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Simulated version of the Optical Character Recognition of a dataset.
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

import os, sys, re, time
import argparse, numpy
import pandas as pd

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

##############################################################################################################################################################
if __name__ == '__main__':
	""" MAIN """
	# Read arguments
	parser = argparse.ArgumentParser("Given the result of getBySuffix.py and a dictionary, search the candidates in the dictionary and returns their similarity")
	parser.add_argument('-i','--input',action="store", required=True, help="Text file to be scanned. Format: filename, scientific name")
	parser.add_argument('-d','--dictionary',action="store", required=True, help="Dictionary. ")
	parser.add_argument('-t','--threshold',action="store", required=False, type=float, default=0.8, help="Minimum similarity for a word to be accepted when compared to dictionary words.")
	parser.add_argument('-o','--output_dir',action="store", required=True, help="Directory where the accepted, rejected, and metric files will be saved. ")
	args = parser.parse_args()
	# Usage:
	# python3 sn_norm_dict.py -i ~/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_suffix/ocropus/accepted/accepted.tsv -d ~/Summer2019/HuMaIN_Simulator/datasets/dictionary/d_all.txt -o ~/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_norm_dict/ocropus
	# python3 sn_norm_dict.py -i ~/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_suffix/tesseract/accepted/accepted.tsv -d ~/Summer2019/HuMaIN_Simulator/datasets/dictionary/d_all.txt -o ~/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_norm_dict/tesseract
	# python3 sn_norm_dict.py -i ~/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_suffix/gc-ocr/accepted/accepted.tsv -d ~/Summer2019/HuMaIN_Simulator/datasets/dictionary/d_all.txt -o ~/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_norm_dict/gc-ocr
	##########################################################################################
	threshold = float(args.threshold)
	##########################################################################################
	# The existence of the source file is verified
	if ( not os.path.isfile( args.input ) ):
		print('Error: File does not exist.\n')
		parser.print_help()
		sys.exit(1)
	
	if ( not os.path.isfile( args.dictionary ) ):
		print('Error: Dictionary file does not exist.\n')
		parser.print_help()
		sys.exit(2)

	if not os.path.exists( args.output_dir ):
		try:
			os.makedirs( args.output_dir )  
		except:
			print('Error: The destination directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(3)	

	if not os.path.exists( args.output_dir + "/accepted" ):
		try:
			os.makedirs( args.output_dir + "/accepted" )  
		except:
			print('Error: The "accepted" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(4)	
	
	if not os.path.exists( args.output_dir + "/rejected" ):
		try:
			os.makedirs( args.output_dir + "/rejected" )  
		except:
			print('Error: The "rejected" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(5)	

	if not os.path.exists( args.output_dir + "/accepted/metrics" ):
		try:
			os.makedirs( args.output_dir + "/accepted/metrics" )  
		except:
			print('Error: The "accepted/metrics" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(6)	

	if not os.path.exists( args.output_dir + "/rejected/metrics" ):
		try:
			os.makedirs( args.output_dir + "/rejected/metrics" )  
		except:
			print('Error: The "rejected/metrics" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(7)	

	# Load the data 
	df_data = pd.read_csv( args.input, sep='\t', names = ['filename', 'sname'] )
	df_data.fillna('', inplace= True)
	# Load the dictionary
	df_dict = pd.read_csv( args.dictionary, sep=',', names = ['first', 'second'] )
	df_dict.fillna('', inplace= True)
	##########################################################################################
	# Search each word in the firstname column (using similarity)
	text_accept = ""
	text_reject = ""
	text_duration_accept = ""
	text_duration_reject = ""
	for index, candidate in df_data.iterrows():
		start_time = time.time()
		firstname = ''
		secondname = ''

		p = candidate['sname'].partition(' ')
		n = 0
		if ( len(p) > 0 ):
			firstname =  p[0]
			if ( len(p) > 2 ):
				secondname = p[2]
				n = 2

		if n == 2:
			found = False
			for idx, entrada in df_dict.iterrows():
				sim1 = 1.0 - normalized_damerau_levenshtein_distance( firstname, entrada['first'] )
				if ( sim1 > threshold ):
					sim2 = 0.0
					if (secondname=='' and entrada['second'] == ''):
						sim2 = 1.0
					elif (secondname=='' and entrada['second'] != '') or (secondname!='' and entrada['second'] == ''):
						sim2 = 0.0
					else:
						sim2 = 1.0 - normalized_damerau_levenshtein_distance( secondname, entrada['second'] )

					if ( sim2 > threshold ):
						if entrada['second'] == '':
							text_accept += candidate['filename'] + "\t" + firstname + "\t" + entrada['first'] + "\n"
						else:
							text_accept += candidate['filename'] + "\t" + firstname + " " + secondname + "\t" + entrada['first'] + " " + entrada['second'] + "\n"
						text_duration_accept += candidate['filename'] + "," + str(time.time() - start_time) + "\n"
						found = True
						break
			if not found:
				text_reject += candidate['filename'] + "\n"
				text_duration_reject += candidate['filename'] + "," + str(time.time() - start_time) + "\n"
		else:
			text_reject += candidate['filename'] + "\n"
			text_duration_reject += candidate['filename'] + "," + str(time.time() - start_time) + "\n"

	with open(args.output_dir + "/accepted/accepted.tsv", "w+") as f_a:
		f_a.write( text_accept )
	with open(args.output_dir + "/accepted/metrics/duration.csv", "w+") as f_d_a:
		f_d_a.write( text_duration_accept )
	with open(args.output_dir + "/rejected/rejected.tsv", "w+") as f_r:
		f_r.write( text_reject )
	with open(args.output_dir + "/rejected/metrics/duration.csv", "w+") as f_d_r:
		f_d_r.write( text_duration_reject )		
