#!/usr/bin/env python3
import os, sys, argparse
from humain.common.utils import *


if __name__ == '__main__':
	""" Compute the total per-specimen execution time 
	"""
	parser = argparse.ArgumentParser("Compute the total per-specimen execution time.")
	parser.add_argument('-mf', '--mf', action="append", required=True, help="One or more metric file which values will be aggregated.")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="File with the summed per-specimen duration.")
	args = parser.parse_args()

	# Usage: 
	# python3 ./duration_event_date.py -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/ocr_dataset/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/reg_expr_dataset/accepted/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/reg_expr_dataset/rejected/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/crowd_event_date_dataset/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/consensus_dataset/accepted/metrics/duration.csv -mf ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/consensus_dataset/rejected/metrics/duration.csv -o ~/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/duration.csv

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	#### INPUTS
	# args.mf
	for pathfilename in args.mf:
		verify_file( pathfilename, 'The metric data file ' + pathfilename + ' was not found.', parser, 1 )

	# args.output_file
	verify_create_file( args.output_file, 'The output data file, for the metric values, could not be created.', parser, 2 )

	
