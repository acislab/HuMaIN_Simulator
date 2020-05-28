#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Extract the event-date DC term from the text files of a directory
##########################################################################################
# Copyright 2020    Advanced Computing and Information Systems (ACIS) Lab - UF
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

import os, sys, argparse, re
import pandas as pd

####################################################################################################
# Regular expressions to be considered for day, month, and year
day = re.compile(r'\b(0?[1-9]|[12][\d]|3[01])\b')

month_word = re.compile(r'\b(january|february|march|april|may|june|july|august|september|october|november|december|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|\
	diciembre|jan|feb|mar|apr|may|jun|jul|aug|sep[t]?|oct|nov|dec|ene|abr|ago|dic|i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii|mch|[1-9]|01|02|03|04|05|06|07|08|09|10|11|12)\b')
# month_roman = re.compile(r'\b(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii)\b')
# month_number = re.compile(r'\b([1-9]|10|11|12)\b')

year_long = re.compile(r'\b(1[89]\d\d|200[\d])\b')
year_short = re.compile(r'\b(\d\d)\b')

special = re.compile('[\W_]+')
####################################################################################################

dict_m = {'january':1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, \
	'september': 9, 'october': 10, 'november': 11, 'december': 12, 'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, \
	'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12, 'enero': 1, 'febrero': 2, \
	'marzo': 3, 'abril':4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, \
	'noviembre': 11, 'diciembre': 12, 'ene': 1, 'abr': 4, 'ago': 8, 'sept': 9, 'dic': 12, \
	'i':1, 'ii':2, 'iii':3, 'iv':4, 'v':5, 'vi':6, 'vii':7, 'viii':8, 'ix':9, 'x':10, 'xi':11, 'xii':12, \
	'mch': 3, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, '11':11, '12':12, \
	'01':1, '02':2, '03':3, '04':4, '05':5, '06':6, '07':7, '08':8, '09':9	}

####################################################################################################

def date_to_string( d , n = 2 ):
	if d in dict_m:
		v = "000" + str(dict_m[d])
		v = v[-n:]
		return(v)
	else:
		print("\nERROR: The integer value for the date component was not found. Unknown value: " + d + "\n")
		return("")

def two_dig( d ):
	v = "0" + str(d)
	v = v[-2:]
	return(v)

