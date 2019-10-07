#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Computes the mean, median, standard deviation, min, and max of a metric file
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

from humain.utils import verify_file


if __name__ == '__main__':
	""" Computes the mean, median, standard deviation, min, and max of a metric file.
	"""
	parser = argparse.ArgumentParser("Computes the mean, median, standard deviation, min, and max of a metric file.")
	parser.add_argument('-m', '--metric_file', action="append", required=True, help="CSV metric file with the values in the second column.")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="Output file where the basic statistics will be saved.")
	args = parser.parse_args()

	# Parameters' verification
	for metric_file in args.metric_file:
		verify_file( metric_file, 'The input metric file (' + metric_file + ') was not found.', None, 1 )

	df = pd.DataFrame(columns=['specimen','value'], dtype={'specimen':str, 'value':float})
	for metric_file in args.metric_file:
		df_metric = pd.DataFrame(columns=['specimen','value'], dtype={'specimen':str, 'value':float})
		# Read the file and load it in a dataframe
		try:
			df_metric = pd.read_csv( metric_file, sep=',', names=['specimen', 'value'])
			df_metric.fillna('', inplace= True)
			df = pd.concat( [df, df_metric] )
		except pd.io.common.EmptyDataError:
			continue

	mean = df.loc[:,"value"].mean()
	median = df.loc[:,"value"].median()
	std_dev = df.loc[:,"value"].std()
	min_val = df['value'].min()
	max_val = df['value'].max()

	output_text = "Number of lines: " + str(df.shape[0]) + "\n"
	output_text += "Mean: " + str(mean) + "\n"
	output_text += "Median: " + str(median) + "\n"
	output_text += "Standard Deviation: " + str(std_dev) + "\n"
	output_text += "Minimum: " + str(min_val) + "\n"
	output_text += "Maximum: " + str(max_val) + "\n"
	with open( args.output_file, "w+") as f_output:
		f_output.write( output_text )