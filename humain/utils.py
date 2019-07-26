#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Functions of common utilization in all the simulator's code
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

import os, sys, shutil, errno
import datetime, re

##############################################################################################################################
# 
def verify_dir( dir_name, error_msg, parser, error_code ):
	if ( not os.path.isdir( dir_name ) ):
		print( "\nERROR: " + error_msg + "\n" )
		if parser:
			parser.print_help()
		if error_code:
			sys.exit( error_code )

##############################################################################################################################	
#	
def verify_create_dir( dir_name, error_msg, parser, error_code ):
	if not os.path.exists( dir_name ):
		try:
			os.makedirs( dir_name )  
		except:
			print( "\nERROR: " + error_msg + "\n" )
			if parser:
				parser.print_help()
			if error_code:
				sys.exit( error_code )

##############################################################################################################################	
#	
def verify_create_file( filename, error_msg, parser, error_code ):
	try:
		f = open(filename, "w+") 
		f.close() 
	except:
		print( "\nERROR: " + error_msg + "\n" )
		if parser:
			parser.print_help()
		if error_code:
			sys.exit( error_code )
        		
##############################################################################################################################
#	
def verify_file( filename, error_msg, parser, error_code ):
	if ( not os.path.isfile( filename ) ):
		print( "\nERROR: " + error_msg + "\n" )
		if parser:
			parser.print_help()
		if error_code:
			sys.exit( error_code )

##############################################################################################################################
#
def write_log( log_pathfilename, msg, init = False ):
	open_format = "a+"
	if init:
		open_format = "w+"

	try:
		with open( log_pathfilename, open_format ) as log_f:
			log_f.write(str('[{date:%Y-%m-%d %H:%M:%S}]'.format( date=datetime.datetime.now() ) + " " + msg + "\n") )
	except IOError:
		print( "\nERROR: The log file could not be accessed (" + log_pathfilename + ").\n" )
		sys.exit( 100 )

##############################################################################################################################
#
def verify_file_ext( pathfilename, ext ):
	extracted_ext = pathfilename[-(len(ext)):].lower()
	if ( extracted_ext != ext.lower() ):
		return(False)
	if ( not os.path.isfile( pathfilename ) ):
		return(False)
	return(True)

##############################################################################################################################
#
def verify_dir_ext( dir_name, ext ):
	if ( not os.path.isdir( dir_name ) ):
		return(False)
	filenames = os.listdir(dir_name)
	filename_list = list(f for f in filenames if f.endswith( "." + ext.lower() ) )
	if len(filename_list) == 0:
		return(False)
	return(True)

##############################################################################################################################
#
def read_section_lines( pathfilename, section_name ):
	lines = ""
	copy_started = False
	with open( pathfilename, "r" ) as f:
		for line in f:
			line = line[:-1]
			parts = line.split(' ')
			if (len(parts) > 0):
				if (parts[0] == section_name):
					copy_started = True
				else:
					if copy_started == True:
						if len(parts[0]) > 0:
							if parts[0][0] == '[':
								# Stop copying
								break
							elif parts[0][0] != '#':
								# Copy line
								lines += line + "\n"			
	return( lines )

##############################################################################################################################
# Copy Folders and Files
def copy_anything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

##############################################################################################################################
# Delete files and subdirectories of specified folders
def delete_files_folders(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

