#!/usr/bin/env python3
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
def combine_and_write(iter_no, ele_list):
	# write into file
	temp_str = "[TASK" + str(iter_no).rjust(3, '0') + "]" + "\n"
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
	result_replace = "results/"+output_name[0]+"/"+output_name[0]+str(iter_no).rjust(3, '0')+"/"
	task_str = re.sub(result_find, result_replace, task_str)
	f.write(task_str+"\n")


# copying the remaining parts of the file
def copy_remaining_file(part_to_copy):
	lines = read_section_lines(simulation_file, part_to_copy)
	f.write(part_to_copy)
	f.write("\n")
	f.write(lines)
	f.write("\n")


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

	project_dir = PROJECTS_DIR + "/" + args.project
	simulation_file = project_dir + "/simulations/" + args.simulation_file
	output_dir = project_dir + "/simulations/" + args.output_file
	# verify the creation of the output file. 
	verify_create_file( output_dir, 'The output file could not be created.', parser, 4 )

	# Usage: ./create_sim_set.py -p selfie -w event_date -t ocr -a dataset -v datasets/aocr_mix100/ocr/ocropus -v datasets/aocr_mix100/ocr/tesseract -v datasets/aocr_mix100/ocr/gc-ocr -o sim_set_001
	# usage: python3 common/create_sim_set.py -p selfie -w event_date -s event_date_001.csv -a ocr_dataset -d dataset -v datasets/aocr_mix100/ocr/tersseract -v datasets/aocr_mix100/ocr/g_ocr -o new_sim.csv
	# usage: python3 common/create_sim_set.py -p selfie -w event_date -s event_date_001.csv -a ocr_dataset -d dataset -v datasets/aocr_mix100/ocr/tersseract -o new_sim.csv
	# usage: python3 common/create_sim_set.py -p selfie -w event_date -s event_date_001.csv -a crowd_event_date_dataset -d crowd_data -v HELLOWORLD -o new_sim.csv

	lines = read_section_lines(simulation_file, "[TASKS]")
	data = lines.split("\n")
	# has data for each Task 
	data_list = []
	f = open(output_dir, "w+")
	
	for var in data:
		temp_list = var.split(",")
		data_list.append(temp_list)

	iter_no = 1
	for param in args.value:
		read_sim_file(param)
		combine_and_write(iter_no, data_list)
		iter_no += 1

	copy_remaining_file("[METRICS]")
	copy_remaining_file("[POST-PROCESSING]")
