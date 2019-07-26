#!/usr/bin/env python3

##########################################################################################
# Developers: 	Aditi Malladi and Icaro Alzuru
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Create the structure of directories for a project, empty or copying the 
# 				files from an existing project.
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

import argparse, csv

from humain.constants import *
from humain.utils import *


# Create files inside "path" folder
def create_file(path, filename):
    open(os.path.join(path, filename), 'wb')
    

# Create a new Project
def create_project_structure(dirname, project):
    try:
        os.mkdir(dirname)
        os.mkdir(dirname+"/tasks")
        os.mkdir(dirname+"/workflows")
        os.mkdir(dirname+"/simulations")
        os.mkdir(dirname+"/results")
        create_file(dirname, "tasks.csv")
        create_file(dirname, "__init__.py")
        create_file(dirname+"/tasks", "__init__.py")
    except FileExistsError:
        print("\nERROR: Project", project, "already exists! Try a different Project Name!\n")


if __name__ == '__main__':
	""" Creates a new Simulation directory and its internal structure. Empty or from an existing project.
	"""
	parser = argparse.ArgumentParser("Creates a new Simulation directory and its internal structure. Empty or from an existing project.")
	parser.add_argument('-n', '--project', action="store", required=True, help="New project's name")
	parser.add_argument('-c', '--copy', action="store", required=False, help="Copy from existing project")
	args = parser.parse_args()
	# usage: python3 common/create_project.py --project test

	dirname = BASE_DIR + "/" + args.project

	if args.copy is not None:
		try: 
			print("Copying from ", args.copy)
			dircopy = BASE_DIR + "/" + args.copy
			if os.path.isdir(dircopy): 
				copy_anything(dircopy, dirname)
				# Remove the Result files
				result_folder = dirname + "/results"
				delete_files_folders(result_folder)
			else: 
				print("\nERROR: Folder", args.copy, "does not exist!\n")
		except FileExistsError:
			print("\nERROR: Project" , args.project,  "already exists! Try a different name!\n")
	else:
	    create_project_structure(dirname, args.project)

	print("Project", args.project , "was successfully created.")

