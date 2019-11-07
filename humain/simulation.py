#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Simulation class. Loads in memory all the simulation structure: Workflow, 
# 				Tasks, Parameters, and Simulation. It permits to run pure- and HITL- 
# 				simulations.
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

import sys, networkx as nx
import matplotlib.pyplot as plt
import ntpath, subprocess, re
import xml.etree.ElementTree as ET

from humain.constants import *
from humain.utils import *


class Simulation:
	'Sequence of tasks to execute'
	######################################################################################################################################
	# Constructor
	def __init__(self, prj_name, wfw_name, sim_par_name):
		##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##--
		# Project's Directory
		self.project_dir = BASE_DIR + "/" + prj_name
		verify_dir( self.project_dir, 'The project directory (' + self.project_dir + ') was not found: ', None, 1 )

		# Workflows Directory 
		self.workflows_dir = self.project_dir + "/workflows" 
		verify_dir( self.workflows_dir, 'The workflows directory (' + self.workflows_dir + ') was not found: ', None, 2 )

		# Workflow Definition File
		self.workflow_pathfilename = self.workflows_dir + "/" + ntpath.basename( wfw_name ).replace('.csv', '') + ".csv"
		verify_file( self.workflow_pathfilename, 'The workflow file (' + self.workflow_pathfilename + ') was not found.', None, 3 )

		# Tasks Directory 
		self.tasks_dir = self.project_dir + "/tasks" 
		verify_dir( self.tasks_dir, 'The tasks directory (' + self.tasks_dir + ') was not found: ', None, 4 )

		# Simulations Directory
		self.simulations_dir = self.project_dir + "/simulations"
		verify_dir( self.simulations_dir, 'The simulations directory (' + self.simulations_dir + ') was not found: ', None, 5 )

		# File with the simulation parameters of the workflow
		self.params_pathfilename = self.simulations_dir + "/" + ntpath.basename( sim_par_name ).replace('.xml', '') + ".xml"
		verify_file( self.params_pathfilename, 'The simulation parameters file (' + self.params_pathfilename + ') was not found.', None, 6 )

		# Results directory: self.project_results
		results_dir = self.project_dir + "/results"
		verify_create_dir( results_dir, 'The results directory (' + results_dir + ') was not found and could not be created.', None, 7 )
		self.project_results = results_dir + "/" + ntpath.basename(sim_par_name).replace('.xml', '')
		verify_create_dir( self.project_results, 'The directory to store the execution results(' + self.project_results + ') and could not be created.', None, 8 )

		# Execution Log 
		self.log_pathfilename = self.project_results + "/" + ntpath.basename( sim_par_name ) + ".log"

		##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##--
		##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##--

		# Workflow = Graph
		self.workflow = nx.DiGraph()
		self.iterative = False			# Yes -> HITL execution
		self.stop_task = None			# Task that will decide when to stop the simulation

		# Task(s) to be executed next
		self.next_task = []

		# Load the structure of tasks
		self.load_tasks( )

		# Load the parameters of every tasks of the workflow
		self.load_parameters( )

		# Load the values for each of the Tasks' parameters
		self.load_values( )

	######################################################################################################################################
	# Load the nodes (tasks) and structure of the IE workflow
	def load_tasks(self):
		with open( self.workflow_pathfilename, "r+" ) as wf:
			for line in wf:
				line = line[:-1].replace(' ', '')
				if line == "":
					continue
				tasks = line.split(',')
				n_a = len(tasks)
				if n_a == 1:
					self.next_task.append( tasks[0] )
					self.workflow.add_node( tasks[0], executed = False )
				elif n_a > 1:
					if (not (tasks[0] in self.workflow)):
						self.workflow.add_node( tasks[0], executed = False )
					i = 1
					while (i < n_a):
						if (not (tasks[i] in self.workflow)):
							self.workflow.add_node( tasks[i], executed = False )
						self.workflow.add_edge( tasks[i], tasks[0] )
						i = i + 1
	
	######################################################################################################################################
	# Draw the graph of tasks and the order of execution
	def draw_workflow(self):
		pos = nx.circular_layout(self.workflow)    
		nx.draw(self.workflow, pos, with_labels = True, edge_color = 'b')  
		#node_labels = nx.get_node_attributes(self.workflow, 'param_types')
		node_labels = nx.get_node_attributes(self.workflow, 'param_values')
		nx.draw_networkx_labels(self.workflow, pos, labels = node_labels)
		plt.show()
	
	######################################################################################################################################
	# Load inputs and outputs of every (tasks) and save them as nodes' attributes in the graph
	def load_parameters(self):
		# Load the content of the xml simulation file, creates element tree object, and get the root
		root_sim = ET.parse( self.params_pathfilename ).getroot()
		# Read the type of workflow and its parameters
		for s in root_sim.findall('simulation'):
			iterative_tag = s.find('iterative')
			iterative_value = ""
			# iterative Tag
			if not (iterative_tag is None):
				iterative_value = str(iterative_tag.text)
			if iterative_value.lower() == "yes":
				self.iterative = True
				# stop_task tag
				stop_task_tag = s.find('stop_task')
				if not (stop_task_tag is None):
					self.stop_task = str(stop_task_tag.text)

		# Load the content of the tasks.xml file
		tasks_xml = self.project_dir + "/tasks.xml"
		verify_file( tasks_xml, "The tasks' description file (" + tasks_xml + ") was not found.", None, 9 )

		root_tasks = ET.parse( tasks_xml ).getroot()
		workflow_tasks = list(self.workflow.node)
		# Process every task
		for task in root_tasks.findall('task'):
			task_name = task.get('name')
			if task_name in workflow_tasks:
				# Python script for the task
				script_name = self.tasks_dir + "/" + task_name + ".py"
				verify_file( script_name, 'The Python script for the task (' + task_name + ') was not found.', None, 10 )
				# The script is added as attribute for the node
				self.workflow.node[ task_name ]['script'] = script_name

				para_type_dict = {}
				para_value_dict = {}
				# Process every parameter
				for parameter in task.findall('parameter'):
					para_name = parameter.get('name')
					para_type = parameter.get('type')
					# Validate the datatype of the parameter
					if not(para_type in DATATYPES):
						print( "\nERROR: In definition of Task " + task_name + ", datatype " + para_type + " does not exist.\n" )
						sys.exit( 11 )
					para_type_dict[ para_name ] = para_type
					para_value_dict[ para_name ] = None

				# The validated list of parameters is added as an attribute to the node
				self.workflow.node[ task_name ]['param_types'] = para_type_dict
				self.workflow.node[ task_name ]['param_values'] = para_value_dict

	######################################################################################################################################
	# Load the values for each of the Tasks' parameters
	def load_values(self):
		# Create element tree object and get the root
		root = ET.parse( self.params_pathfilename ).getroot()
		# Process every task
		for task in root.findall('tasks/task'):
			task_name = task.get('name')
			# Check if the task was previously defined
			if not(task_name in list(self.workflow)):
				print( "\nERROR: The task " + task_name + " was not defined in the workflow.\n" )
				sys.exit( 12 )

			# Process every parameter
			for parameter in task.findall('parameter'):
				para_name = parameter.get('name')
				para_value = str(parameter.text)
				# Check if the parameter exist for the task
				if not( para_name in self.workflow.node[ task_name ]['param_values'] ):
					print( "\nERROR: Parameter " + para_name + " has not been defined in Task " + task_name + ".\n" )
					sys.exit( 13 )
				# We assign the value to the parameter
				# Values are treated as lists because there may be multiple values
				if self.workflow.node[ task_name ]['param_values'][ para_name ]:
					#print([ para_value ])
					self.workflow.node[ task_name ]['param_values'][ para_name ] += [ para_value ]
				else:
					self.workflow.node[ task_name ]['param_values'][ para_name ] = [ para_value ]

			# Verification that all the parameters have an assigned value
			for para_name in self.workflow.node[ task_name ]['param_values']:
				if self.workflow.node[ task_name ]['param_values'][ para_name ] is None:
					print( "\nERROR: No value was defined for parameter " + para_name + " of Task " + task_name + " in the simulation file.\n" )
					sys.exit( 14 )

	######################################################################################################################################
	# Returns the parameters to run the especified Task
	def get_execution_parameters(self, task_name ):
		args_list = []
		if task_name in list(self.workflow):
			param_types = self.workflow.node[ task_name ]['param_types']
			param_values = self.workflow.node[ task_name ]['param_values']
			for p_name, p_type in param_types.items():
				# Validate existence of the parameter and its value
				if not (p_name in param_values.keys()):
					print( "\nERROR: The parameter " + p_name + " has not been defined for Task " + task_name + ".\n" )
					sys.exit( 15 )
				if param_values[ p_name ] is None:
					print( "\nERROR: The parameter " + p_name + " has no assigned value for Task " + task_name + ".\n" )
					sys.exit( 16 )

				p_value_list = param_values[ p_name ]
				for p_value in p_value_list:
					args_list.append("--" + p_name)
					# Directory
					if p_type in ['D_JPG', 'D_TXT', 'D_JSON']:
						dir_name = BASE_DIR + "/" + p_value
						ext = p_type.split('_')[-1]
						if not( verify_dir_ext( dir_name, ext ) ):
							# print( "\nWARNING: Execution of " + task_name + ". Directory " + dir_name + " does not exist or does not contain " + ext + " files.\n" )
							# sys.exit( 17 )
							write_log(self.log_pathfilename, "WARNING: Execution of " + task_name + ". Directory " + dir_name + " does not exist or does not contain " + ext + " files.")
						#
						args_list.append(dir_name)
					# File
					elif p_type in ['TXT', 'JPG', 'TSV']:
						filename = BASE_DIR + "/" + p_value
						ext = p_type.split('_')[-1]
						if not( verify_file_ext( filename, ext ) ):
							print( "\nERROR: Execution of " + task_name + ". File " + filename + " does not exist or does not have " + ext + " extension.\n" )
							sys.exit( 18 )
						# 
						args_list.append(filename)
					elif p_type in ['INT', 'FLOAT']:
						if not (p_value.replace('.','',1).isdigit()):
							print( "\nERROR: Execution of " + task_name + ". " + p_name + "'s value is not numeric: " + str(p_value) + ".\n" )
							sys.exit( 19 )
						# 
						args_list.append(p_value)
					elif (p_type in OUTPUT_TYPES) or (p_type in ['D_AR']):
						args_list.append(BASE_DIR + "/" + p_value)
					else:
						args_list.append(p_value)
		else:
			print( "\nERROR: The Task " + task_name + " has not been defined in the Graph (get_execution_parameters).\n" )
			sys.exit( 22 )

		return(args_list)

	#############################################################################################################
	# Verify Output of an Task
	def verifyTaskOutput( self, task_name ):
		if task_name in list(self.workflow):
			param_types = self.workflow.node[ task_name ]['param_types']
			param_values = self.workflow.node[ task_name ]['param_values']
			for p_name, p_type in param_types.items():
				if p_type in OUTPUT_TYPES:
					# Validate existence of the parameter and its value
					if not (p_name in param_values.keys()):
						print( "\nERROR: The parameter " + p_name + " has not been defined for Task " + task_name + ".\n" )
						sys.exit( 20 )
					if param_values[ p_name ] is None:
						print( "\nERROR: The parameter " + p_name + " has no assigned value for Task " + task_name + ".\n" )
						sys.exit( 21)

					p_value_list = param_values[ p_name ]
					for p_value in p_value_list:
						complete_value = BASE_DIR + "/" + p_value
						# Directory
						if p_type in ['O_D_JPG', 'O_D_TXT', 'O_D_TSV']:
							ext = p_type.split('_')[-1]
							if not( verify_dir_ext( complete_value, ext ) ):
								print( "\nERROR: Verification of " + task_name + ". Output directory " + p_value + " does not exist or does not contain " + ext + " files.\n" )
								sys.exit( 22 )
						# File
						elif p_type in ['O_TXT', 'O_JPG']:
							ext = p_type.split('_')[-1]
							if not( verify_file_ext( complete_value, ext ) ):
								print( "\nERROR: Verification of " + task_name + ". Output file " + p_value + " does not exist or does not have " + ext + " extension.\n" )
								sys.exit( 23 )
						# Directory of Accepted and Rejected values
						elif p_type in ['O_D_AR']:
							accepted_dir = complete_value + "/accepted"
							verify_dir( accepted_dir, "The output accepted directory was not found (" + accepted_dir + ")", None, 24 )
							rejected_dir = complete_value + "/rejected"
							verify_dir( accepted_dir, "The output accepted directory was not found (" + accepted_dir + ")", None, 25 )
							accepted_file = accepted_dir + "/accepted.tsv"
							verify_file( accepted_file, "The output accepted file was not found (" + accepted_file + ")", None, 26 )
							rejected_file = rejected_dir + "/rejected.txt"
							verify_file( rejected_file, "The output rejected file was not found (" + rejected_file + ")", None, 27 )
		else:
			print( "\nERROR: The Task " + task_name + " has not been defined in the Graph (verifyTaskOutput).\n" )
			sys.exit( 28 )

		return True

	######################################################################################################################################
	# 
	def updateGraphAfterExecution( self, executed_task ):
		if executed_task in list(self.workflow):
			self.workflow.node[ executed_task ][ 'executed' ] = True
			# For all the successors of the executed task, we check if they can be now executed
			for successor_task in self.workflow.successors( executed_task ):
				prereq_done = True
				for predecessor_task in self.workflow.predecessors( successor_task ):
					if not self.workflow.node[ predecessor_task ][ 'executed' ]:
						prereq_done = False
				# If all the predecessors were already executed, the task can now be executed
				if prereq_done:
					self.next_task.append( successor_task )
			# The executed task is deleted from next_task
			del self.next_task[0]
		else:
			print( "\nERROR: The Task " + executed_task + " has not been defined in the Graph (updateGraphAfterExecution).\n" )
			sys.exit( 29 )
		# When an iterative workflow is being run, the states are updated in every iteration

	######################################################################################################################################
	# Execution of the Simulation process
	def run( self ):
		# Init log
		write_log(self.log_pathfilename, "Simulation starts.", init = True)

		# Write in the log the parameters of the simulation
		self.save_basic_info()

		#*********************************************************************
		# Simulation path in case of an iterative execution
		iteration_number = 0
		iteration_subdir = "/".join(self.project_results.split('/')[-2:]) # e.g. results/recorded_by_hitl
		#*********************************************************************

		# Start To_Run Tasks
		while len(self.next_task) > 0:
			current_task = self.next_task[0]

			#*********************************************************************
			# If iterative, update paths and study simulation process
			if self.iterative and current_task == self.stop_task:
				# Starts a new iteration
				iteration_number += 1
				iteration_dir = self.project_results + "/iteration_" + str(iteration_number)
				# The new simulation directory is created
				verify_create_dir( iteration_dir, 'The directory for the new iteration (' + iteration_dir + ') could not be created (run).', None, 30 )

				# Set the state of the tasks as Not executed
				for task_name in self.workflow:
					self.workflow.node[ task_name ][ 'executed' ] = False

				new_iteration_subdir = ""
				if iteration_number == 1:
					new_iteration_subdir = iteration_subdir + "/iteration_1"
				else:
					new_iteration_subdir = '_'.join(iteration_subdir.split('_')[:-1]) + "_" + str(iteration_number)

				# The directory values of the parameters are updated accordingly
				for task_name in self.workflow:
					for para_name in self.workflow.node[ task_name ]['param_values']:
						new_values_list = []
						# Every value is a list (hence, we treat each possible value)
						value_list = self.workflow.node[ task_name ]['param_values'][ para_name ]
						for para_value in value_list:
							new_values_list += [ str(para_value).replace( iteration_subdir, new_iteration_subdir ) ]
						#
						self.workflow.node[ task_name ]['param_values'][ para_name ] = new_values_list

				iteration_subdir = new_iteration_subdir

				# A new iteration will start
				msg = "STARTS ITERATION " + str(iteration_number) + ":"
				write_log(self.log_pathfilename, msg)

			#*********************************************************************

			# Verify the required parameters and data sources of current_task
			execution_parameters = self.get_execution_parameters( current_task )

			# Run the Task
			script_filename = self.workflow.node[ current_task ]['script']
			cmd = [script_filename] + execution_parameters
			output = subprocess.run(args=cmd)

			if output.returncode == 0: # Success
				msg = "Task " + current_task + " was successfully executed."
				write_log(self.log_pathfilename, msg)
			else: # Error or Stop iterative execution
				#*********************************************************************
				# Stop the iterative execution
				if self.iterative and (self.stop_task == current_task):
					# Finish log
					write_log(self.log_pathfilename, "Simulation finishes.")
					return(0)
				#*********************************************************************
				# Error
				else:
					msg = "ERROR: Task " + current_task + " generated an error:\n"
					msg += "\t" + str(output.stderr) + "\n"
					write_log(self.log_pathfilename, msg)
					sys.exit(output.returncode)

			# Verify the output data sources generated by the current task
			if (not self.iterative) and self.verifyTaskOutput( current_task ):
				write_log(self.log_pathfilename, "The output of the " + current_task  + " Task has been successfully verified.")

			# Update self.next_task
			self.updateGraphAfterExecution( current_task )

			#*********************************************************************
			# Verify if a new iteration must be started (If iterative)
			if self.iterative and (len(self.next_task) == 0):
				# Run the metrics scripts
				self.run_scripts('metrics', iteration_number)
				# Run the post-processing scripts
				self.run_scripts('post-processing', iteration_number)
				# Ends the iteration
				msg = "ENDS ITERATION " + str(iteration_number) + ".\n"
				write_log(self.log_pathfilename, msg)
				# We set the next task for the new iteration (The task that select the subset)
				self.next_task.append( self.stop_task )
			#*********************************************************************				

		################################################################
		# Run the metrics scripts
		if not self.iterative:
			self.run_scripts('metrics')
			# Run the post-processing scripts
			self.run_scripts('post-processing')

		# Finish log
		write_log(self.log_pathfilename, "Simulation finishes.")

	######################################################################################################################################
	# Execute the metrics and post-processing scripts
	def run_scripts(self, section_name, iteration_number = 0):
		if not (section_name in ["metrics", "post-processing"]):
			print( "\nERROR: Unknown section name (" + section_name + ").\n" )
			sys.exit(30)

		# Directory where the scripts to be executed must be located
		scripts_dir = BASE_DIR + "/humain/" + section_name + "/"

		# If it is an iterative execution
		original_subdir = ""
		iteration_subdir = ""
		if iteration_number > 0:
			original_subdir = "/".join(self.project_results.split('/')[-2:]) # e.g. results/recorded_by_hitl
			iteration_subdir = original_subdir + "/iteration_" + str(iteration_number)

		# Create element tree object and get the root
		root = ET.parse( self.params_pathfilename ).getroot()
		# Process every task
		for script in root.findall( section_name + '/script'):
			script_name = script.get('name')
			# Verify the existence of the script
			script_filename = scripts_dir + script_name
			verify_file( script_filename, "The script " + script_filename + " was not found.", None, 31 )

			parameters_list = []
			# Create the list of parameters for the script
			for parameter in script.findall( 'parameter'):
				para_text = parameter.text
				if iteration_number > 0:
					para_text = para_text.replace(original_subdir,iteration_subdir)
				parameters_list.append( "--" + parameter.get('name') )
				parameters_list.append( BASE_DIR + "/" + para_text )

			# Execution of the script
			cmd = [script_filename] + parameters_list
			output = subprocess.run(args=cmd)

			if output.returncode == 0: # Success
				msg = "The script " + script_filename + " was sucessfully executed."
				write_log(self.log_pathfilename, msg)
			else: # Error
				msg = "The script " + script_filename + " generated an execution error:\n"
				msg += "\t" + str(output.stderr) + "\n"
				write_log(self.log_pathfilename, msg)
				sys.exit(32)

	######################################################################################################################################
	# Save in the log file the project, workflow, and simulation parameters file used in the simulation
	def save_basic_info(self):
		basic_info = "Simulation Parameters:\n\t\tProject Directory: " + self.project_dir + "\n\t\tWorkflow Definition File: " + self.workflow_pathfilename
		basic_info += "\n\t\tSimulation Parameters File: " + self.params_pathfilename
		basic_info += "\n\t\tParameters per Task:\n"

		# Collect the information, one by one, of the tasks and their parameters:		
		for task_name in list(self.workflow):
			param_values = self.workflow.node[ task_name ]['param_values']
			basic_info += "\t\t\t" + task_name + ": " + str(param_values) + "\n"

		# Write in the log
		write_log(self.log_pathfilename, basic_info)
