#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Using the crowdsourced data, trains the NER model and augments the local 
# 				dictionary for the term.
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

import os, sys, argparse, re
import pandas as pd
import spacy, random
from spacy.util import minibatch, compounding

from humain.constants import *
from humain.utils import *

valid_terms = ["COUNTY", "EVENTDATE", "HABITAT", "RECORDEDBY", "SCIENTIFICNAME", "STATEPROVINCE"]

##############################################################################################################################################################
if __name__ == '__main__':
	""" Using the crowdsourced data, trains the NER model and augments the local dictionary for the term. """
	# Read arguments
	parser = argparse.ArgumentParser("Using the crowdsourced data, trains the NER model and augments the local dictionary for the term.")
	parser.add_argument('-af','--accepted_file',action="store", required=True, help="Accepted file with the filename and crowdsourced term value.")
	parser.add_argument('-td','--training_data_dir',action="store", required=True, help="Directory with the files with the training data for the collection, in spacy format.")
	parser.add_argument('-t','--term',action="store", required=True, help="Darwin Core Term to search and for which the model will be trained.")
	parser.add_argument('-it','--iterations',action="store", required=True, help="Number of iterations to use for training.")
	parser.add_argument('-od', '--output_dir', action="store", required=True, help="Directory with the new Spacy trained model and the new dictionary version.")
	args = parser.parse_args()
	
	# Usage example:
	# python3 ~/Fall2019/HuMaIN_Simulator/selfie/tasks/learning.py -af ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/consensus_sim/accepted/accepted.tsv 
	# 		  -t RECORDEDBY -td ~/Fall2019/HuMaIN_Simulator/datasets/wedigbio/trn_data_spacy_format/wdb_comfort -it 50 -od ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/learning
	
	# python3 ~/Fall2019/HuMaIN_Simulator/selfie/tasks/learning.py -af ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/consensus_sim/accepted/accepted.tsv -t RECORDEDBY -td ~/Fall2019/HuMaIN_Simulator/datasets/wedigbio/trn_data_spacy_format/wdb_comfort -it 10 -od ~/Fall2019/HuMaIN_Simulator/selfie/results/rb_ner_comfort/learning

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
	#### INPUTS
	# args.accepted_file
	verify_file( args.accepted_file, 'The accepted file (' + args.accepted_file + ') was not found: ', parser, 1 )
	# args.training_data_dir
	verify_dir( args.training_data_dir, 'The directory with the training data in spacy format (' + args.training_data_dir + ') was not found: ', parser, 2 )	
	# args.term
	term = args.term.upper()
	if not (term in valid_terms):
		print("\nERROR: The inserted term (" + args.term + ") is not valid.\n")
		parser.print_help()
		sys.exit( 4 )
	# args.iterations
	n_iter = 0
	try:
		n_iter = int(args.iterations)
		if n_iter < 1 or n_iter > 500:
			raise Exception()
	except:
		print( "\nERROR: Invalid number of iterations.\n" )
		parser.print_help()
		sys.exit( -1 )

	#### OUTPUTS
	# Output directory: args.output_dir
	verify_create_dir( args.output_dir, 'The output directory could not be created.', parser, 5 )
	results_dir = os.path.dirname( args.output_dir )	
	# Training data file
	training_data_file = args.output_dir + "/training_data_file.tsv"
	# Directory for the model
	model_directory = args.output_dir + "/model"
	verify_create_dir( model_directory, 'The model for the directory could not be created (' + model_directory + ').', parser, 6 )

	################################################################################################################################
	# Get the number of the last iteration. 0 means "No iterative"
	################################################################################################################################
	current_iteration_number = 1
	try:
		current_iteration_number = int( results_dir.split('_')[-1] )
	except: # If the current iteration directory does not have a number, then it is assumed a sequenctial execution (no iterative)
		current_iteration_number = 0

	################################################################################################################################
	# LOADS THE PREVIOUS DICTIONARY (IF EXISTS)
	################################################################################################################################
	dictionary = {}
	if current_iteration_number > 1:
		previous_iteration_number = current_iteration_number - 1
		previous_results_dir = results_dir.replace("_" + str(current_iteration_number), "_" + str(previous_iteration_number) )
		previous_dict_filename = previous_results_dir + "/learning/dictionary.tsv"
		#
		verify_file( previous_dict_filename, 'The previous dictionary file could not be read (' + previous_dict_filename + ').', None, 7 )
		df_dict = pd.read_csv( previous_dict_filename, sep='\t', names = ['word', 'count'], encoding='utf8', dtype = {'word':str, 'count':int} )
		df_dict = df_dict.fillna('')
		for index, row in df_dict.iterrows():
			dictionary[ row['word'] ] = int(row['count'])

	################################################################################################################################
	# Read the specimens files that will be processed
	################################################################################################################################
	df = pd.read_csv( args.accepted_file, sep='\t', names = ['filename', 'value'], encoding='utf8', dtype = {'filename':str, 'value':str} )
	df = df.fillna('')

	################################################################################################################################
	# Loads each file and search the value. It generates a training line of each value that matches.
	################################################################################################################################
	TRAIN_DATA = []
	training_text = ""
	# j = 1
	for index, row in df.iterrows():
		# Standarize the gold value in lower case and no special characters
		gold_value = re.sub(r'[^\w\s]', ' ', row['value'].lower(), re.UNICODE).replace('  ', ' ').replace('  ', ' ')
		# The value if added to the dictionary or the count incremented
		if gold_value in dictionary.keys():
			dictionary[ gold_value ] = dictionary[ gold_value ] + 1
		else:
			dictionary[ gold_value ] = 1

		# Read the data file
		tr_data_filename = args.training_data_dir + "/" + row['filename']
		if not os.path.isfile( tr_data_filename ):
			print("\nERROR: The file with the training data was not found (" + tr_data_filename + ").")
			continue
		with open( tr_data_filename ) as f_d:
			lines = f_d.readlines()
		lines = [x.strip() for x in lines]

		# Process line by line in search of the value
		for line in lines:
			segments = line.split("\t")
			sentence = segments[0]			
			i = 1
			while (i+2) < len(segments):
				if segments[i+2] == term:
					candidate_value = sentence[ int(segments[i]):int(segments[i+1]) ]
					# Standarize the candidate value in lower case and no special characters
					candidate_value = re.sub(r'[^\w\s]', ' ', candidate_value.lower(), re.UNICODE).replace('  ', ' ').replace('  ', ' ')
					if gold_value == candidate_value:
						training_text += sentence + "\t" + segments[i] + "\t" + segments[i+1] + "\t" + term + "\n"
						# 
						tuples_list = [ (int(segments[i]), int(segments[i+1]), term) ]
						dict_entities = {}
						dict_entities["entities"] = tuples_list
						TRAIN_DATA.append( (sentence, dict_entities) )
						# Exit
						i = len(segments)
					# else:
					# 	print(tr_data_filename, gold_value, candidate_value, row['value'], sentence[ int(segments[i]):int(segments[i+1]) ])

				i = i + 3
		# j = j + 1 
		# if j >= 8:
		# 	break
	################################################################################################################################	
	# Write the training data file, for validation or debugging purposes
	################################################################################################################################
	with open(training_data_file, "w+") as f_t:
		f_t.write( training_text )

	################################################################################################################################	
	# Save the dictionary to disk
	################################################################################################################################
	dict_text = ""
	for key in dictionary.keys():
		dict_text += key + "\t" + str(dictionary[key]) + "\n"
	#
	new_dict_filename = results_dir + "/learning/dictionary.tsv"
	with open( new_dict_filename, "w+" ) as f_dict:
		f_dict.write( dict_text )
	print("Dictionary saved to", new_dict_filename)

	################################################################################################################################
	# Spacy's training process
	################################################################################################################################
	# Gets and loads the model to train
	base_model_name = "en_core_web_sm"
	if current_iteration_number > 1:
		previous_iteration_number = current_iteration_number - 1
		previous_results_dir = results_dir.replace("_" + str(current_iteration_number), "_" + str(previous_iteration_number) )
		base_model_name = previous_results_dir + "/learning/model"

	print("Model loaded for training: " + base_model_name)
	nlp = spacy.load( base_model_name )
	print("number of Iterations: " + str(n_iter))
	
	# create the built-in pipeline components and add them to the pipeline. nlp.create_pipe works for built-ins that are registered with spaCy
	if "ner" not in nlp.pipe_names:
		ner = nlp.create_pipe("ner")
		nlp.add_pipe(ner, last=True)
	else: # otherwise, get it so we can add labels
		ner = nlp.get_pipe("ner")

	################################################################################################################################
	# Add labels
	for _, annotations in TRAIN_DATA:
		for ent in annotations.get("entities"):
			ner.add_label(ent[2])

	# Get names of other pipes to disable them during training
	other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
	with nlp.disable_pipes(*other_pipes):  # only train NER
		for itn in range(n_iter):
			random.shuffle(TRAIN_DATA)
			losses = {}
			# batch up the examples using spaCy's minibatch
			batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
			for batch in batches:
				texts, annotations = zip(*batch)
				nlp.update(
					texts,  # batch of texts
					annotations,  # batch of annotations
					drop=0.5,  # dropout - make it harder to memorise data
					losses=losses,
				)
	################################################################################################################################
	# Save the trained model to the correspondent directory
	nlp.to_disk(model_directory)
	print("Model saved to", model_directory)