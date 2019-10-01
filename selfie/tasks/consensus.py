#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Simulates the execution of the consensus algorithm to determine the final 
# 				value among the crowdsourced values for each image.
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
	""" Simulates the execution of the consensus algorithm to determine the final value among the crowdsourced values for each image.
	"""
	parser = argparse.ArgumentParser("Simulates the execution of the consensus algorithm to determine the final value among the crowdsourced values for each image.")
	parser.add_argument('-cr', '--crowd_file', action="store", required=True, help="Reference tsv file with the values transcribed by the volunteers.")
	parser.add_argument('-co', '--consensus_dir', action="store", required=True, help="Directory where the accepted (consensus reached) and rejected specimens (unknown) are saved.")
	parser.add_argument('-m', '--metric', action="append", required=True, help="One or more metrics that will be collected during the consensus execution.")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted and rejected transcriptions will be stored.")
	args = parser.parse_args()

	# Usage:
	# python3 ./sn_consensus.py 
	# -cr /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_crowd/sn_crowd.tsv 
	# -co /home/ialzuru/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_consensus 
	# -m duration -o /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_consensus
	# python3 ./sn_consensus.py -cr /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_crowd/sn_crowd.tsv -co /home/ialzuru/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_consensus -m duration -o /home/ialzuru/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_consensus
	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
	#### INPUTS
	# args.crowd_file
	verify_file( args.crowd_file, 'The file with the crowdsourced values (' + args.crowd_file + ') was not found: ', parser, 1 )

	# args.consensus_dir
	verify_dir( args.consensus_dir, 'The directory with the accepted and rejected values (' + args.consensus_dir + ') was not found: ', parser, 3 )
	cons_accepted_dir = args.consensus_dir + "/accepted"
	cons_rejected_dir = args.consensus_dir + "/rejected"
	# Input subdirectories for the accepted values and the rejected specimens
	verify_dir( cons_accepted_dir, 'The directory of the accepted values was not found (' + cons_accepted_dir + ').', parser, 4 )
	verify_dir( cons_rejected_dir, 'The directory of the rejected specimens was not found (' + cons_rejected_dir + ').', parser, 5 )
	cons_accepted_file = cons_accepted_dir + "/accepted.tsv"
	cons_rejected_file = cons_rejected_dir + "/rejected.txt"
	verify_file( cons_accepted_file, 'The file of accepted values ' + cons_accepted_file + ' was not found.', parser, 6 )
	verify_file( cons_rejected_file, 'The file of rejected specimens ' + cons_rejected_file + ' was not found.', parser, 7 )
	# args.metric
	metrics_dir_accepted = cons_accepted_dir + "/metrics"
	metrics_dir_rejected = cons_rejected_dir + "/metrics"
	if len(args.metric) > 0:
		# Metric directory
		verify_dir( metrics_dir_accepted, 'The metrics directory of the accepted values was not found.', parser, 8 )
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
	verify_create_dir( args.output_dir + "/accepted", 'The output directory for the accepted values could not be created.', parser, 13 )
	verify_create_dir( args.output_dir + "/rejected", 'The output directory for the specimens with rejected specimens could not be created.', parser, 14 )
	# Output files
	output_accepted_file = args.output_dir + "/accepted/accepted.tsv"
	output_rejected_file = args.output_dir + "/rejected/rejected.txt"
	verify_create_file( output_accepted_file, 'The output file, for the extracted values, could not be created.', parser, 15 )
	verify_create_file( output_rejected_file, 'The output file of rejected specimens, could not be created.', parser, 16 )
	# Metric folders
	verify_create_dir( args.output_dir + "/accepted/metrics", 'The output metrics directory for the accepted values could not be created.', parser, 17 )
	verify_create_dir( args.output_dir + "/rejected/metrics", 'The output metrics directory for the rejected specimens could not be created.', parser, 18 )

	################################################################################################################################
	# Read the specimens files rejected during the suffix extraction task
	df_s = pd.read_csv( args.crowd_file, sep='\t', names=['filename','value1','value2','value3'] )
	df_s = df_s.fillna('')

	df_files = df_s['filename']

	################################################################################################################################
	# Load the values extracted through consensus
	df_a = pd.read_csv( cons_accepted_file, sep='\t', names=['filename', 'final_value'] )
	df_a = df_a.fillna('')

	df_accepted = pd.merge(df_files, df_a, on='filename')
	df_accepted.to_csv(output_accepted_file, sep='\t', index=False, header=False)
	################################################################################################################################
	# Load the specimens (filenames) for which no value could be extracted using consensus
	df_r = pd.read_csv( cons_rejected_file, sep='\t', names=['filename'] )
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

	sys.exit(0)
