#!/usr/bin/env python3
import argparse

from humain.common.constants import *
from humain.common.utils import *

if __name__ == '__main__':
	""" Runs the workflow's execution definition, validating I/O, and logging the progress events.
	"""
	parser = argparse.ArgumentParser("Runs the workflow's execution definition, validating I/O, and logging the progress events.")
	parser.add_argument('-p', '--project', action="store", required=True, help="Project name (directory name of the project).")
	parser.add_argument('-w', '--workflow', action="store", required=True, help="Workflow name (name of the workflow file) without .csv.")
	parser.add_argument('-e', '--execution', action="store", required=True, help="Execution name (do not include the .csv extension)")
	args = parser.parse_args()

	# Usage example
	# python3 simulate.py -p selfie -w event_date -e event_date_001

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
    
	# args.project
	project_dir = PROJECTS_DIR + "/" + args.project
	verify_dir( project_dir, 'The project directory (' + project_dir + ') was not found: ', parser, 1 )

	# args.workflow
	workflow_dir = project_dir + "/workflows"
	verify_dir( workflow_dir, 'The workflows directory (' + workflow_dir + ') was not found: ', parser, 2 )
	workflow_filename = workflow_dir + "/" + args.workflow.replace('.csv', '') + ".csv"
	verify_file( workflow_filename, 'The workflow file (' + workflow_filename + ') was not found.', parser, 3 )

	# args.execution
	execution_dir = project_dir + "/executions"
	verify_dir( execution_dir, 'The execution directory (' + execution_dir + ') was not found: ', parser, 4 )
	execution_filename = execution_dir + "/" + args.execution.replace('.csv', '') + ".csv"
	verify_file( execution_filename, 'The execution file (' + execution_filename + ') was not found.', parser, 5 )


	print("Hello")
	
