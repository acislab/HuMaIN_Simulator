#!/usr/bin/env python3
import argparse
import pandas as pd
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
from humain.constants import *
from humain.utils import *

if __name__ == '__main__':
	""" Create a dictionary of recorded_by names from consensus file
	"""
	parser = argparse.ArgumentParser("Create dictionary of recorded-by names")
	parser.add_argument('-a', '--accepted', action="store", required=True, help="File of accepted recorded-by names (.tsv)")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="Output file where the recorded by names with frequency will be saved")
	args = parser.parse_args()

    ################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	# INPUTS
	# args.accepted
	verify_file( args.accepted, 'The file with the accepted values of recorded-by names was not found: ', parser, 1 )

    # OUTPUTS
	# Output file: args.output_file
	output_dir = os.path.dirname( args.output_file )
	verify_create_dir( output_dir, 'The output directory could not be created (' + output_dir + ').', parser, 5 )
	verify_create_file( args.output_file, 'The output file, for the transcribed names recorded, could not be created (' + args.output_file + ').', parser, 6 )

    ################################################################################################################################
	# READ THE ACCPETED AND ADD TO DICT
	accepted_rec_by = {}
	with open( args.accepted, "r" ) as f_c:
		for line in f_c:
			line = line[:-1]
			filename, value = line.split('\t')
			if value in accepted_rec_by.keys():
				accepted_rec_by[value] = accepted_rec_by[value] + 1
			else:
				accepted_rec_by[value] = 1

	# WRITE DICT VALUES INTO OUTPUT FILE
	output_file = open(args.output_file, "w+")
	for key in accepted_rec_by.keys():
		s = key + "," + str(accepted_rec_by[key]) + "\n"
		output_file.write(s)

	sys.exit(0)


