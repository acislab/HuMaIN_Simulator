#!/usr/bin/env python3
import sys, networkx as nx
import matplotlib.pyplot as plt
import ntpath, subprocess, re

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
		self.params_pathfilename = self.simulations_dir + "/" + ntpath.basename( sim_par_name ).replace('.csv', '') + ".csv"
		verify_file( self.params_pathfilename, 'The simulation parameters file (' + self.params_pathfilename + ') was not found.', None, 6 )

		# Results directory: self.project_results
		results_dir = self.project_dir + "/results"
		verify_create_dir( results_dir, 'The results directory (' + results_dir + ') was not found and could not be created.', None, 7 )
		self.project_results = results_dir + "/" + ntpath.basename(sim_par_name).replace('.csv', '')
		verify_create_dir( self.project_results, 'The directory to store the execution results(' + self.project_results + ') and could not be created.', None, 8 )

		# Execution Log 
		self.log_pathfilename = self.project_results + "/" + ntpath.basename( sim_par_name ) + ".log"

		##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##--
		##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##--

		# Workflow = Graph
		self.workflow = nx.DiGraph()

		# Task(s) to be executed next
		self.next_task = []

		# Load the structure of tasks
		self.load_tasks()

		# Load the parameters of every tasks of the workflow
		self.load_parameters()

		# Load the values for each of the Tasks' parameters
		self.load_values( self.params_pathfilename )

	######################################################################################################################################
	# Load the nodes (tasks) and structure of the IE workflow
	def load_tasks(self):
		with open( self.workflow_pathfilename, "r+" ) as wf:
			for line in wf:
				line = line[:-1].replace(' ', '')
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
		# Load the content of the tasks.csv file
		tasks_csv = self.project_dir + "/tasks.csv"
		verify_file( tasks_csv, "The tasks' description file (" + tasks_csv + ") was not found.", None, 9 )

		# Create a dictionary with the list of parameters for each Task
		params_dict = {}
		tasks_csv_text = ""
		with open(tasks_csv, "r+") as t_f:
			for line in t_f:
		# 		tasks_csv_text += line.replace('\n', '&&')
		# print(tasks_csv_text)
		# # The TASK section is loaded
		# task_section = re.findall(r'\[TASKS\](.+?)\[.+\]', tasks_csv_text)
		# if len(task_section) == 0:
		# 	print( "\nERROR: The TASKS section could not be read from tasks.csv.\n" )
		# 	sys.exit( 10 )
		# lines = task_section.split('&&')
		# print(lines)
		# # Each line is processed and the parameters are extracted
		# for line in lines:
				line = line[:-1].replace(' ', '')
				list_segments = line.split(',')
				if len(list_segments) > 0:
					params_dict[ list_segments[0] ] = list_segments[1:]

		# Review, one by one, of all the tasks:		
		for task_name in list(self.workflow):
			# Python script for the task
			script_name = self.tasks_dir + "/" + task_name + ".py"
			verify_file( script_name, 'The Python script for the task (' + task_name + ') was not found.', None, 10 )
			# The script is added as attribute for the node
			self.workflow.node[task_name]['script'] = script_name

			# Veryfication of the list of parameters for the Task under study
			if not(task_name in params_dict):
				print( "\nERROR: There is not definition, in tasks.csv, for the parameters of the Task " + task_name + ".\n" )
				sys.exit( 11 )

			# Dictionaries of (parameter, datatype) and (parameter, value) pairs
			param_datatype_dict = {}
			param_value_dict = {}
			# Processing of each of the parameters
			params_line = params_dict[ task_name ]
			for parameter_definition in params_line:
				p_name, p_datatype = "", ""

				param_parts = parameter_definition.split(':')
				if len(param_parts) == 2:
					p_name, p_datatype = param_parts[0], param_parts[1]
					if not(p_datatype in DATATYPES):
						print( "\nERROR: In definition of Task " + task_name + ", datatype " + p_datatype + " does not exist.\n" )
						sys.exit( 12 )
					# We save the datatype, but we do not know yet the value
					param_datatype_dict[ p_name ] = p_datatype
					param_value_dict[ p_name ] = None

				else:
					print( "\nERROR: In definition of Task " + task_name + ", parameter " + p_name + " has a wrong type specification.\n" )
					sys.exit( 13 )

			# The validated list of parameters is added as an attribute to the node
			self.workflow.node[task_name]['param_types'] = param_datatype_dict
			self.workflow.node[task_name]['param_values'] = param_value_dict
	
	######################################################################################################################################
	# Load the values for each of the Tasks' parameters
	def load_values(self, sim_fname):
		# Create a dictionary with the list of parameters for each Task
		params_dict = {}
		with open(self.params_pathfilename, "r+") as par_f:
			for line in par_f:
				line = line[:-1].replace(' ', '')
				list_segments = line.split(',')
				if len(list_segments) > 0:
					params_dict[ list_segments[0] ] = list_segments[1:]
		
		# Process, one by one, the tasks and their parameters:		
		for task_name in list(self.workflow):
			# Veryfication of the list of parameters for the Task under study
			if not(task_name in params_dict):
				print( "\nERROR: There is not definition, in " + self.params_pathfilename + ", for the parameters of the Task " + task_name + ".\n" )
				sys.exit( 14 )

			# Processing of each of the parameters
			params_line = params_dict[ task_name ]
			for parameter_definition in params_line:
				p_name, p_value = "", ""
				param_parts = parameter_definition.split('=')
				if len(param_parts) == 2:
					p_name, p_value = param_parts[0], param_parts[1]
					if not( p_name in self.workflow.node[task_name]['param_values'] ):
						print( "\nERROR: Parameter " + p_name + " has not been defined in Task " + task_name + ".\n" )
						sys.exit( 15 )
					# We assign the value to the parameter
					self.workflow.node[task_name]['param_values'][ p_name ] = p_value
				else:
					print( "\nERROR: In definition of Task " + task_name + ", parameter " + p_name + " has a wrong type specification.\n" )
					sys.exit( 16 )

	######################################################################################################################################
	# Returns the parameters to run the especified Task
	def get_execution_parameters(self, task_name ):
		args_list = []
		if task_name in list(self.workflow):
			param_types = self.workflow.node[task_name]['param_types']
			param_values = self.workflow.node[task_name]['param_values']
			for p_name, p_type in param_types.items():
				# Validate existence of the parameter and its value
				if not (p_name in param_values.keys()):
					print( "\nERROR: The parameter " + p_name + " has not been defined for Task " + task_name + ".\n" )
					sys.exit( 17 )
				if param_values[ p_name ] is None:
					print( "\nERROR: The parameter " + p_name + " has no assigned value for Task " + task_name + ".\n" )
					sys.exit( 18 )

				p_value = param_values[ p_name ]
				args_list.append("--" + p_name)

				# Directory
				if p_type in ['D_JPG', 'D_TXT']:
					dir_name = BASE_DIR + "/" + p_value
					ext = p_type.split('_')[-1]
					if not( verify_dir_ext( dir_name, ext ) ):
						print( "\nERROR: Execution of " + task_name + ". Directory " + dir_name + " does not exist or does not contain " + ext + " files.\n" )
						sys.exit( 19 )
					#
					args_list.append(dir_name)
				# File
				elif p_type in ['TXT', 'JPG', 'TSV']:
					filename = BASE_DIR + "/" + p_value
					ext = p_type.split('_')[-1]
					if not( verify_file_ext( filename, ext ) ):
						print( "\nERROR: Execution of " + task_name + ". File " + filename + " does not exist or does not have " + ext + " extension.\n" )
						sys.exit( 20 )
					# 
					args_list.append(filename)
				elif p_type in ['INT', 'FLOAT']:
					if not (p_value.replace('.','',1).isdigit()):
						print( "\nERROR: Execution of " + task_name + ". " + p_name + "'s value is not numeric: " + str(p_value) + ".\n" )
						sys.exit( 21 )
					# 
					args_list.append(p_value)
				elif p_type in OUTPUT_TYPES:
					# It is a file or a directory
					args_list.append(BASE_DIR + "/" + p_value)
				else:
					args_list.append(p_value)
		else:
			print( "\nERROR: The Task " + task_name + " has not been defined in the Graph.\n" )
			sys.exit( 22 )

		return(args_list)

	#############################################################################################################
	# Verify Output of an Task
	def verifyTaskOutput( self, task_name ):
		if task_name in list(self.workflow):
			param_types = self.workflow.node[task_name]['param_types']
			param_values = self.workflow.node[task_name]['param_values']
			for p_name, p_type in param_types.items():
				if p_type in OUTPUT_TYPES:
					# Validate existence of the parameter and its value
					if not (p_name in param_values.keys()):
						print( "\nERROR: The parameter " + p_name + " has not been defined for Task " + task_name + ".\n" )
						sys.exit( 23 )
					if param_values[ p_name ] is None:
						print( "\nERROR: The parameter " + p_name + " has no assigned value for Task " + task_name + ".\n" )
						sys.exit( 24)

					p_value = param_values[ p_name ]
					complete_value = BASE_DIR + "/" + p_value

					# Directory
					if p_type in ['O_D_JPG', 'O_D_TXT']:
						ext = p_type.split('_')[-1]
						if not( verify_dir_ext( complete_value, ext ) ):
							print( "\nERROR: Verification of " + task_name + ". Output directory " + p_value + " does not exist or does not contain " + ext + " files.\n" )
							sys.exit( 25 )
					# File
					elif p_type in ['O_TXT', 'O_JPG']:
						ext = p_type.split('_')[-1]
						if not( verify_file_ext( complete_value, ext ) ):
							print( "\nERROR: Verification of " + task_name + ". Output file " + p_value + " does not exist or does not have " + ext + " extension.\n" )
							sys.exit( 26 )
					# Directory of Accepted and Rejected values
					elif p_type in ['O_D_AR']:
						accepted_dir = complete_value + "/accepted"
						verify_dir( accepted_dir, "The output accepted directory was not found (" + accepted_dir + ")", None, 27 )
						rejected_dir = complete_value + "/rejected"
						verify_dir( accepted_dir, "The output accepted directory was not found (" + accepted_dir + ")", None, 28 )
						accepted_file = accepted_dir + "/accepted.tsv"
						verify_file( accepted_file, "The output accepted file was not found (" + accepted_file + ")", None, 29 )
						rejected_file = rejected_dir + "/rejected.tsv"
						verify_file( rejected_file, "The output rejected file was not found (" + rejected_file + ")", None, 30 )
		else:
			print( "\nERROR: The Task " + task_name + " has not been defined in the Graph.\n" )
			sys.exit( 27 )

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
			print( "\nERROR: The Task " + executed_task + " has not been defined in the Graph.\n" )
			sys.exit( 28 )

	######################################################################################################################################
	# Execution of the Simulation process
	def run( self ):
		# Init log
		write_log(self.log_pathfilename, "Simulation starts.", init = True)

		# Write in the log the parameters of the simulation
		self.save_basic_info()

		# Start To_Run Tasks (TODO: This can be parallelized)
		while len(self.next_task) > 0:
			current_task = self.next_task[0]
			# Verify the required parameters and data sources of current_task
			execution_parameters = self.get_execution_parameters( current_task )
			# Run the Task
			script_filename = self.workflow.node[ current_task ]['script']
			cmd = [script_filename] + execution_parameters
			output = subprocess.run(args=cmd)

			if output.returncode == 0: # Success
				msg = "Task " + current_task + " was sucessfully executed."
				write_log(self.log_pathfilename, msg)
			else: # Error
				msg = "ERROR: Task " + current_task + " generated an error:\n"
				msg += "\t" + str(output.stderr) + "\n"
				write_log(self.log_pathfilename, msg)
				sys.exit(output.returncode)

			# Verify the output data sources generated by the current task
			if self.verifyTaskOutput( current_task ):
				write_log(self.log_pathfilename, "The output of the " + current_task  + " Task has been successfully verified.")

			# Update self.next_task
			self.updateGraphAfterExecution( current_task )

		# Run the metrics scripts
		self.run_scripts('[METRICS]')
		# Run the post-processing scripts
		#self.run_scripts('[POST-PROCESSING]')

		# Finish log
		write_log(self.log_pathfilename, "Simulation finishes.")

	######################################################################################################################################
	# Execute the metrics and post-processing scripts
	def run_scripts(self, section_name):
		if not (section_name in ["[METRICS]", "[POST-PROCESSING]"]):
			print( "\nERROR: Unknown section name (" + section_name + ").\n" )
			sys.exit(31)

		scripts_list_text = read_section_lines( self.params_pathfilename, section_name )
		for line in scripts_list_text.split('\n'):
			script_name = ""
			parameters_list = []
			line = line.replace(' ', '')
			if line == "": 
				continue

			# Get the Execution parameters
			parameters = line.split(',')
			if len(parameters) > 1:
				# Verify the existence of the metric script
				script_name = self.tasks_dir + "/metrics/" + parameters[0]
				verify_file( script_name, "The metric script " + script_name + " was not found.", None, 32 )
				i = 1
				while (i < len(parameters)):
					param_name, value = None, None
					try:
						param_name, value = parameters[i].split('=')
						parameters_list.append( "--" + param_name )
						parameters_list.append( BASE_DIR + "/" + value )
					except ValueError:
						print( "\nERROR: Script " + script_name + ". The parameter does not have the right syntax.\n" )
						sys.exit(31)
					i = i + 1
					
			# Execution of the script
			cmd = [script_name] + parameters_list
			output = subprocess.run(args=cmd)

			if output.returncode == 0: # Success
				msg = "Metric Script: " + script_name + ". The script was sucessfully executed."
				write_log(self.log_pathfilename, msg)
			else: # Error
				msg = "ERROR: The " + script_name + " metric script generated an execution error:\n"
				msg += "\t" + str(output.stderr) + "\n"
				write_log(self.log_pathfilename, msg)
				sys.exit(33)

	######################################################################################################################################
	# Save in the log file the project, workflow, and simulation parameters file used in the simulation
	def save_basic_info(self):
		basic_info = "Simulation Parameters:\n\t\tProject Directory: " + self.project_dir + "\n\t\tWorkflow Definition File: " + self.workflow_pathfilename
		basic_info += "\n\t\tSimulation Parameters File: " + self.params_pathfilename
		basic_info += "\n\t\tParameters per Task:\n"

		# Collect the information, one by one, of the tasks and their parameters:		
		for task_name in list(self.workflow):
			param_values = self.workflow.node[task_name]['param_values']
			basic_info += "\t\t\t" + task_name + ": " + str(param_values) + "\n"

		# Write in the log
		write_log(self.log_pathfilename, basic_info)
