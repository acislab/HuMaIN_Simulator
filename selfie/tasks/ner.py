#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Namend Entity Recognition: Scans every sentence looking up for the term 
# 				under study.
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

import os, sys, argparse, re, time, spacy
import pandas as pd

from humain.constants import *
from humain.utils import *

valid_terms = ["COUNTY", "EVENTDATE", "HABITAT", "RECORDEDBY", "SCIENTIFICNAME", "STATEPROVINCE"]

##############################################################################################################################################################
if __name__ == '__main__':
	""" NER: Scans every sentence looking up for the term under study. """
	# Read arguments
	parser = argparse.ArgumentParser("NER: Scans every sentence looking up for the term under study.")
	parser.add_argument('-if','--input_file',action="store", required=True, help="File with the list of (specimen) text files to process using the NER model.")
	parser.add_argument('-dd','--data_dir',action="store", required=True, help="Directory with the OCR-ed text files of the images in Spacy format.")
	parser.add_argument('-md','--model_dir',action="store", required=True, help="Directory with the text files in Spacy format.")
	parser.add_argument('-t','--term',action="store", required=True, help="Darwin Core Term to search using the trained model.")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="TSV file with the extracted term's value for each file (specimen).")
	args = parser.parse_args()
	
	# Usage example:
	# python3 ~/Fall2019/HuMaIN_Simulator/selfie/tasks/ner.py -if ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/remaining_specimens.txt -dd ~/Fall2019/HuMaIN_Simulator/datasets/wedigbio/trn_data_spacy_format/wdb_comfort -md ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/learning/model -t RECORDEDBY -o ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/ner/ner.tsv
	
	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
	#### INPUTS
	# args.input_file
	verify_file( args.input_file, 'The file with the list of files o process (' + args.input_file + ') was not found: ', parser, 1 )	
	# args.data_dir
	verify_dir( args.data_dir, 'The directory of the text files in Spacy format (' + args.data_dir + ') was not found: ', parser, 2 )	
	# args.model_dir
	verify_dir( args.model_dir, 'The dictionary of the Spacy Model (' + args.model_dir + ') was not found: ', parser, 3 )	
	# args.term
	term = args.term.upper()
	if not (term in valid_terms):
		print("\nERROR: The inserted term (" + args.term + ") is not valid.\n")
		parser.print_help()
		sys.exit( 4 )

	#### OUTPUTS
	# Output directory: args.output_file
	output_dir = os.path.dirname( args.output_file)
	print(output_dir)
	verify_create_dir( output_dir, 'The output directory, for the extracted values, could not be created.', parser, 5 )
	print(args.output_file)
	verify_create_file( args.output_file, 'The output file, for the extracted values, could not be created.', parser, 6 )
	# Rejected specimens
	verify_create_dir( output_dir + "/rejected", 'The output directory for the rejected specimens could not be created.', parser, 7 )
	rejected_filename = output_dir + "/rejected/rejected.txt"
	verify_create_file( rejected_filename, 'The output file for the rejected specimens could not be created.', parser, 8 )

	################################################################################################################################
	# LOAD THE MODEL
	################################################################################################################################
	print("Loading model from", args.model_dir)
	nlp = spacy.load( args.model_dir )
	if not nlp:
		print( "\nERROR: The model could not be loaded (" + args.model_dir + ").\n" )
		sys.exit( 9 )

	################################################################################################################################
	# PROCESS ALL THE FILES THAT ARE IN INPUT_FILE AND DATA_DIR
	################################################################################################################################
	# Filename in args.input_file
	df_remaining = pd.read_csv( args.input_file, names = ['filename'] )
	df_remaining.fillna('', inplace= True)
	remaining_set = set( df_remaining["filename"].tolist() )

	# All the data files available
	filenames = os.listdir( args.data_dir )
	filename_list = list(f for f in filenames if f.endswith('.txt'))

	# Intersection of both lists of files
	filename_list = list( set(filename_list) & remaining_set)

	text_to_save = ""
	text_rejected = ""
	for src_file in filename_list:
		# start_time = time.time()
		term_found = False

		with open( args.data_dir + "/" + src_file ) as f:
			lines = f.readlines()
		# Remove whitespace characters like `\n` at the end of each line
		lines = [x.strip() for x in lines] 
		#
		for line in lines:
			segmented_line = line.split('\t')
			sentence = segmented_line[0]

			# Read the terms extracted by the trained model in the same sentence
			candidate = {}
			doc = nlp( sentence )
			for ent in doc.ents:
				if ent.label_ == term:
					text_to_save += src_file + "\t" + ent.text + "\n"
					term_found = True

		if not term_found:
		 	text_rejected += src_file + "\n"
	
	################################################################################################################################
	# SAVE THE OUTPUT FILES
	################################################################################################################################
	# Write the candidate values to the output file
	with open( args.output_file, "w+" ) as f_a:
		f_a.write( text_to_save )
	with open( rejected_filename, "w+" ) as f_r:
		f_r.write( text_rejected )
	