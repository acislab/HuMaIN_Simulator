#!/usr/bin/env python3
import sys, networkx as nx
import matplotlib.pyplot as plt
import ntpath, subprocess

from constants import *
from utils import *



class Simulation:
	'Sequence of actions to execute'
	######################################################################################################################################
	# Constructor
	def __init__(self, prj_name, wfw_name, sim_par_name):
		##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##--
		# Project's Directory
		self.project_dir = PROJECTS_DIR + "/" + prj_name
		verify_dir( self.project_dir, 'The project directory (' + self.project_dir + ') was not found: ', None, 1 )

		# Workflows Directory 
		self.workflows_dir = self.project_dir + "/workflows" 
		verify_dir( self.workflows_dir, 'The workflows directory (' + self.workflows_dir + ') was not found: ', None, 2 )

		# Workflow Definition File
		self.workflow_pathfilename = self.workflows_dir + "/" + ntpath.basename( wfw_name ).replace('.csv', '') + ".csv"
		verify_file( self.workflow_pathfilename, 'The workflow file (' + self.workflow_pathfilename + ') was not found.', None, 3 )

		# Actions Directory 
		self.actions_dir = self.project_dir + "/actions" 
		verify_dir( self.actions_dir, 'The actions directory (' + self.actions_dir + ') was not found: ', None, 4 )

		# Simulations Directory
		self.simulations_dir = PROJECTS_DIR + "/" + prj_name + "/simulations"
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

		# Action(s) to be executed next
		self.next_action = []

		# Load the structure of actions
		self.load_actions()

		# Load the parameters of every actions of the workflow
		self.load_parameters()

		# Load the values for each of the Actions' parameters
		self.load_values( self.params_pathfilename )

	######################################################################################################################################
	# Load the nodes (actions) and structure of the IE workflow
	def load_actions(self):
		with open( self.workflow_pathfilename, "r+" ) as wf:
			for line in wf:
				line = line[:-1].replace(' ', '')
				actions = line.split(',')
				n_a = len(actions)
				if n_a == 1:
					self.next_action.append( actions[0] )
					self.workflow.add_node( actions[0], run = False )
				elif n_a > 1:
					if (not (actions[0] in self.workflow)):
						self.workflow.add_node( actions[0], run = False )
					i = 1
					while (i < n_a):
						if (not (actions[i] in self.workflow)):
							self.workflow.add_node( actions[i], run = False )
						self.workflow.add_edge( actions[i], actions[0] )
						i = i + 1
	
	######################################################################################################################################
	# Draw the graph of actions and the order of execution
	def draw_workflow(self):
		pos = nx.circular_layout(self.workflow)    
		nx.draw(self.workflow, pos, with_labels = True, edge_color = 'b')  
		#node_labels = nx.get_node_attributes(self.workflow, 'param_types')
		node_labels = nx.get_node_attributes(self.workflow, 'param_values')
		nx.draw_networkx_labels(self.workflow, pos, labels = node_labels)
		plt.show()
	
	######################################################################################################################################
	# Load inputs and outputs of every (actions) and save them as nodes' attributes in the graph
	def load_parameters(self):
		# Load the content of the actions.csv file
		actions_csv = self.project_dir + "/actions.csv"
		verify_file( actions_csv, "The actions' description file (" + actions_csv + ") was not found.", None, 9 )

		# Create a dictionary with the list of parameters for each Action
		params_dict = {}
		with open(actions_csv, "r+") as act_f:
			for line in act_f:
				line = line[:-1].replace(' ', '')
				list_segments = line.split(',')
				if len(list_segments) > 0:
					params_dict[ list_segments[0] ] = list_segments[1:]

		# Review, one by one, of all the actions:		
		for act_name in list(self.workflow):
			# Python script for the action
			script_name = self.actions_dir + "/" + act_name + ".py"
			verify_file( script_name, 'The Python script for the  action (' + act_name + ') was not found.', None, 10 )
			# The script is added as attribute for the node
			self.workflow.node[act_name]['script'] = script_name

			# Veryfication of the list of parameters for the Action under study
			if not(act_name in params_dict):
				print( "\nERROR: There is not definition, in Actions.csv, for the parameters of the Action " + act_name + ".\n" )
				sys.exit( 11 )

			# Dictionaries of (parameter, datatype) and (parameter, value) pairs
			param_datatype_dict = {}
			param_value_dict = {}
			# Processing of each of the parameters
			params_line = params_dict[ act_name ]
			for parameter_definition in params_line:
				p_name, p_datatype = "", ""

				param_parts = parameter_definition.split(':')
				if len(param_parts) == 2:
					p_name, p_datatype = param_parts[0], param_parts[1]
					if not(p_datatype in DATATYPES):
						print( "\nERROR: In definition of Action " + act_name + ", datatype " + p_datatype + " does not exist.\n" )
						sys.exit( 12 )
					# We save the datatype, but we do not know yet the value
					param_datatype_dict[ p_name ] = p_datatype
					param_value_dict[ p_name ] = None

				else:
					print( "\nERROR: In definition of Action " + act_name + ", parameter " + p_name + " has a wrong type specification.\n" )
					sys.exit( 13 )

			# The validated list of parameters is added as an attribute to the node
			self.workflow.node[act_name]['param_types'] = param_datatype_dict
			self.workflow.node[act_name]['param_values'] = param_value_dict

			#self.draw_workflow()
			break

	
	######################################################################################################################################
	# Load the values for each of the Actions' parameters
	def load_values(self, sim_fname):
		# Create a dictionary with the list of parameters for each Action
		params_dict = {}
		with open(self.params_pathfilename, "r+") as par_f:
			for line in par_f:
				line = line[:-1].replace(' ', '')
				list_segments = line.split(',')
				if len(list_segments) > 0:
					params_dict[ list_segments[0] ] = list_segments[1:]
		
		# Process, one by one, the actions and their parameters:		
		for act_name in list(self.workflow):
			# Veryfication of the list of parameters for the Action under study
			if not(act_name in params_dict):
				print( "\nERROR: There is not definition, in " + self.params_pathfilename + ", for the parameters of the Action " + act_name + ".\n" )
				sys.exit( 14 )

			# Processing of each of the parameters
			params_line = params_dict[ act_name ]
			for parameter_definition in params_line:
				p_name, p_value = "", ""
				param_parts = parameter_definition.split('=')
				if len(param_parts) == 2:
					p_name, p_value = param_parts[0], param_parts[1]
					if not( p_name in self.workflow.node[act_name]['param_values'] ):
						print( "\nERROR: Parameter " + p_name + " has not been defined in Action " + act_name + ".\n" )
						sys.exit( 15 )
					# We assign the value to the parameter
					self.workflow.node[act_name]['param_values'][ p_name ] = p_value
				else:
					print( "\nERROR: In definition of Action " + act_name + ", parameter " + p_name + " has a wrong type specification.\n" )
					sys.exit( 16 )

			break

	######################################################################################################################################
	# Returns the parameters to run the especified Action
	def get_execution_parameters(self, act_name ):
		args_list = []
		if act_name in list(self.workflow):
			param_types = self.workflow.node[act_name]['param_types']
			param_values = self.workflow.node[act_name]['param_values']
			for p_name, p_type in param_types.items():
				# Validate existence of the parameter and its value
				if not (p_name in param_values.keys()):
					print( "\nERROR: The parameter " + p_name + " has not been defined for Action " + act_name + ".\n" )
					sys.exit( 17 )
				if param_values[ p_name ] is None:
					print( "\nERROR: The parameter " + p_name + " has no assigned value for Action " + act_name + ".\n" )
					sys.exit( 18 )

				p_value = param_values[ p_name ]
				args_list.append("--" + p_name)

				# Directory
				if p_type in ['D_JPG', 'D_TXT']:
					dir_name = BASE_DIR + "/" + p_value
					ext = p_type.split('_')[-1]
					if not( verify_dir_ext( dir_name, ext ) ):
						print( "\nERROR: Execution of " + act_name + ". Directory " + p_value + " does not exist or does not contain " + ext + " files.\n" )
						sys.exit( 19 )
					#
					args_list.append(dir_name)
				# File
				elif p_type in ['TXT', 'JPG']:
					filename = BASE_DIR + "/" + p_value
					ext = p_type.split('_')[-1]
					if not( verify_file_ext( filename, ext ) ):
						print( "\nERROR: Execution of " + act_name + ". File " + p_value + " does not exist or does not have " + ext + " extension.\n" )
						sys.exit( 20 )
					# 
					args_list.append(filename)
				elif p_type in ['INT', 'FLOAT']:
					if not (p_value.replace('.','',1).isdigit()):
						print( "\nERROR: Execution of " + act_name + ". " + p_name + "'s value is not numeric: " + str(p_value) + ".\n" )
						sys.exit( 21 )
					# 
					args_list.append(p_value)
				elif p_type in OUTPUT_TYPES:
					# It is a file or a directory
					
					args_list.append(BASE_DIR + "/" + p_value)
				else:
					args_list.append(p_value)
		else:
			print( "\nERROR: The Action " + act_name + " has not been defined in the Graph.\n" )
			sys.exit( 22 )

		return(args_list)


	######################################################################################################################################
	# Execution of the Simulation process
	def run(self):
		# Init log
		write_log(self.log_pathfilename, "Simulation starts.", init = True)

		# Write in the log the parameters of the simulation
		self.save_basic_info()

		# Start To_Run Actions (TODO: This can be parallelized)
		while len(self.next_action) > 0:
			current_action = self.next_action[0]
			# Verify the required parameters and data sources of current_action
			execution_parameters = self.get_execution_parameters( current_action )
			# Run the Action
			script_filename = self.workflow.node[ current_action ]['script']
			cmd = [script_filename] + execution_parameters
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
			# out, err = p.communicate() 
			# result = out.split('\n')
			# for lin in result:
			# 	print(lin)

			# Verify the output data sources generated by the current action

			# Update self.next_action
			break

		# Run the metrics scripts


		# Finish log
		write_log(self.log_pathfilename, "Simulation finishes.")

	######################################################################################################################################
	# Save in the log file the project, workflow, and simulation parameters file used in the simulation
	def save_basic_info(self):
		basic_info = "Simulation Parameters:\n\t\tProject Directory: " + self.project_dir + "\n\t\tWorkflow Definition File: " + self.workflow_pathfilename
		basic_info += "\n\t\tSimulation Parameters File: " + self.params_pathfilename
		basic_info += "\n\t\tParameters per Action: "

		# Collect the information, one by one, of the actions and their parameters:		
		for act_name in list(self.workflow):
			param_values = self.workflow.node[act_name]['param_values']
			basic_info += "\n\t\t\t" + act_name + ": " + str(param_values) + "\n"

			break
		# Write in the log
		write_log(self.log_pathfilename, basic_info)
