#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Simulation of the extraction of scientific names by using a dictionary to 
# 				scan the words of the text files.
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

import argparse
import pandas as pd

from humain.constants import *
from humain.utils import *

if __name__ == '__main__':
	""" Simulation of the extraction of scientific names by using a dictionary to scan the words of the text files.
	"""
	parser = argparse.ArgumentParser("Simulation of the extraction of scientific names by using a dictionary to scan the words of the text files.")
	parser.add_argument('-s', '--rej_suf_file', action="store", required=True, help="txt file with rejected specimens from the Extraction by Suffixes task.")
	parser.add_argument('-n', '--rej_nor_file', action="store", required=True, help="txt file with rejected specimens from the Dictionary Normalization task.")
	parser.add_argument('-d', '--dict_extr_dir', action="store", required=True, help="Directory with the result of the extraction of scientific names by using a dictionary.")
	parser.add_argument('-m', '--metric', action="append", required=False, help="One or more metrics that will be collected when verifying the scientific name.")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted and rejected extractions will be stored.")
	args = parser.parse_args()	
	# Usage example: python3 sn_dict_extr.py -s /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_suffix_ds/rejected/rejected.tsv 
	# 	-n /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_norm_dict/rejected/rejected.tsv
	# 	-d /home/ialzuru/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_dict_extr/ocropus 
	# 	-m duration -o /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_dict_extr
	# python3 sn_dict_extr.py -s /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_suffix_ds/rejected/rejected.tsv -n /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_norm_dict/rejected/rejected.tsv -d /home/ialzuru/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_dict_extr/ocropus -m duration -o /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_dict_extr
	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
	#### INPUTS
	# args.rej_suf_file and args.rej_nor_file (Rejected specimens)
	verify_file( args.rej_suf_file, 'The file with the rejected specimens from the suffix extraction task (' + args.rej_suf_file + ') was not found: ', parser, 1 )
	verify_file( args.rej_nor_file, 'The file with the rejected specimens from the normalization task (' + args.rej_nor_file + ') was not found: ', parser, 2 )

	# args.dict_extr_dir
	verify_dir( args.dict_extr_dir, 'The directory with the accepted and rejected values (' + args.dict_extr_dir + ') was not found: ', parser, 3 )
	dict_accepted_dir = args.dict_extr_dir + "/accepted"
	dict_rejected_dir = args.dict_extr_dir + "/rejected"
	# Input subdirectories for the accepted scientific name values and the rejected specimens
	verify_dir( dict_accepted_dir, 'The directory of the accepted scientific names was not found (' + dict_accepted_dir + ').', parser, 4 )
	verify_dir( dict_rejected_dir, 'The directory of the rejected specimens was not found (' + dict_rejected_dir + ').', parser, 5 )
	dict_accepted_file = dict_accepted_dir + "/accepted.tsv"
	dict_rejected_file = dict_rejected_dir + "/rejected.txt"
	verify_file( dict_accepted_file, 'The file of accepted scientific names ' + dict_accepted_file + ' was not found.', parser, 6 )
	verify_file( dict_rejected_file, 'The file of rejected specimens ' + dict_rejected_file + ' was not found.', parser, 7 )
	# args.metric
	metrics_dir_accepted = dict_accepted_dir + "/metrics"
	metrics_dir_rejected = dict_rejected_dir + "/metrics"
	if len(args.metric) > 0:
		# Metric directory
		verify_dir( metrics_dir_accepted, 'The metrics directory of the accepted scientific names was not found.', parser, 8 )
		verify_dir( metrics_dir_rejected, 'The metrics directory of the rejected specimens was not found.', parser, 9 )
		# Metric files
		for m_name in args.metric:
			metric_file_accepted = metrics_dir_accepted + "/" + m_name + ".csv"
			metric_file_rejected = metrics_dir_rejected + "/" + m_name + ".csv"
			verify_file( metric_file_accepted, 'The metric file ' + metric_file_accepted + ' was not found in the accepted metrics directory.', parser, 10 )
			verify_file( metric_file_rejected, 'The metric file ' + metric_file_rejected + ' was not found in the rejected metrics directory.', parser, 11 )

	#### OUTPUTS
	# Output directory: args.output_dir
	verify_create_dir( args.output_dir, 'The output directory could not be created.', parser, 12 )
	# Output subdirectories for the accepted values and rejected specimens
	verify_create_dir( args.output_dir + "/accepted", 'The output directory for the accepted scientifics could not be created.', parser, 13 )
	verify_create_dir( args.output_dir + "/rejected", 'The output directory for the specimens with rejected scientific name candidate could not be created.', parser, 14 )
	# Output files
	output_accepted_file = args.output_dir + "/accepted/accepted.tsv"
	output_rejected_file = args.output_dir + "/rejected/rejected.txt"
	verify_create_file( output_accepted_file, 'The output file, for the extracted scientific names, could not be created.', parser, 15 )
	verify_create_file( output_rejected_file, 'The output file of rejected specimens, could not be created.', parser, 16 )
	# Metric folders
	verify_create_dir( args.output_dir + "/accepted/metrics", 'The output metrics directory for the accepted scientific name values could not be created.', parser, 17 )
	verify_create_dir( args.output_dir + "/rejected/metrics", 'The output metrics directory for the rejected specimens could not be created.', parser, 18 )

	################################################################################################################################
	# Read the specimens files rejected during the suffix extraction task
	df_s = pd.read_csv( args.rej_suf_file, sep='\t', names=['filename'] )
	df_s = df_s.fillna('')

	# Read the specimens files rejected during the normalization task
	df_n = pd.read_csv( args.rej_nor_file, sep='\t', names=['filename'] )
	df_n = df_n.fillna('')

	df_files = pd.concat([df_s, df_n])

	################################################################################################################################
	# Load the scientific name extracted using the dictionary extraction task
	df_a = pd.read_csv( dict_accepted_file, sep='\t', names=['filename', 'candidate', 'dict_entry'] )
	df_a = df_a.fillna('')

	df_accepted = pd.merge(df_files, df_a, on='filename')[['filename','dict_entry']]
	df_accepted.to_csv(output_accepted_file, sep='\t', index=False, header=False)
	################################################################################################################################
	# Load the specimens (filenames) for which no scientific name could be extracted using the dictionary extraction task
	df_r = pd.read_csv( dict_rejected_file, sep='\t', names=['filename'] )
	df_r = df_r.fillna('')

	df_rejected = pd.merge(df_files, df_r, on='filename')
	df_rejected.to_csv(output_rejected_file, sep='\t', index=False, header=False)
	################################################################################################################################

	################################################################################################################################
	# Metrics Processing
	for m_name in args.metric:
		# Input metric files
		input_metric_file_accepted = metrics_dir_accepted + "/" + m_name + ".csv"
		input_metric_file_rejected = metrics_dir_rejected + "/" + m_name + ".csv"
		# Output metric files
		output_metric_file_accepted = args.output_dir + "/accepted/metrics/" + m_name + ".csv"
		output_metric_file_rejected = args.output_dir + "/rejected/metrics/" + m_name + ".csv"

		# Accepted metric file
		df_am = pd.read_csv( input_metric_file_accepted, sep=',', names=['filename', 'value'] )
		df_accepted_m = pd.merge(df_files, df_am, on='filename')
		df_accepted_m.to_csv(output_metric_file_accepted, sep=',', index=False, header=False)
		# Rejected metric file
		df_rm = pd.read_csv( input_metric_file_rejected, sep=',', names=['filename', 'value'] )
		df_rejected_m = pd.merge(df_files, df_rm, on='filename')
		df_rejected_m.to_csv(output_metric_file_rejected, sep=',', index=False, header=False)
