#!/usr/bin/env python3
import os, sys
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
def verify_file( filename, error_msg, parser, error_code ):
	if ( not os.path.isfile( filename ) ):
		print( "\nERROR: " + error_msg + "\n" )
		if parser:
			parser.print_help()
		if error_code:
			sys.exit( error_code )
