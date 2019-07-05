#!/usr/bin/env python3
import sys, networkx as nx
import matplotlib.pyplot as plt

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
		self.workflow_pathfilename = self.workflows_dir + "/" + wfw_name.replace('.csv', '') + ".csv"
		verify_file( self.workflow_pathfilename, 'The workflow file (' + self.workflow_pathfilename + ') was not found.', None, 3 )

		# Actions Directory 
		self.actions_dir = self.project_dir + "/actions" 
		verify_dir( self.actions_dir, 'The actions directory (' + self.actions_dir + ') was not found: ', None, 4 )

		# Simulations Directory
		self.simulations_dir = PROJECTS_DIR + "/" + prj_name + "/simulations"
		verify_dir( self.simulations_dir, 'The simulations directory (' + self.simulations_dir + ') was not found: ', None, 5 )

		# File with the simulation parameters of the workflow
		self.params_pathfilename = self.simulations_dir + "/" + sim_par_name.replace('.csv', '') + ".csv"
		verify_file( self.params_pathfilename, 'The simulation parameters file (' + self.params_pathfilename + ') was not found.', None, 6 )

		##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##--
		##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##-------##--

		# Workflow
		self.workflow = nx.DiGraph()

		# Action(s) to be executed next
		self.next_action = []

		# Load the structure of actions
		self.load_actions()

		# Load the parameters of every actions of the workflow
		self.load_parameters()

		# Load the values for each of the Actions' parameters
		self.load_values(self.params_pathfilename)

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
		plt.show()

	
	######################################################################################################################################
	# Load inputs and outputs of every (actions) and save them as nodes' attributes in the graph
	def load_parameters(self):
		# Load the content of the actions.csv file
		actions_csv = self.project_dir + "/actions.csv"
		verify_file( actions_csv, "The actions' description file (" + actions_csv + ") was not found.", None, 7 )

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
			verify_file( script_name, 'The Python script for the  action (' + act_name + ') was not found.', None, 8 )
			# The script is added as attribute for the node
			self.workflow.node[act_name]['script'] = script_name

			# Veryfication of the list of parameters for the Action under study
			if not(act_name in params_dict):
				print( "\nERROR: There is not definition, in Actions.csv, for the parameters of the Action " + act_name + ".\n" )
				sys.exit( 9 )
			params_list = params_dict[ act_name ]
			for parameter_string in params_list:
				param_segments = parameter_string.split(':')
				p_name, p_datatype, p_DS = "", "", ""
				if len(param_segments) == 2:
					p_name, p_datatype = param_segments[0], param_segments[1]
					if not(p_datatype in DATATYPES):
						print( "\nERROR: In definition of Action " + act_name + ", datatype " + p_datatype + " does not exist.\n" )
						sys.exit( 10 )
				elif len(param_segments) == 3:
					p_name, p_datatype, p_DS = param_segments[0], param_segments[1], param_segments[2]
					if not(p_datatype in DATATYPES):
						print( "\nERROR: In definition of Action " + act_name + ", datatype " + p_datatype + " does not exist.\n" )
						sys.exit( 10 )
					if not(p_DS in DATASET_TYPES):
						print( "\nERROR: In definition of Action " + act_name + ", dataset type " + p_datatype + " does not exist.\n" )
						sys.exit( 11 )
				else:
					print( "\nERROR: In definition of Action " + act_name + ", parameter " + p_name + " has a wrong type specification.\n" )
					sys.exit( 12 )

			# The validated list of parameters id added as an attribute to the node
			self.workflow.node[act_name]['parameters'] = params_list

	
	######################################################################################################################################
	# Load the values for each of the Actions' parameters
	def load_values(self, sim_fname):
		# Load the content of the actions.csv file
		actions_csv = self.project_dir + "/actions.csv"
		verify_file( actions_csv, "The actions' description file (" + actions_csv + ") was not found.", None, 7 )

	######################################################################################################################################
	# Execution of the Simulation process
	def run(self):
		# Init log

		# Start To_Run Actions

		# While len(To_Run) > 0:
		# 	verify_input
		# 	run
		# 	verify_output
		pass
