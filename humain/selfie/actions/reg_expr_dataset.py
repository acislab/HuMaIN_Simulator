#!/usr/bin/env python3
import argparse, shutil
import pandas as pd

from humain.common.constants import *
from humain.common.utils import *


if __name__ == '__main__':
	""" Simulated version of the regular expression Event Date extraction
	"""
	parser = argparse.ArgumentParser("Run the simulated version of the regular expression Event Date extraction.")
	parser.add_argument('-d', '--fulltext_dir', action="store", required=True, help="Directory with the fulltext transcription files of the images.")
	parser.add_argument('-f', '--regexp_file', action="store", required=True, help="File with the correspondent Event Date extracted using the regular expresion algorithm.")	
	parser.add_argument('-m', '--metric', action="append", required=False, help="One or more metrics that will be collected when running the regular expression extraction.")
	parser.add_argument('-o', '--out_file', action="store", required=True, help="File with (image, event_date) pairs extracted using regular expression.")
	args = parser.parse_args()
	
	# Usage example
	# python3 reg_expr_dataset.py -d humain/selfie/results/event_date_001/ocr_dataset -d aocr_insects -m duration -o /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/results

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	# args.fulltext_dir
	verify_dir( args.fulltext_dir, 'The fulltext transcription directory (' + args.fulltext_dir + ') was not found: ', parser, 1 )

	# args.regexp_file
	verify_file( args.regexp_file, 'The event dates file (' + args.regexp_file + ') was not found: ', parser, 2 )

	# args.metric
	metrics_dir = os.path.dirname( args.regexp_file )
	if len(args.metric) > 0:
		# Metric directory
		metrics_dir = metrics_dir + "/metrics"
		verify_dir( metrics_dir, 'The metrics directory was not found.', parser, 3 )
		# Metric files
		for m_name in args.metric:
			metric_file = args.regexp_file[:-4] + "/" + m_name + ".csv"
			verify_file( metric_file, 'The file metric ' + metric_file + ' was not found in the metrics directory.', parser, 4 )

	# args.out_file
	verify_create_file( args.out_file, 'The output file, for the extracted event dates, could not be created.', parser, 5 )
	output_metrics_dir = os.path.dirname( args.out_file ) + "/metrics" 
	verify_create_dir( output_metrics_dir, 'The destination metric directory could not be created.', parser, 6 )

	################################################################################################################################
	# LOAD IN A DATAFRAME THE EXTRACTED EVENT DATE VALUES USING REGULAR EXPRESIONS
	################################################################################################################################
	df = pd.read_csv( args.regexp_file, sep='\t', names=['filename', 'value'] )


	# ################################################################################################################################
	# # COPY THE TEXT FILES TO THE EXPERIMENT'S RESULT FOLDER
	# ################################################################################################################################
	# # Create the list of files to process
	# filenames = os.listdir(args.dataset)
	# filename_list = list(f for f in filenames if f.endswith('.txt'))
	# try:
	# 	pathfilename = ""
	# 	for filename in filename_list:
	# 		pathfilename = args.dataset + "/" + filename
	# 		shutil.copy( pathfilename, args.out_dir)
	# except (OSError, IOError):
	# 	print('ERROR: The file ' + pathfilename + ' could not be copied to ' + args.out_dir + '.\n')
	# 	sys.exit(8)

	# ################################################################################################################################
	# # INSERT THE LINES WITH THE METRIC'S VALUES - FOR EACH METRIC
	# ################################################################################################################################	
	# if len(args.metric) > 0:
	# 	# Metric files
	# 	for m_name in args.metric:
	# 		metric_filename_src = metrics_dir + "/" + m_name + ".csv"
	# 		try:
	# 			shutil.copy( metric_filename_src, output_metrics_dir )	
	# 		except (OSError, IOError):
	# 			print('ERROR: The metric file ' + metric_filename_src + ' could not be found or copied to ' + output_metrics_dir + '.\n')
	# 			sys.exit(8)

	sys.exit(0)