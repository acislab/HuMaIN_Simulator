#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	File runs the simulation set (when the given simulation file has been 
#               generated from a prevously exisiting simulation
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


import sys, argparse

from humain.simulation import *


if __name__ == '__main__':
	""" Runs the workflow's execution definition, validating I/O, and logging the progress events.
	"""
	parser = argparse.ArgumentParser("Runs the workflow's execution definition, validating I/O, and logging the progress events.")
	parser.add_argument('-p', '--project', action="store", required=True, help="Project name (directory name of the project).")
	parser.add_argument('-w', '--workflow', action="store", required=True, help="Workflow name (name of the workflow file) without .csv.")
	parser.add_argument('-s', '--sim_params', action="store", required=True, help="Name of the file with the parameters for the simulation (do not require the .csv extension)")
	args = parser.parse_args()

	# Usage example
	# python3 run_simulation.py -p selfie -w event_date -s event_date_001
	
	sim = Simulation( args.project, args.workflow, args.sim_params )
	#sim.draw_workflow()
	
	sim.run()