def getDate( s ): # Return: isDate, month, day, year, length
	# Scan the whole string in search of dates
	w4, w3, w2, w1, w0 = "", "", "", "", ""
	dates_list = []
	
	for w in s.split():
		w4 = w3
		w3 = w2
		w2 = w1
		w1 = w0
		w0 = w

		######################## YEAR #########################
		year_4d = ""	
		# Year long
		y_long = year_long.match(w0)
		if y_long:
			year_4d = y_long.group(0)
		# else:
		# 	# Year short
		# 	y_short = year_short.match(w0)
		# 	if y_short:
		# 		# 2 digits year must be converted, for comparison purposes, to four digits
		# 		year_4d = str(1900 + int(y_short.group(0)))

		######################## MONTH #######################
		if (year_4d != ""):
			m4 = month_word.match(w4)
			d4 = day.match(w4)

			m3 = month_word.match(w3)
			d3 = day.match(w3)

			m2 = month_word.match(w2)
			d2 = day.match(w2)

			m1 = month_word.match(w1)
			d1 = day.match(w1)

			if m4 and d3 and m2 and d1: # Format MM DD MM DD YYYY
				v = year_4d + "-" + date_to_string(m4.group(0)) + "-" + two_dig(d3.group(0)) + "/" + date_to_string(m2.group(0)) + "-" + two_dig(d1.group(0))
				dates_list.append( v )
			elif d4 and m3 and d2 and m1: # Format DD MM DD MM YYYY
				v = year_4d + "-" + date_to_string(m3.group(0)) + "-" + two_dig(d4.group(0)) + "/" + date_to_string(m1.group(0)) + "-" + two_dig(d2.group(0))
				dates_list.append( v )
			elif m3 and d2 and d1: # Format w4 MM DD DD YYYY
				v = year_4d + "-" + date_to_string(m3.group(0)) + "-" + two_dig(d2.group(0)) + "/" + two_dig(d1.group(0))
				dates_list.append( v )
			elif d3 and d2 and m1: # Format w4 DD DD MM YYYY
				v = year_4d + "-" + date_to_string(m1.group(0)) + "-" + two_dig(d3.group(0)) + "/" + two_dig(d2.group(0))
				dates_list.append( v )
			elif m2 and d1: # Format w4 w3 MM DD YYYY
				v = year_4d + "-" + date_to_string(m2.group(0)) + "-" + two_dig(d1.group(0))
				dates_list.append( v )
			elif d2 and m1:  # Format w4 w3 DD MM YYYY
				v = year_4d + "-" + date_to_string(m1.group(0)) + "-" + two_dig(d2.group(0))
				dates_list.append( v )
			elif m2 and m1: # Format w4 w3 MM MM YYYY
				v = year_4d + "-" + date_to_string(m2.group(0)) + "/" + date_to_string(m1.group(0))
				dates_list.append( v )
			elif m1: # Format w4 w3 w2 MM YYYY
				v = year_4d + "-" + date_to_string(m1.group(0))
				dates_list.append( v )
		else:
			y_long = year_long.match(w4)
			if y_long:
				year_4d = y_long.group(0)

				m3 = month_word.match(w3)
				d3 = day.match(w3)

				m2 = month_word.match(w2)
				d2 = day.match(w2)

				m1 = month_word.match(w1)
				d1 = day.match(w1)
				
				m0 = month_word.match(w0)
				d0 = day.match(w0)

				if m3 and d2 and m1 and d0: # Format YYYY MM DD MM DD
					v = year_4d + "-" + date_to_string(m3.group(0)) + "-" + two_dig(d2.group(0)) + "/" + date_to_string(m1.group(0)) + "-" + two_dig(d0.group(0))
					dates_list.append( v )
				elif d3 and m2 and d1 and m0: # Format YYYY DD MM DD MM
					v = year_4d + "-" + date_to_string(m2.group(0)) + "-" + two_dig(d3.group(0)) + "/" + date_to_string(m0.group(0)) + "-" + two_dig(d1.group(0))
					dates_list.append( v )
				elif m3 and d2 and d1: # Format YYYY MM DD DD w0
					v = year_4d + "-" + date_to_string(m3.group(0)) + "-" + two_dig(d2.group(0)) + "/" + two_dig(d1.group(0))
					dates_list.append( v )
				elif d3 and d2 and m1: # Format YYYY DD DD MM w0
					v = year_4d + "-" + date_to_string(m1.group(0)) + "-" + two_dig(d3.group(0)) + "/" + two_dig(d2.group(0))
					dates_list.append( v )
				elif m3 and d2: # Format YYYY MM DD w1 w0
					v = year_4d + "-" + date_to_string(m3.group(0)) + "-" + two_dig(d2.group(0))
					dates_list.append( v )
				elif d3 and m2:  # Format YYYY DD MM w1 w0
					v = year_4d + "-" + date_to_string(m2.group(0)) + "-" + two_dig(d3.group(0))
					dates_list.append( v )
				elif m3 and m2: # Format YYYY MM MM w1 w0
					v = year_4d + "-" + date_to_string(m3.group(0)) + "/" + date_to_string(m2.group(0))
					dates_list.append( v )
				elif m3: # Format YYYY MM w2 w1 w0
					v = year_4d + "-" + date_to_string(m3.group(0))
					dates_list.append( v )
				else: # Format YYYY w3 w2 w1 w0
					v = year_4d + "z"
					dates_list.append( v )
	return(dates_list)



if __name__ == '__main__':
	""" Extract the event-date DC term from the text files of a directory
	"""
	parser = argparse.ArgumentParser("Extract the event-date DC term from the text files of a directory.")
	parser.add_argument('-sd', '--srcdir', action="store", required=True, help="Directory where the text files are located.")
	parser.add_argument('-o', '--output_file', action="store", required=True, help="Text file where the filename and event-date values will be saved.")
	args = parser.parse_args()
	# Usage example
	# python3 getDate_dir.py -sd ./test/input -o ./test/output/test.tsv

	# Arguments Validations
	if ( not os.path.isdir( args.srcdir ) ):
		print('Error: The directory with the text and prob files was not found.\n')
		parser.print_help()
		sys.exit(1)

	# Create the lists of files to process
	files_list = list()
	for root, dirs, filenames in os.walk( args.srcdir ):
		files_list = list(f for f in filenames if f.endswith('.txt'))

	# Process each text file
	output_text = ""
	for filename in files_list:
		txt_path_filename = args.srcdir + "/" + filename

		# Read the content of the text file
		f = open(txt_path_filename, 'r')
		label = f.read().replace('\n', ' ').lower()
		f.close()
		
		# Eliminate special characters
		label = special.sub(' ', label)
		label = re.sub(' +', ' ', label)
		dates_list = getDate( label )

		if ( len(dates_list) > 0 ):
			dates_list.sort() 	# Take the oldest date
			final_date = dates_list[0]
			if len(final_date) == 5:
				final_date = final_date[:-1]
			output_text += filename + '\t' + final_date + '\n'

	with open(args.output_file, "w") as os:
		os.write(output_text)
