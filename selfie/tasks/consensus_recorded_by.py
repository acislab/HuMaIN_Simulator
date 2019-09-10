#!/usr/bin/env python3
import argparse
import pandas as pd
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
from humain.constants import *
from humain.utils import *


if __name__ == '__main__':
	""" Consensus for the recorded by values
	"""
	parser = argparse.ArgumentParser("Consensus for the recorded by values")
	parser.add_argument('-cr', '--crowd_file', action="store", required=True, help="Reference tsv file with the values transcribed by the volunteers.")
	parser.add_argument('-th', '--threshold', action="store", required=True, help="Threshold to decide the distance for acceptance pr rejection.")
	parser.add_argument('-m', '--metric', action="append", required=True, help="One or more metrics that will be collected during the consensus execution.")
	parser.add_argument('-md', '--metric_dir', action="append", required=True, help="Metrics directory for the dataset")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted and rejected transcriptions will be stored.")
	args = parser.parse_args()


	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	#### INPUTS
	# args.crowd_file
	verify_file( args.crowd_file, 'The file with the referential crowdsourced values for Event Date (' + args.crowd_file + ') was not found: ', parser, 1 )

	# args.metric
	# input_metrics_dir = args.metric_dir + "/metrics"
	# input_metrics_file = os.path.dirname(args.metric_dir) + "/metrics"
	input_metrics_dir = open(args.metric_dir[0], 'r')
	input_metrics_file  = input_metrics_dir.readlines()
	input_metrics_dir.close()

	input_metrics_file = BASE_DIR + "/" + input_metrics_file[0] 


	if len(args.metric) > 0:
		# Metric directory
		verify_dir( input_metrics_file, 'The input metrics directory was not found.', parser, 3 )
		# Metric files
		for m_name in args.metric:
			metric_file = input_metrics_file + "/" + m_name + ".csv"
			verify_file( metric_file, 'The metric file ' + metric_file + ' was not found in the metrics directory.', parser, 4 )

	
	#### OUTPUTS
	# args.output_dir
	verify_create_dir( args.output_dir, 'The output directory could not be created.', parser, 5 )
	# Output subdirectories for the accepted values and rejected specimens
	verify_create_dir( args.output_dir + "/accepted", 'The output directory for the accepted event date values could not be created.', parser, 6 )
	verify_create_dir( args.output_dir + "/rejected", 'The output directory for the rejected specimens could not be created.', parser, 7 )
	# Output files
	accepted_file = args.output_dir + "/accepted/accepted.tsv"
	rejected_file = args.output_dir + "/rejected/rejected.tsv"
	verify_create_file( accepted_file, 'The output file, for the extracted event dates, could not be created.', parser, 8 )
	verify_create_file( rejected_file, 'The output file of rejected specimens, could not be created.', parser, 9 )
	# Metric folders
	verify_create_dir( args.output_dir + "/accepted/metrics", 'The output metrics directory for the accepted event date values could not be created.', parser, 10 )
	verify_create_dir( args.output_dir + "/rejected/metrics", 'The output metrics directory for the rejected specimens could not be created.', parser, 11 )

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