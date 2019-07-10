#!/usr/bin/env python3
import os, sys
import datetime
# 
def verify_dir( dir_name, error_msg, parser, error_code ):
	if ( not os.path.isdir( dir_name ) ):
		print( "\nERROR: " + error_msg + "\n" )
		if parser:
			parser.print_help()
		if error_code:
			sys.exit( error_code )
	
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
        		
#	
def verify_file( filename, error_msg, parser, error_code ):
	if ( not os.path.isfile( filename ) ):
		print( "\nERROR: " + error_msg + "\n" )
		if parser:
			parser.print_help()
		if error_code:
			sys.exit( error_code )

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

#
def verify_file_ext( pathfilename, ext ):
	extracted_ext = pathfilename[:-(len(ext))].lower()
	if ( extracted_ext != ext.lower() ):
		return(False)
	if ( not os.path.isfile( pathfilename ) ):
		return(False)
	return(True)

#
def verify_dir_ext( dir_name, ext ):
	if ( not os.path.isdir( dir_name ) ):
		return(False)
	filenames = os.listdir(dir_name)
	filename_list = list(f for f in filenames if f.endswith( "." + ext.lower() ) )
	if len(filename_list) == 0:
		return(False)
	return(True)
	
