#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Consensus algorithm to get a final value from the crowdsourced data.
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

import os, sys, csv, time
import argparse, numpy
import pandas as pd
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

Acceptance_Threshold = 0.75

##############################################################################################################################################################
# Returns the string with the highets average similarity to the others. If two strings are the same, returns that string.
def winner( v_ ):
	n = len(v_)
	sim = [0.0] * n
	
	if n == 1: return -1, 1.0
		
	i = 0
	while(i < n):
		j = i + 1
		while(j < n):
			if v_[i] == v_[j]:
				return(i, 1.0)
			s = 1.0 - normalized_damerau_levenshtein_distance( v_[i], v_[j] )
			sim[i] = sim[i] + s
			sim[j] = sim[j] + s
			j = j + 1	
		i = i + 1

	# Search maximum and return the index
	sim_max = sim[0]
	i_max = 0
	i = 1
	while(i < n):
		if (sim_max < sim[i]):
			i_max = i
			sim_max = sim[i]
		i = i + 1
		
	return i_max, (sim_max/(n-1))

#-------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	""" Consensus algorithm to get a final value from the crowdsourced data.
	"""
	parser = argparse.ArgumentParser("Consensus algorithm to get a final value from the crowdsourced data.")
	parser.add_argument('-c', '--crowd_file', action="store", required=True, help="tsv file with the three crowdsourced values.")
	parser.add_argument('-o', '--output_dir', action="store", required=True, help="Directory where the accepted, rejected, and metric files will be saved.")
	args = parser.parse_args()

	# Usage:
	# python3 consensus.py -c ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/crowd/terms/zooniverse/scientific_name.tsv -o ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/sn_consensus
	# python3 consensus.py -c ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/crowd/terms/zooniverse/recorded_by.tsv -o ~/Fall2019/HuMaIN_Simulator/datasets/aocr_mix100/rb_consensus

	# CRITERIA:
	# Given the set of values available for each specimen, the script will compute the similarity of each candidate with 
	# all the other candidates, accumulating the similarity values. The candidate with the highest similarity value will be the winner.
	# If two candidates have the same cumulative similarity, the first candidate with that similarity will be picked up.

	##########################################################################################
	# PARAMETERS VERIFICATION
	if ( not os.path.isfile( args.crowd_file ) ):
		print('\nERROR: The crowdsourced data file was not found.\n')
		parser.print_help()
		sys.exit(1)

	if not os.path.exists( args.output_dir ):
		try:
			os.makedirs( args.output_dir )  
		except:
			print('Error: The destination directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(3)	

	if not os.path.exists( args.output_dir + "/accepted" ):
		try:
			os.makedirs( args.output_dir + "/accepted" )  
		except:
			print('Error: The "accepted" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(4)	
	
	if not os.path.exists( args.output_dir + "/rejected" ):
		try:
			os.makedirs( args.output_dir + "/rejected" )  
		except:
			print('Error: The "rejected" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(5)	

	if not os.path.exists( args.output_dir + "/accepted/metrics" ):
		try:
			os.makedirs( args.output_dir + "/accepted/metrics" )  
		except:
			print('Error: The "accepted/metrics" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(6)	

	if not os.path.exists( args.output_dir + "/rejected/metrics" ):
		try:
			os.makedirs( args.output_dir + "/rejected/metrics" )  
		except:
			print('Error: The "rejected/metrics" directory was not found and could not be created.\n')
			parser.print_help()
			sys.exit(7)	
	##########################################################################################
	# Read the file and load it in a DataFrame
	df = pd.read_csv( args.crowd_file, sep='\t' )
	df = df.fillna('')
	
	##########################################################################################
	# Compute the Damerau Levenshtein similarity among the transcribed values
	accepted_text = ""
	rejected_text = ""
	duration_accepted_text = ""
	duration_rejected_text = ""
	for index, row in df.iterrows():
		start_time = time.time()
		w_id, w_sim = winner( [ row['value1'], row['value2'], row['value3'] ] )
		if w_sim >= Acceptance_Threshold:
			# Accept the value
			if w_id in [0,1,2]:
				w_id = w_id + 1
				consensus_value = row['value' + str(w_id)]
				accepted_text += row['filename'] + '\t' + consensus_value + '\n'
				duration_accepted_text += row['filename'] + ',' + str(time.time() - start_time) + '\n'
			else:
				print("\nERROR: The winner index of the value returned by the consensus function is out of range (" + str(w_id) + ").\n")
				sys.exit(2)
		else:
			# Reject the values and save the specimen in the rejected list
			rejected_text += row['filename'] + '\n'
			duration_rejected_text += row['filename'] + ',' + str(time.time() - start_time) + '\n'

	# Save the text in the correspondent files
	with open(args.output_dir + "/accepted/accepted.tsv", "w+") as f_a:
		f_a.write( accepted_text )
	with open(args.output_dir + "/accepted/metrics/duration.csv", "w+") as f_d_a:
		f_d_a.write( duration_accepted_text )
	with open(args.output_dir + "/rejected/rejected.tsv", "w+") as f_r:
		f_r.write( rejected_text )
	with open(args.output_dir + "/rejected/metrics/duration.csv", "w+") as f_d_r:
		f_d_r.write( duration_rejected_text )	
