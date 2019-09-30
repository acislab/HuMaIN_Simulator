#!/usr/bin/env python3

##########################################################################################
# Developers: 	Aditi Malladi and Icaro Alzuru 
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Simulates the consensus (majority voting) and Damerau-Levenshtein comparison
# 				made to find a final value from the crowdsourced data.
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
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
from humain.constants import *
from humain.utils import *


if __name__ == '__main__':
	""" Simulates the consensus (majority voting) and Damerau-Levenshtein comparison made to find a final value from the crowdsourced data.
	"""
	parser = argparse.ArgumentParser("Simulates the consensus (majority voting) and Damerau-Levenshtein comparison made to find a final value from the crowdsourced data.")
	parser.add_argument('-cr', '--crowd_file', action="store", required=True, help="Reference tsv file with the values transcribed by the volunteers.")
	parser.add_argument('-th', '--threshold', action="store", required=True, help="Threshold to decide the distance for acceptance or rejection.")
	parser.add_argument('-m', '--metric', action="append", required=True, help="One or more metrics that will be collected during the consensus execution.")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted and rejected transcriptions will be stored.")
	args = parser.parse_args()
	# Usage Example:
	# python3 consensus_recorded_by 
	# -cr /home/ialzuru/Fall2019/HuMaIN_Simulator/selfie/results/recorded_by_001/crowd_recorded_by/recorded_by.tsv
	# -th 0.8
	# -m duration
	# -metric_dir = datasets/aocr_mix100/consensus/directory_recorded_by.txt, output_dir = selfie/results/recorded_by_001/consensus_recorded_by

	python3 sn_consensus.py -c /home/ialzuru/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/crowd/terms/zooniverse/recorded_by.tsv -o /home/ialzuru/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/rb_consensus
	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
	#### INPUTS
	# args.crowd_file
	verify_file( args.crowd_file, 'The file with the referential crowdsourced values for Event Date (' + args.crowd_file + ') was not found: ', parser, 1 )
	# args.threshold
	threshold = 0.0
	try:
		threshold = float( args.threshold )
		if threshold < 0.0 or threshold > 1.0:
			print("\nERROR: The threshold value must be in the (0,1) range.\n")
			sys.exit( 2 )
	except ValueError:
		print("\nERROR: The threshold value must be in the (0,1) range.\n")
		sys.exit( 3 )

	# args.metric
	input_metrics_file = os.path.dirname(args.crowd_file) + "/metrics"
	if len(args.metric) > 0:
		# Metric directory
		verify_dir( input_metrics_file, 'The input metrics directory (' + input_metrics_file + ') was not found.', parser, 4 )
		# Metric files
		for m_name in args.metric:
			metric_file = input_metrics_file + "/" + m_name + ".csv"
			verify_file( metric_file, 'The metric file ' + metric_file + ' was not found in the metrics directory.', parser, 5 )
	
	#### OUTPUTS
	# args.output_dir
	verify_create_dir( args.output_dir, 'The output directory could not be created.', parser, 6 )
	# Output subdirectories for the accepted values and rejected specimens
	verify_create_dir( args.output_dir + "/accepted", 'The output directory for the accepted event date values could not be created.', parser, 7 )
	verify_create_dir( args.output_dir + "/rejected", 'The output directory for the rejected specimens could not be created.', parser, 8 )
	# Output files
	accepted_file = args.output_dir + "/accepted/accepted.tsv"
	rejected_file = args.output_dir + "/rejected/rejected.tsv"
	verify_create_file( accepted_file, 'The output file, for the extracted event dates, could not be created.', parser, 9 )
	verify_create_file( rejected_file, 'The output file of rejected specimens, could not be created.', parser, 10 )
	# Metric folders
	verify_create_dir( args.output_dir + "/accepted/metrics", 'The output metrics directory for the accepted event date values could not be created.', parser, 11 )
	verify_create_dir( args.output_dir + "/rejected/metrics", 'The output metrics directory for the rejected specimens could not be created.', parser, 12 )

	################################################################################################################################
	# LOAD IN A DATAFRAME THE CROWDSOURCED VALUES AND THE CORRESPONDENT SPECIMEN'S FILE
	df_crowd = pd.read_csv( args.crowd_file, sep='\t', names=['filename', 'value1', 'value2'] )
	df_crowd = df_crowd.fillna('')

	################################################################################################################################
	# LOAD IN A DICTIONARY THE FILENAMES AND THE CALC DISTANCE AND ADD TO ACCEPTED OR REJECTED
	
	# CREATE THE ACCEPTED AND REJECTED FILES
	accepted_text = ""
	rejected_text = ""
	filename_list = []
	accepted_dict = {}

	for index, row in df_crowd.iterrows():
		filename_list.append( row['filename'] )
		s = 1.0 - normalized_damerau_levenshtein_distance(row['value1'], row['value2'])
		if s >= float(args.threshold):
			accepted_text += row['filename'] + "\t" + row['value1']+ "\n"
			accepted_dict[row['filename']] = row['value1']
		else:
			rejected_text += row['filename'] + "\t" + row['value1'] + "\t" + row['value2'] + "\n"

	with open( accepted_file, "w+") as f_a:
		f_a.write( accepted_text )

	with open( rejected_file, "w+") as f_r:
		f_r.write( rejected_text )

	
	################################################################################################################################
	# CREATE THE METRIC FILES
		
	# For each metric, divide the values in Accepted and Rejected
	for m_name in args.metric:
		# Loads the metric values in a dataframe
		metric_file = input_metrics_file + "/" + m_name + ".csv"
		df_metric = pd.read_csv( metric_file, names=['filename', 'value'] )
		accepted_txt = ""
		rejected_txt = ""
		# Divide the metric value in Accepted and Rejected
		for index, row in df_metric.iterrows():
			if row['filename'] in filename_list:
				if row['filename'] in accepted_dict.keys():
					accepted_txt += row['filename'] + "," + str(row['value']) + "\n"
				else:
					rejected_txt += row['filename'] + "," + str(row['value']) + "\n"

		# Create and fill the Accepted metric file
		new_metric_filename = args.output_dir + "/accepted/metrics/" + m_name + ".csv"
		with open(new_metric_filename, "w+") as f_m:
			f_m.write( accepted_txt )
		# Create and fill the Rejected metric file
		new_metric_filename = args.output_dir + "/rejected/metrics/" + m_name + ".csv"
		with open(new_metric_filename, "w+") as f_m:
			f_m.write( rejected_txt )

	sys.exit(0)