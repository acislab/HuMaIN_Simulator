#!/usr/bin/env python

import os, sys, re, codecs, datetime
import argparse, numpy
import pandas as pd

if __name__ == '__main__':
	""" MAIN """
	# Read arguments
	parser = argparse.ArgumentParser("Given some text and a dictionary set (indicated both as files), it returns a list of candidate words with a confidence estimation for each")
	parser.add_argument('-f','--folder',action="store", required=True, help="Directory with the text files to be scanned.")
	parser.add_argument('-d','--dictionary',action="store", required=True, help="Dictionary file.")
	args = parser.parse_args()

	##############################################################################################################################
	# Verify the existence of the directory with the labels
	if not os.path.isdir( args.folder ):
		print('\nERROR: Source folder', args.folder, 'does not exist.\n')
		parser.print_help()
		sys.exit(1)

	##############################################################################################################################
	# The existence of the dictionary is verified
	if ( not os.path.isfile( args.dictionary ) ):
		print('Error: Dictionary file was not found.\n')
		parser.print_help()
		sys.exit(2)
	##############################################################################################################################
	
	# create the dict
	D = {}
	with open(args.dictionary, "r") as f:
		for line in f:
			temp = line[:-1].strip()
			# split using tabs
			t_l = (temp.split("	"))
			if t_l[0] in D:
				data = D.get(t_l[0])
				data += int(t_l[1])
				D[t_l[0]] = data
			else:
				# to avoid the case where nothing has been detected in the original dict
				if len(t_l) != 2:
					continue
				D[t_l[0]] = t_l[1]

	# The dictionary is built
	# df = pd.read_csv( args.dictionary, names = ['value', 'freq'] )
	# D = createDict( df )
	# #print(D)

	# Go through each of the text files of the folder        
	for root, dirs, files in os.walk( args.folder ):
		for filename in files:
			if filename.endswith(".txt"):
				baseFilename = filename[:-4]
				start = datetime.datetime.now()	
			
				# Read the content of the text file, coverting it to unicode
				data = ''
				f = codecs.open( args.folder + '/' + filename, encoding='utf-8', mode='r')
				data = f.read().replace('\n', ' ').lower()
				f.close()
				#print(data)
				data = re.sub(' and | with | & |[,\.]', ' ', data)
				data = ' '.join( data.split() )
				data = data + " a a"
				#print(data)
				w1 = w2 = w3 = w4 = ''
				for w in data.split():
					w1 = w2
					w2 = w3
					w3 = w4
					w4 = w
		
					r1 = D.get(w1)
					if r1 is not None:
						if isinstance(r1, dict):
							r2 = r1.get(w2)
							if r2 is not None:
								if isinstance(r2, dict):
								    r3 = r2.get(w3)
								    if r3 is not None:
								        if isinstance(r3, dict):
								            r4 = r3.get(w4)
								            if r4 is not None:
								                if isinstance( r4, int ):
								                    print("N", baseFilename,w1,w2,w3,w4,str(r2))
								        elif isinstance( r3, int ):
								            print("N", baseFilename,w1,w2,w3,str(r3))
								elif isinstance( r2, int ):
								    print("N", baseFilename,w1,w2,str(r2))
						elif isinstance( r1, int ):
							print("N", baseFilename,w1,str(r1))
					
				end = datetime.datetime.now()
				diff = end - start
				print( "T", baseFilename, str(diff.total_seconds()) )		
	# 			#sys.exit(3)	
    