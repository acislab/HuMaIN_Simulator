#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Simulated version of the extraction of Scientific Name candidates by suffixes.
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

import argparse, shutil
import pandas as pd
from shutil import copyfile

from humain.constants import *
from humain.utils import *

if __name__ == '__main__':
	""" Simulated version of the extraction of Scientific Name candidates by suffixes
	"""
	parser = argparse.ArgumentParser("Simulated version of the extraction of Scientific Name candidates by suffixes.")
	parser.add_argument('-d', '--fulltext_dir', action="store", required=True, help="Directory with the fulltext transcription files of the images.")
	parser.add_argument('-s', '--suffix_dir', action="store", required=True, help="File with the Scientific Name candidates extracted using suffixes algorithm.")	
	parser.add_argument('-m', '--metric', action="append", required=False, help="One or more metrics that will be collected when running the regular expression extraction.")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted and rejected extractions will be stored.")
	args = parser.parse_args()

	# Usage example: 
	# python3 sn_suffix_ds.py -d ~/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/ocr_ds -s ~/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_suffix/ocropus -m duration -o ~/Summer2019/HuMaIN_Simulator/selfie/results/scientific_name/sn_suffix_ds
	
	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	#### INPUTS
	# args.fulltext_dir
	verify_dir( args.fulltext_dir, 'The fulltext transcription directory (' + args.fulltext_dir + ') was not found: ', parser, 1 )

	# args.suffix_dir
	verify_dir( args.suffix_dir, 'The directory with the accepted and rejected values (' + args.suffix_dir + ') was not found: ', parser, 2 )
	suff_accepted_dir = args.suffix_dir + "/accepted"
	suff_rejected_dir = args.suffix_dir + "/rejected"
	# Input subdirectories for the accepted scientific name values and the rejected specimens
	verify_dir( suff_accepted_dir, 'The directory of the accepted scientific names was not found (' + suff_accepted_dir + ').', parser, 3 )
	verify_dir( suff_rejected_dir, 'The directory of the rejected scientific names was not found (' + suff_rejected_dir + ').', parser, 4 )
	suff_accepted_file = suff_accepted_dir + "/accepted.tsv"
	suff_rejected_file = suff_rejected_dir + "/rejected.txt"
	verify_file( suff_accepted_file, 'The file of accepted scientific names ' + suff_accepted_file + ' was not found.', parser, 5 )
	verify_file( suff_rejected_file, 'The file of rejected specimens ' + suff_rejected_file + ' was not found.', parser, 6 )
	
	# args.metric
	metrics_dir_accepted = suff_accepted_dir + "/metrics"
	metrics_dir_rejected = suff_rejected_dir + "/metrics"
	if len(args.metric) > 0:
		# Metric directory
		verify_dir( metrics_dir_accepted, 'The metrics directory of the accepted scientific names was not found.', parser, 7 )
		verify_dir( metrics_dir_rejected, 'The metrics directory of the rejected specimens was not found.', parser, 8 )
		# Metric files
		for m_name in args.metric:
			metric_file_accepted = metrics_dir_accepted + "/" + m_name + ".csv"
			metric_file_rejected = metrics_dir_rejected + "/" + m_name + ".csv"
			verify_file( metric_file_accepted, 'The metric file ' + metric_file_accepted + ' was not found in the accepted metrics directory.', parser, 9 )
			verify_file( metric_file_rejected, 'The metric file ' + metric_file_rejected + ' was not found in the rejected metrics directory.', parser, 10 )

	#### OUTPUTS
	# Output directory: args.output_dir
	verify_create_dir( args.output_dir, 'The output directory could not be created.', parser, 11 )
	# Output subdirectories for the accepted values and rejected specimens
	verify_create_dir( args.output_dir + "/accepted", 'The output directory for the accepted scientifics could not be created.', parser, 12 )
	verify_create_dir( args.output_dir + "/rejected", 'The output directory for the specimens with rejected scientific name candidate could not be created.', parser, 13 )
	# Output files
	output_accepted_file = args.output_dir + "/accepted/accepted.tsv"
	output_rejected_file = args.output_dir + "/rejected/rejected.txt"
	verify_create_file( output_accepted_file, 'The output file, for the extracted scientific names, could not be created.', parser, 14 )
	verify_create_file( output_rejected_file, 'The output file of rejected specimens, could not be created.', parser, 15 )
	# Metric folders
	verify_create_dir( args.output_dir + "/accepted/metrics", 'The output metrics directory for the accepted scientific name values could not be created.', parser, 16 )
	verify_create_dir( args.output_dir + "/rejected/metrics", 'The output metrics directory for the rejected specimens could not be created.', parser, 17 )

	################################################################################################################################
	# Copy the accepted values
	try:
		copyfile(suff_accepted_file, output_accepted_file)
	except IOError as e:
		print("\nERROR: Unable to copy the accepted file. %s\n" % suff_accepted_file)
		sys.exit( 18 )
	except:
		print("Unexpected error:", sys.exc_info())
		sys.exit( 18 )

	# Copy the rejected specimens
	try:
		copyfile(suff_rejected_file, output_rejected_file)
	except IOError as e:
		print("\nERROR: Unable to copy the rejected file. %s\n" % suff_rejected_file)
		sys.exit( 19 )
	except:
		print("Unexpected error:", sys.exc_info())
		sys.exit( 19 )
	################################################################################################################################
	# Metric files
	for m_name in args.metric:
		metric_file_accepted = metrics_dir_accepted + "/" + m_name + ".csv"
		metric_file_rejected = metrics_dir_rejected + "/" + m_name + ".csv"
		output_metric_file_accepted = args.output_dir + "/accepted/metrics/" + m_name + ".csv"
		output_metric_file_rejected = args.output_dir + "/rejected/metrics/" + m_name + ".csv"
		# Copy the accepted metric file
		try:
			copyfile(metric_file_accepted, output_metric_file_accepted)
		except IOError as e:
			print("\nERROR: Unable to copy the accepted metric file. %s\n" % metric_file_accepted)
			sys.exit( 20 )
		except:
			print("\nERROR: Unexpected error while copying the accepted metric file. %s\n" % metric_file_accepted)
			sys.exit( 20 )
		# Copy the rejected metric file
		try:
			copyfile(metric_file_rejected, output_metric_file_rejected)
		except IOError as e:
			print("\nERROR: Unable to copy the rejected metric file. %s\n" % metric_file_rejected)
			sys.exit( 20 )
		except:
			print("\nERROR: Unexpected error while copying the rejected metric file. %s\n" % metric_file_rejected)
			sys.exit( 20 )

	sys.exit(0)
