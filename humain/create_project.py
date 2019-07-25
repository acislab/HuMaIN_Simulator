#!/usr/bin/env python3
import argparse
import os, shutil, errno, csv
from humain.constants import *

# Create files inside "path" folder
def create_file(path, filename):
    open(os.path.join(path, filename), 'wb')


# Create a new Project
def create_new_folder(dirname):
    print("Creating a new folder!")
    try:
        os.mkdir(dirname)
        print("Project: ", args.project, "created!")
        os.mkdir(dirname+"/tasks")
        os.mkdir(dirname+"/workflows")
        os.mkdir(dirname+"/simulations")
        os.mkdir(dirname+"/results")
        create_file(dirname, "tasks.csv")
        create_file(dirname, "__init__.py")
        create_file(dirname+"/tasks", "__init__.py")
    except FileExistsError:
        print("ERROR: Project", args.project,
              "already exists! Try a different Project Name!")


# Copy Folders and Files
def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise


# Delete files and subdirectories of specified folders
def delete_files_folders(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


if __name__ == '__main__':
	""" Creates a new file and copies into a new file if required.
	"""
	parser = argparse.ArgumentParser("Creates a new project file.")
	parser.add_argument('-n', '--project', action="store", required=True, help="New Project's name")
	parser.add_argument('-c', '--copy', action="store", required=False, help="Copy from existing project")
	args = parser.parse_args()

	print("New Project name: ", args.project)
	dirname = BASE_DIR + "/" + args.project
	print(dirname)

	if args.copy is not None:
		try: 
			print("Copying from: ", args.copy)
			dircopy = os.path.pardir + "/" + args.copy
			if os.path.isdir(dircopy): 
				copyanything(dircopy, dirname)
				# Remove the Result files
				result_folder = dirname+"/results"
				delete_files_folders(result_folder)
			else: 
				print("ERROR: Folder", args.copy, "does not exist!")
		except FileExistsError:
			print("ERROR: Project" , args.project ,  "already exists! Try a different name!")
	else:
	    create_new_folder(dirname)


# usage: python3 common/create_project.py --project test
