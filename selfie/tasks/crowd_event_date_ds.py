#!/usr/bin/env python3
import argparse, shutil
import pandas as pd

from humain.constants import *
from humain.utils import *

if __name__ == '__main__':
	""" Get the simulated results of the crowdsourced transcription of Event Date
	"""
	parser = argparse.ArgumentParser("Get the simulated results of the crowdsourced transcription of Event Date.")
	parser.add_argument('-s', '--specimens', action="store", required=True, help="Text file with the list of specimens for which no event date has been extracted.")
	parser.add_argument('-f', '--crowd_data', action="store", required=True, help="tsv file with the crowdsourced data from the volunteers.")
	parser.add_argument('-m', '--metric', action="append", required=True, help="One or more metrics that will be collected when executing the crowdsourcing.")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="tsv with the transcription made by the volunteers for the specified list of specimens.")
	args = parser.parse_args()
	# Usage example: python3 crowd_event_date_ds.py 
	# -s /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/reg_expr_ds/rejected/rejected.txt 
	# -f /home/ialzuru/Summer2019/HuMaIN_Simulator/datasets/aocr_insects/crowd/terms/event_date.tsv 
	# -m duration 
	# -o /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/crowd_event_date_ds/crowd_event_date.tsv
	# python3 crowd_event_date_ds.py -s /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/reg_expr_ds/rejected/rejected.txt -f /home/ialzuru/Summer2019/HuMaIN_Simulator/datasets/aocr_insects/crowd/terms/event_date.tsv -m duration -o /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/results/event_date_001/crowd_event_date_ds/crowd_event_date.tsv
	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	#### INPUTS
	# args.specimens
	verify_file( args.specimens, 'The file with the list of specimens to crowdsource could not be read (' + args.specimens + ').', parser, 1 )
	
	# args.crowd_data
	verify_file( args.crowd_data, 'The file with crowdsourced data for the simulation could not be read (' + args.crowd_data + ').', parser, 2 )
	input_metrics_dir = os.path.dirname( args.crowd_data ) + "/metrics"
	verify_dir( input_metrics_dir, 'The input metrics directory was not found.', parser, 3 )

	# args.metric
	for m_name in args.metric:
		basename = args.crowd_data.split('/')[-1].split('.')[0]
		metric_file = input_metrics_dir + "/" + basename + "_" + m_name + ".csv"
		verify_file( metric_file, 'The metric file ' + metric_file + ' was not found in the metrics directory.', parser, 4 )

	#### OUTPUTS
	# Output file: args.output_file
	output_dir = os.path.dirname( args.output_file )
	verify_create_dir( output_dir, 'The output directory could not be created (' + output_dir + ').', parser, 5 )
	verify_create_file( args.output_file, 'The output file, for the transcribed event dates, could not be created (' + args.output_file + ').', parser, 6 )
	# Metrics
	output_metrics_dir = output_dir + "/metrics"
	verify_create_dir( output_metrics_dir, 'The output directory for the metric values could not be created (' + output_metrics_dir + ').', parser, 7 )

	################################################################################################################################
	# Load in a list the specimens that need to be processed
	specimens_list = []
	with open(args.specimens, "r") as f_s:
		for line in f_s:
			specimens_list.append( line[:-1].strip() )

	################################################################################################################################
	# Load in a dataframe the crowdsourced data
	df_crowd = pd.read_csv( args.crowd_data, sep='\t' )
	df_crowd = df_crowd.fillna('')

	################################################################################################################################
	# Copy the crowdsourced data for the selected specimens and create a tsv file with this data
	crowd_data_string = ""
	for index, row in df_crowd.iterrows():
		if row['filename'] in specimens_list:
			crowd_data_string += row['filename'] + "\t" + row['event_date1'] + "\t" + row['event_date2'] + "\t" + row['event_date3'] + "\n"

	with open( args.output_file, "w+" ) as f_out:
		f_out.write( crowd_data_string )

	################################################################################################################################
	# Copy the metric values for each of the selected metrics of the specimens of interest
	for m_name in args.metric:
		basename = args.crowd_data.split('/')[-1].split('.')[0]
		metric_file = input_metrics_dir + "/" + basename + "_" + m_name + ".csv"
		# Dataframe of the metric file
		df_in_me = pd.read_csv( metric_file )
		df_in_me = df_in_me.fillna('')

		metric_string = ""
		for index, row in df_in_me.iterrows():
			if row['filename'] in specimens_list:
				metric_string += row['filename'] + "," + str(row['sec1']) + "," + str(row['sec2']) + "," + str(row['sec3']) + "\n"

		output_metric_filename = output_metrics_dir + "/" + m_name + ".csv"
		with open( output_metric_filename, "w+" ) as f_m:
			f_m.write( metric_string )

	sys.exit(0)		
