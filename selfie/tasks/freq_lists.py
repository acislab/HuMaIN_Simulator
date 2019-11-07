#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Accepts or rejects the values extracted by the NER process based on the 
# 				local (per-biocollection) and global (iDigBio) frequency lists of the term
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

import os, sys, argparse, re, codecs, time, csv
import pandas as pd

from humain.constants import *
from humain.utils import *

##############################################################################################################################################################
if __name__ == '__main__':
	""" Accepts or rejects the values extracted by the NER process based on the local (per-biocollection) and global (iDigBio) frequency lists of the term. """
	# Read arguments
	parser = argparse.ArgumentParser("Accepts or rejects the values extracted by the NER process based on the local (per-biocollection) and global (iDigBio) frequency lists of the term.")
	parser.add_argument('-if','--input_file', action="store", required=True, help="File with the candidate values.")
	parser.add_argument('-ld','--local_dict_file', action="store", required=True, help="File with the dictionary or frequency list of values for the term, in the biocollection.")
	parser.add_argument('-gd','--global_dict_file', action="store", required=True, help="Frequency list of values for the term in the iDigBio repository.")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted values and rejected specimens will be saved")
	args = parser.parse_args()
	
	# Usage example:
	# python3 ~/Fall2019/HuMaIN_Simulator/selfie/tasks/freq_lists.py -if ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/ner/ner.tsv 
	# 			-ld ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/learning/dictionary.tsv -gd ~/Fall2019/HuMaIN_Simulator/datasets/idigbio/freq_table/recordedBy.tsv
	# 			-o ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/freq_lists
	
	# python3 ~/Fall2019/HuMaIN_Simulator/selfie/tasks/freq_lists.py -if ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/ner/ner.tsv -ld ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/learning/dictionary.tsv -gd ~/Fall2019/HuMaIN_Simulator/datasets/idigbio/freq_table/recordedBy.tsv -o ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/freq_lists

	###############################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
	#### INPUTS
	# args.input_file
	verify_file( args.input_file, 'The file with the candidate values (' + args.input_file + ') was not found: ', parser, 1 )	
	# args.local_dict_file
	verify_file( args.local_dict_file, 'The local dictionary file (' + args.local_dict_file + ') was not found: ', parser, 2 )	
	# args.global_dict_file
	verify_file( args.global_dict_file, 'The global dictionary file (' + args.global_dict_file + ') was not found: ', parser, 3 )

	#### OUTPUTS
	# Output directory: args.output_dir
	verify_create_dir( args.output_dir, 'The output directory could not be created.', parser, 4 )
	# Output subdirectories for the accepted values and rejected specimens
	verify_create_dir( args.output_dir + "/accepted", 'The output directory for the accepted values could not be created (' + args.output_dir + "/accepted" + ').', parser, 5 )
	verify_create_dir( args.output_dir + "/rejected", 'The output directory for the specimens of unknown term value could not be created.', parser, 6 )
	# Output files
	output_accepted_file = args.output_dir + "/accepted/accepted.tsv"
	output_rejected_file = args.output_dir + "/rejected/rejected.txt"
	verify_create_file( output_accepted_file, 'The output file, for the extracted values, could not be created.', parser, 7 )
	verify_create_file( output_rejected_file, 'The output file of rejected specimens, could not be created.', parser, 8 )
	# # Metric folders
	# verify_create_dir( args.output_dir + "/accepted/metrics", 'The output metrics directory for the accepted values could not be created.', parser, 9 )
	# verify_create_dir( args.output_dir + "/rejected/metrics", 'The output metrics directory for the rejected specimens could not be created.', parser, 10 )

	##########################################################################################		
	# Load the local dictionary
	df_dict_local = pd.read_csv( args.local_dict_file, sep='\t', names = ['entry', 'count'] )
	df_dict_local.fillna('', inplace= True)
	dict_local = {}
	for index, row in df_dict_local.iterrows():
		dict_local[ row['entry'] ] = int(row['count'])

	##########################################################################################		
	# Load the global dictionary
	df_dict_global = pd.read_csv( args.global_dict_file, sep='\t', names = ['entry', 'count'] )
	df_dict_global.fillna('', inplace= True)
	dict_global = {}
	for index, row in df_dict_global.iterrows():
		dict_global[ row['entry'] ] = int(row['count'])

	##########################################################################################		
	# Load the file with the candidate values
	df_cand = pd.read_csv( args.input_file, sep='\t', names = ['filename', 'value'], engine='python', encoding='utf8', error_bad_lines=False, quoting=csv.QUOTE_NONE, dtype = {'filename':str, 'value':str} )
	df_cand.fillna('', inplace= True)
	# Group by filename
	df_grp_cand = df_cand.groupby('filename')
	# Process each group, searching for "valid" values
	accepted_text = ""
	rejected_text = ""
	for filename, grp_cand in df_grp_cand:
		found = False
		accepted_list = []
		accepted_list_lower = []
		for index, row in grp_cand.iterrows():
			value = re.sub(r'[^\w\s]', ' ', row['value'].lower(), re.UNICODE).replace('  ', ' ').replace('  ', ' ')
			value = value.strip()
			
			if ( (value in dict_local.keys()) or ((value in dict_global.keys()) and dict_global[ value ] > 10) ) and (not value in accepted_list_lower):
				accepted_list.append( row['value'] )
				accepted_list_lower.append( value )
				found = True

		if found:
			accepted_text += filename + "\t" + ", ".join(accepted_list) + "\n"
		else:
			rejected_text += filename + "\n"

	# 	if not found:
	# 		text_reject += src_file + '\n'
	# 		text_duration_reject += src_file + ',' + str(time.time() - start_time) + '\n'
	
	# Write the accepted value to the output file
	with open( output_accepted_file, "w+" ) as f_a:
		f_a.write( accepted_text )	

	# # Write the duration of the accepted values
	# with open( args.output_dir + "/accepted/metrics/duration.csv", "w+" ) as f_ad:
	# 	f_ad.write( text_duration_accept )

	# Write the rejected specimens to the output file
	with open( output_rejected_file, "w+" ) as f_r:
		f_r.write( rejected_text )	

	# # Write the duration of the rejected specimens
	# with open( args.output_dir + "/rejected/metrics/duration.csv", "w+" ) as f_rd:
	# 	f_rd.write( text_duration_reject )				
