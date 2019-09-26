#!/usr/bin/env python3
import os, sys, argparse
import pandas as pd

from humain.utils import *


if __name__ == '__main__':
	""" Compute the per-specimen total execution time 
	"""
	parser = argparse.ArgumentParser("Compute the per-specimen total execution time.")
	parser.add_argument('-mf', '--mf', action="append", required=True, help="One or more metric file which values will be aggregated.")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="File with the summed per-specimen duration.")
	args = parser.parse_args()

	# Usage: 
	# python3 ./duration_event_date.py -mf ~/Desktop/HuMaIN_Simulator/humain/selfie/results/recorded_by_001/crowd_recorded_by/metrics/duration.csv -o ~/Desktop/HuMaIN_Simulator/humain/selfie/results/recorded_by_001/duration.csv

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	#### INPUTS
	# args.mf
	for pathfilename in args.mf:
		verify_file( pathfilename, 'The metric data file ' + pathfilename + ' was not found.', parser, 1 )

	# args.output_file
	verify_create_file( args.output_file, 'The output data file, for the metric values, could not be created.', parser, 2 )

	specimen_duration_dict = {}
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

			# Add the (filename,value) to the dictionary or increment the duration
			basename = row[0].split('.')[0]	
			if basename in specimen_duration_dict.keys():
				prev_sum = specimen_duration_dict[ basename ]
				specimen_duration_dict[ basename ] = prev_sum + new_sum
			else:
				specimen_duration_dict[ basename ] = new_sum

	duration_text = ""
	for basename in specimen_duration_dict.keys():
		duration_text += basename + "," + str(specimen_duration_dict[ basename ]) + "\n"
	
	with open( args.output_file, "w+" ) as f_o:
		f_o.write( duration_text )
