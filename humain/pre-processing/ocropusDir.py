#!/usr/bin/env python2

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Run OCRopus over all the images of an specified folder.
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

import argparse, sys, os, subprocess
import time

DIR_OCROPY = "~/ocropus/ocropy"

#********************************************************************************************************************
def img2txt( pathFilename, dstFolderText ):
	start_time = time.time()
	##########################################################################################
	name1 = pathFilename.split("/")[-1]
	name = name1.split(".")[0]
	dstSubfolderText = dstFolderText + '/' + name
	##########################################################################################
	### Binarization
	c = DIR_OCROPY + "/ocropus-nlbin -n " + pathFilename + " -o " + dstSubfolderText
	r = subprocess.call([c], shell=True)
	if r != 0:
		return (6, "Error: Binarization process failed", 0,  0,  0,  0)
	bin_time = time.time()

	### Segmentation
	c = DIR_OCROPY + "/ocropus-gpageseg -n -q " + dstSubfolderText + "/0001.bin.png"
	r = subprocess.call([c], shell=True)
	if r != 0:
		return (7, "Error: Segmentation process failed", 0,  0,  0,  0)
	seg_time = time.time()
	
	### Character Recognition
	c = DIR_OCROPY + "/ocropus-rpred -n -q -m en-default.pyrnn.gz --probabilities " + dstSubfolderText + "/0001/*.png"
	r = subprocess.call([c], shell=True)
	if r != 0:
		return (8, "Error: Character recognition process failed", 0,  0,  0,  0)
	rec_time = time.time()

	### All text
	newPathFilename = dstSubfolderText + "/" + name + ".txt"
	c = "cat " + dstSubfolderText + "/0001/??????.txt > " + newPathFilename
	r = subprocess.call([c], shell=True)

	newPathFilenameProb = dstSubfolderText + "/" + name + ".prob"
	c = "cat " + dstSubfolderText + "/0001/??????.prob >> " + newPathFilenameProb
	r = subprocess.call([c], shell=True)

	return ( 0, newPathFilename, bin_time - start_time, seg_time - bin_time, rec_time - seg_time, time.time() - start_time )

#********************************************************************************************************************
#********************************************************************************************************************
if __name__ == '__main__':
	""" MAIN """
	#
	# Read arguments
	parser = argparse.ArgumentParser("Run OCRopus over all the images of an specified folder.")
	parser.add_argument('-i', '--input_d', action="store", required=True, help="Input folder, where jpg images are stored.")
	parser.add_argument('-t', '--text_d', action="store", required=True, help="Folder where text files will be stored.")
	parser.add_argument('-o', '--output', action="store", required=True, help="Output file where the duration of the OCR process will be stored, per image.")
	args = parser.parse_args()

	# Arguments Validations
	if ( not os.path.isdir( args.input_d ) ):
		print('Error: The directory of the jpg files was not found.\n')
		parser.print_help()
		sys.exit(1)

	if not os.path.exists( args.text_d ):
		try:
			os.makedirs( args.text_d )  
		except:
			print('Error: The destination directory for the text files was not found and could not be created.\n')
			parser.print_help()
			sys.exit(2)	

	# Execution
	with open(args.output, 'w') as f:
		for root, dirs, files in os.walk( args.input_d ):
			for filename in files:
				if filename.endswith(".jpg"):
					baseFilename = filename[:-4]
					pathFilename = args.input_d + "/" + filename
					r, txt_file, bin_dur, seg_dur, rec_dur, duration = img2txt( pathFilename, args.text_d )
					if r == 0:
						f.write(filename + "," + str(bin_dur) + "," + str(seg_dur) + "," + str(rec_dur) + "," + str(duration) + "\n")
					else:
						f.write(filename + ",-1,0,0,0,0\n")
