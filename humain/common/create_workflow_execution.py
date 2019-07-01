#!/usr/bin/env python3
import argparse

from humain.common.constants import *
from humain.common.utils import *

if __name__ == '__main__':
	""" Runs the workflow's execution definition, validating I/O, and logging the progress events.
	"""
	parser = argparse.ArgumentParser("Runs the workflow's execution definition, validating I/O, and logging the progress events.")
	parser.add_argument('-p', '--project', action="store", required=True, help="Project name (directory name of the project).")
	parser.add_argument('-w', '--workflow', action="store", required=True, help="Workflow name (directory name of the workflow).")
	parser.add_argument('-e', '--execution', action="store", required=True, help="csv execution file (do not incldue the extension)")
	args = parser.parse_args()
	
	# Usage example
	python3 
