#!/usr/bin/env python3
import argparse
import pandas as pd

from humain.common.constants import *
from humain.common.utils import *


if __name__ == '__main__':
	""" Get the simulated execution result from an OCR engine
	"""
	parser = argparse.ArgumentParser("Run the specified OCR engine over all the images of an specified collection.")
	parser.add_argument('-cr', '--crowd_file', action="store", required=True, help="Reference tsv file with the values transcribed by the volunteers.")
	parser.add_argument('-co', '--consensus_file', action="store", required=True, help="tsv file with the values transcribed by the volunteers.")
	parser.add_argument('-m', '--metric', action="append", required=True, help="One or more metrics that will be collected during the consensus execution.")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted and rejected transcriptions will be stored.")
	args = parser.parse_args()

	# Usage:
	# python3 ./consensus_dataset.py -cr /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/crowd_event_date_dataset/crowd_event_date.tsv -co /home/ialzuru/Summer2019/HuMaIN_Simulator/datasets/aocr_mix100/consensus/accepted.tsv -m duration -o /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/consensus_dataset

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	#### INPUTS
	# args.crowd_file
	verify_file( args.crowd_file, 'The file with the referential crowdsourced values for Event Date (' + args.crowd_file + ') was not found: ', parser, 1 )

	# args.crowd_file
	verify_file( args.consensus_file, 'The file with the simulation values for the consensus (' + args.consensus_file + ') was not found: ', parser, 2 )

	# args.metric
	input_metrics_dir = os.path.dirname( args.consensus_file ) + "/metrics"
	if len(args.metric) > 0:
		# Metric directory
		verify_dir( input_metrics_dir, 'The input metrics directory was not found.', parser, 3 )
		# Metric files
		for m_name in args.metric:
			metric_file = input_metrics_dir + "/" + m_name + ".csv"
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
	df_crowd = pd.read_csv( args.crowd_file, sep='\t', names=['filename', 'value1', 'value2', 'value3'] )
	df_crowd = df_crowd.fillna('')

	################################################################################################################################
	# LOAD IN A DICTIONARY THE FILENAMES AND THE CORRESPONDENT CONSENSUAL VALUE
	accepted_dict = {}
	with open( args.consensus_file, "r" ) as f_c:
		for line in f_c:
			line = line[:-1]
			filename, value = line.split('\t')
			accepted_dict[ filename ] = value

	################################################################################################################################
	# CREATE THE ACCEPTED AND REJECTED FILES
	accepted_text = ""
	rejected_text = ""
	filename_list = []
	for index, row in df_crowd.iterrows():
		filename_list.append( row['filename'] )
		if row['filename'] in accepted_dict.keys():
			accepted_text += row['filename'] + "\t" + accepted_dict[ row['filename'] ] + "\n"
		else:
			rejected_text += row['filename'] + "\t" + row['value1'] + "\t" + row['value2'] + "\t" + row['value3'] + "\n"

	with open( accepted_file, "w+") as f_a:
		f_a.write( accepted_text )

	with open( rejected_file, "w+") as f_r:
		f_r.write( rejected_text )

	################################################################################################################################
	# CREATE THE METRIC FILES
		
	# For each metric, divide the values in Accepted and Rejected
	for m_name in args.metric:
		# Loads the metric values in a dataframe
		metric_file = input_metrics_dir + "/" + m_name + ".csv"
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