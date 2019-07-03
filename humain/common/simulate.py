#!/usr/bin/env python3
import argparse, networkx as nx

from humain.common.constants import *
from humain.common.utils import *
import matplotlib.pyplot as plt

class Workflow:
	'Sequence of actions to execute'

	# Constructor
	def __init__(self, prj_name, wfw_name):
		# Project's Directory
		self.project_dir = PROJECTS_DIR + "/" + prj_name
		verify_dir( self.project_dir, 'The project directory (' + self.project_dir + ') was not found: ', None, 1 )

		# Workflows Directory 
		self.workflows_dir = self.project_dir + "/workflows" 
		verify_dir( self.workflows_dir, 'The workflows directory (' + self.workflows_dir + ') was not found: ', None, 2 )

		# Workflow Definition File
		self.workflow_pathfilename = self.workflows_dir + "/" + wfw_name.replace('.csv', '') + ".csv"
		verify_file( self.workflow_pathfilename, 'The workflow file (' + self.workflow_pathfilename + ') was not found.', None, 3 )

		# Digraph with the structure of actions to run
		self.workflow = nx.DiGraph()

		# Action(s) to be executed next
		self.next_action = []

	# Load the nodes (actions) and structure of the IE workflow
	def load_structure(self):
		with open( self.workflow_pathfilename, "r+" ) as wf:
			for line in wf:
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

		# Need to create a layout when doing
		# separate calls to draw nodes and edges
		pos = nx.spring_layout(G)
		nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
							node_color = values, node_size = 500)
		nx.draw_networkx_labels(G, pos)
		nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
		nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
		plt.show()

		
class Simulation:
	'Workflow and the simulation parameters'

	def __init__(self, proj_name, wfw_name, sim_param):
		# Workflow Structure: Sequence of Actions
		self.workflow = Workflow( proj_name, wfw_name )

		# Simulations Directory
		self.simulations_dir = PROJECTS_DIR + "/" + proj_name + "/simulations"
		verify_dir( self.simulations_dir, 'The simulations directory (' + self.simulations_dir + ') was not found: ', None, 4 )

		# File with the simulation parameters of the workflow
		self.params_pathfilename = self.simulations_dir + "/" + sim_param.replace('.csv', '') + ".csv"
		verify_file( self.params_pathfilename, 'The simulation parameters file (' + self.params_pathfilename + ') was not found.', None, 5 )

		# Load the structure of the workflow
		self.workflow.load_structure()



if __name__ == '__main__':
	""" Runs the workflow's execution definition, validating I/O, and logging the progress events.
	"""
	parser = argparse.ArgumentParser("Runs the workflow's execution definition, validating I/O, and logging the progress events.")
	parser.add_argument('-p', '--project', action="store", required=True, help="Project name (directory name of the project).")
	parser.add_argument('-w', '--workflow', action="store", required=True, help="Workflow name (name of the workflow file) without .csv.")
	parser.add_argument('-s', '--simulation', action="store", required=True, help="Name of the file with the parameters for the simulation (do not require the .csv extension)")
	args = parser.parse_args()

	# Usage example
	# python3 simulate.py -p selfie -w event_date -s event_date_001

	# wfw = Workflow(args.project, args.workflow)
	sim = Simulation( args.project, args.workflow, args.simulation )

