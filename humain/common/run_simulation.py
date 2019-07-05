#!/usr/bin/env python3
import sys, argparse

from simulation import *


if __name__ == '__main__':
	""" Runs the workflow's execution definition, validating I/O, and logging the progress events.
	"""
	parser = argparse.ArgumentParser("Runs the workflow's execution definition, validating I/O, and logging the progress events.")
	parser.add_argument('-p', '--project', action="store", required=True, help="Project name (directory name of the project).")
	parser.add_argument('-w', '--workflow', action="store", required=True, help="Workflow name (name of the workflow file) without .csv.")
	parser.add_argument('-s', '--sim_params', action="store", required=True, help="Name of the file with the parameters for the simulation (do not require the .csv extension)")
	args = parser.parse_args()

	# Usage example
	# python3 simulate.py -p selfie -w event_date -s event_date_001

	sim = Simulation( args.project, args.workflow, args.sim_params )
	sim.run()