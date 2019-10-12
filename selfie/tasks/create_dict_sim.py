#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Simulates the creation of a dictionary from a data file
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

import sys, argparse
from shutil import copyfile

from humain.constants import *
from humain.utils import *

if __name__ == '__main__':
	""" Simulates the creation of a dictionary from a data file
	"""
	parser = argparse.ArgumentParser("Simulates the creation of a dictionary from a data file.")
	parser.add_argument('-a', '--accepted_file', action="store", required=True, help="File of accepted values (.tsv)")
	parser.add_argument('-d', '--dict_file', action="store", required=True, help="Dictionary already created from the values in the accepted file.")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="Output file where the values with their repetition count will be saved.")
	args = parser.parse_args()

	# Usage:
	# python3 rb_create_dict.py -a ~/Fall2019/HuMaIN_Simulator/selfie/results/recorded_by/consensus/accepted/accepted.tsv -d ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/consensus/recorded_by/accepted/dict_recorded_by.tsv -o ~/Fall2019/HuMaIN_Simulator/selfie/results/recorded_by/rb_create_dict/dictionary.tsv

    ################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
	# INPUTS #
	# args.accepted_file
	verify_file( args.accepted_file, 'The file with the accepted values was not found (' + args.accepted_file + ').', parser, 1 )
	# args.dict_file
	verify_file( args.dict_file, 'The dictionary file was not found (' + args.dict_file + ').', parser, 2 )
	#################################################################
    # OUTPUTS #
	# args.output_file
	output_dir = os.path.dirname( args.output_file )
	verify_create_dir( output_dir, 'The output directory could not be created (' + output_dir + ').', parser, 3 )
	verify_create_file( args.output_file, 'The output file, for the dictionary of values, could not be created (' + args.output_file + ').', parser, 4 )

    ################################################################################################################################
	# Copy the Dictionary File
	try:
		copyfile(args.dict_file, args.output_file)
	except IOError as e:
		print("\nERROR: Unable to copy the dictionary file.\n")
		exit(5)
	except:
		print("\nERROR: Unexpected error:", sys.exc_info(), "\n")
		exit(6)

	sys.exit(0)
