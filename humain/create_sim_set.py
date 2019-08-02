#!/usr/bin/env python3

##########################################################################################
# Developers: 	Aditi Malladi and Icaro Alzuru
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Create a new simulation file by using an existing simulation. Have the 
# 				option of having multiple parameters in the same sim file. 
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


import os, sys, argparse, random, csv, re
from utils import *
from constants import *


# function to find the task and replace with passed param
def read_sim_file(param):
	regex_str = " " + args.argument + " = "
	temp_var = -1
	for ele in data_list:
		# search for line which has the task to be changed
		if ele[0] == args.task:
			for var in ele:
				if re.match(r"%s[a-zA-Z0-9]*" % regex_str, var):
					temp_var = ele.index(var)
					ele[temp_var] = regex_str + param


# function to write to a file
def combine_and_write(iter_no, ele_list, string_section):
	# write into file
	temp_str = string_section + str(iter_no).rjust(3, '0') + "]" + "\n"
	f.write(temp_str)

	# re-create task string in file
	for var in ele_list:
		t = ""
		var = t.join(var)

	temp_list = []
	for ele in ele_list:
		t = ","
		temp_str = t.join(ele)
		temp_list.append(temp_str)
	
	s = "\n"
	task_str = s.join(temp_list)

	# find and replace results dir
	result_find = "results/"+args.simulation_file.split(".")[0]+"/"
	output_name = (args.output_file).split(".")
	result_replace = "results/"+output_name[0]+"/"+"TASKS_"+str(iter_no).rjust(3, '0')+"/"
	task_str = re.sub(result_find, result_replace, task_str)
	f.write(task_str+"\n")


# copying the remaining parts of the file
def copy_remaining_file(part_to_copy):
	lines = read_section_lines(simulation_file, part_to_copy)
	f.write(part_to_copy)
	f.write("\n")
	f.write(lines)
	f.write("\n")

# reads the section lines from the file 
# splits the lines
# section variable is the part of the sim file that needs to be read
def read_lines(section, bool_val):
	lines = read_section_lines(simulation_file, section)
	data = lines.split("\n")
	f = open(output_dir, "w+")
	
	for var in data:
		temp_list = var.split(",")
		data_list.append(temp_list)

	iter_no = 1
	for param in args.value:
		if bool_val:
			read_sim_file(param)
			combine_and_write(iter_no, data_list, "[TASKS_")
		else:
			combine_and_write(iter_no, data_list, "[METRICS_")
		iter_no += 1



if __name__ == '__main__':
	""" Generate random values for the files in a directory.
	"""
	parser = argparse.ArgumentParser("Generate random values for the files in a directory.")
	parser.add_argument('-p', '--project', action="store", required=True, help="Project selected")
	parser.add_argument('-s', '--simulation_file', action="store", required=True, help="Simulation to edit")
	parser.add_argument('-t', '--task', action="store", required=True, help="Task to edit")
	parser.add_argument('-a', '--argument', action="store", required=True, help="Task's parameter or argument to change")
	parser.add_argument('-v', '--value', action="append", required=True, help="Value to put for the parameter selected, can send in more than one.")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="Output csv file for the new simulation filename")
	args = parser.parse_args()

	project_dir = BASE_DIR + "/" + args.project
	simulation_file = project_dir + "/simulations/" + args.simulation_file
	output_dir = project_dir + "/simulations/" + args.output_file
	# verify the creation of the output file. 
	verify_create_file( output_dir, 'The output file could not be created.', parser, 4 )

	# usage: python3 create_sim_set.py -p selfie -s event_date_001.csv -t ocr_dataset -a dataset -v datasets/aocr_mix100/ocr/tersseract -o new_sim.csv

	# has data for each Task
	data_list = []
	f = open(output_dir, "w+")
	read_lines("[TASKS]", True)
	
	# copy_remaining_file("[METRICS]")
	data_list = []
	read_lines("[METRICS]", False)


	task_no = 1
	for param in args.value:
		f.write("\n")
		temp_str = "[POST-PROCESSING_" + str(task_no).rjust(3, '0') + "] \n"
		f.write(temp_str)
		f.write("\n")
		task_no += 1

# post processing examples
f.write("\n")
f.write("[POST-PROCESSING]	(Examples) \n")
f.write("# python3 post-processing/box_whisker_plot.py -f <filename1>.csv -f <filename2>.csv \n")
f.write("# python3 post-processing/comparison_bar_graph.py -f <filename1>.csv -f <filename2>.csv -t <Title> -a <sum/average> -o <output_file_name>.png \n")
f.write("# python3 post-processing/comparison_table.py -f <filename1>.csv -f <filename2>.csv -c <column_name> -t <Title> -o <output_file_name>.png \n")
f.write("\n")