#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Computes the per-specimen accumulated metric value in the different 
# 				tasks of the workflow.
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

from humain.utils import *


if __name__ == '__main__':
	""" Computes the per-specimen accumulated metric value in the different tasks of the workflow.
	"""
	parser = argparse.ArgumentParser("Computes the per-specimen accumulated metric value in the different tasks of the workflow.")
	parser.add_argument('-mf', '--mf', action="append", required=True, help="One or more metric files which values will be aggregated.")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="File with the summed per-specimen metric.")
	args = parser.parse_args()

	# Usage: 
	# python3 ./add.py -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/ocr_ds/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/reg_expr_ds/accepted/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/reg_expr_ds/rejected/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/crowd_event_date_ds/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/consensus_ds/accepted/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/consensus_ds/rejected/metrics/duration.csv -o ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/duration.csv

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	#### INPUTS
	# args.mf
	for pathfilename in args.mf:
		verify_file( pathfilename, 'The metric data file ' + pathfilename + ' was not found.', parser, 1 )

	# args.output_file
	verify_create_file( args.output_file, 'The output data file, for the metric values, could not be created.', parser, 2 )

	specimen_metric_dict = {}
	x = 1
	for pathfilename in args.mf:
		df_mf = pd.read_csv( pathfilename, header=None )
		df_mf = df_mf.fillna('')

		n = len(df_mf.columns)
		for index, row in df_mf.iterrows():
			# Compute the sum of the duration column(s)
			new_sum = 0.0
			i = 1 
			while i < n:
				if row[i]:
					new_sum += float( row[i] )
				i = i + 1

			# Add the (filename,value) to the dictionary or increment the total
			basename = row[0].split('.')[0]	
			if basename in specimen_metric_dict.keys():
				prev_sum = specimen_metric_dict[ basename ]
				specimen_metric_dict[ basename ] = prev_sum + new_sum
			else:
				specimen_metric_dict[ basename ] = new_sum

	output_file_text = ""
	for basename in specimen_metric_dict.keys():
		output_file_text += basename + "," + str(specimen_metric_dict[ basename ]) + "\n"
	
	with open( args.output_file, "w+" ) as f_o:
		f_o.write( output_file_text )
