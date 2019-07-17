#!/usr/bin/env python3
import argparse, shutil
import pandas
from humain.common.constants import *
from humain.common.utils import *

if __name__ == '__main__':
	""" Get the simulated execution result from an OCR engine
	"""
	parser = argparse.ArgumentParser("Run tesseract over all the images of an specified folder.")
	parser.add_argument('-e', '--engine', action="store", required=True, help="OCR engine: ocropus, tesseract, or gc-ocr.")
	parser.add_argument('-d', '--dataset', action="store", required=True, help="Biocollection or dataset name.")
	parser.add_argument('-f', '--filename', action="store", required=True, help="Filename of the image to process.")
	parser.add_argument('-m', '--metric', action="append", required=True, help="One or more metrics that will be collected when executing the ocr.")
	parser.add_argument('-o', '--out_dir', action="store", required=True, help="Directory where the ocr transcription of the image will be stored.")
	args = parser.parse_args()
	# Usage example
	# python3 /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/tasks/ocr_specimen.py -e ocropus -d aocr_insects -f EMEC609576_Cerceris_compacta.jpg -m duration -o /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/results

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################
    
	# args.dataset
	dataset_dir = DATASETS_DIR + "/" + args.dataset
	verify_dir( dataset_dir, 'The dataset directory (' + dataset_dir + ') was not found: ', parser, 1 )

	# args.engine
	engine_dir = dataset_dir + "/ocr/" + args.engine
	verify_dir( engine_dir, 'The directory of the engine results (' + engine_dir + ') was not found in the dataset folder.', parser, 2 )

	# args.filename
	txt_name = args.filename.split('.')[0] + ".txt"
	pathfilename = engine_dir + "/" + txt_name
	verify_file( pathfilename, 'The image file was not found in the directory of the engine results.', parser, 3 )

	# args.out_dir
	verify_create_dir( args.out_dir, 'The destination directory, for the text file, was not found and could not be created.', parser, 4 )
	verify_create_dir( args.out_dir + "/metrics", 'The destination metric directory was not found and could not be created.', parser, 5 )

	# args.metric
	metrics_dir = ""
	if len(args.metric) > 0:
		# Metric directory
		metrics_dir = engine_dir + "/metrics"
		verify_dir( metrics_dir, 'The metrics directory was not found.', parser, 6 )
		# Metric files
		for m_name in args.metric:
			verify_file( metrics_dir + "/" + m_name + ".csv", 'The file metric ' + m_name + ' was not found in the metrics directory.', parser, 7 )

	################################################################################################################################
	# COPY THE TEXT FILE TO THE EXPERIMENT'S RESULT FOLDER
	################################################################################################################################	
	try:
		shutil.copy( pathfilename, args.out_dir )
	except (OSError, IOError):
		print('ERROR: The file ' + pathfilename + ' could not be copied to ' + args.out_dir + '.\n')
		sys.exit(8)

	################################################################################################################################
	# INSERT THE LINES WITH THE METRIC'S VALUES - FOR EACH METRIC
	################################################################################################################################	
	if len(args.metric) > 0:
		# Metric files
		for m_name in args.metric:
			metric_filename_src = metrics_dir + "/" + m_name + ".csv"
			# Load the content of the file in a dataframe
			df = pandas.read_csv( metric_filename_src, header=None, names=('img_name', 'value') )
			metric_row = df.loc[ df['img_name'] == args.filename ]
			if ( len(metric_row)>0 ):
				value = metric_row.iloc[0, 1]
				metric_filename_dst = args.out_dir + "/metrics/" + m_name + ".csv"
				with open(metric_filename_dst, 'a+') as fd:
					fd.write(args.filename + "," + str(value) + "\n")
			else:
				print('ERROR: It was not found a metric ' + m_name + ' value for image ' + args.filename + '.\n')
				sys.exit(9)