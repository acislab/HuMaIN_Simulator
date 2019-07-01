#!/usr/bin/env python3
import argparse, shutil

from humain.common.constants import *
from humain.common.utils import *


if __name__ == '__main__':
	""" Get the simulated execution result from an OCR engine
	"""
	parser = argparse.ArgumentParser("Run the specified OCR engine over all the images of an specified collection.")
	parser.add_argument('-e', '--engine', action="store", required=True, help="OCR engine: ocropus, tesseract, or gc-ocr.")
	parser.add_argument('-d', '--dataset', action="store", required=True, help="Biocollection or dataset name.")
	parser.add_argument('-m', '--metric', action="append", required=True, help="One or more metrics that will be collected when executing the ocr.")
	parser.add_argument('-o', '--out_dir', action="store", required=True, help="Directory where the ocr transcription of the image will be stored.")
	args = parser.parse_args()
	
	# Usage example
	# python3 /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/actions/ocr.py -e ocropus -d aocr_insects -m duration -o /home/ialzuru/Summer2019/HuMaIN_Simulator/humain/selfie/results

	################################################################################################################################
	# ARGUMENTS VALIDATIONS
	################################################################################################################################

	# args.dataset
	dataset_dir = DATASETS_DIR + "/" + args.dataset
	verify_dir( dataset_dir, 'The dataset directory (' + dataset_dir + ') was not found: ', parser, 1 )

	# args.engine
	engine_dir = dataset_dir + "/ocr/" + args.engine
	verify_dir( engine_dir, 'The directory of the engine results (' + engine_dir + ') was not found in the dataset folder.', parser, 2 )

	# args.metric
	metrics_dir = ""
	if len(args.metric) > 0:
		# Metric directory
		metrics_dir = engine_dir + "/metrics"
		verify_dir( metrics_dir, 'The metrics directory was not found.', parser, 3 )
		# Metric files
		for m_name in args.metric:
			verify_file( metrics_dir + "/" + m_name + ".csv", 'The file metric ' + m_name + ' was not found in the metrics directory.', parser, 4 )

	# args.out_dir
	verify_create_dir( args.out_dir, 'The destination directory, for the text file, was not found and could not be created.', parser, 5 )
	verify_create_dir( args.out_dir + "/metrics", 'The destination metric directory was not found and could not be created.', parser, 6 )

	################################################################################################################################
	# COPY THE TEXT FILES TO THE EXPERIMENT'S RESULT FOLDER
	################################################################################################################################
	# Create the list of files to process
	filenames = os.listdir(engine_dir)
	filename_list = list(f for f in filenames if f.endswith('.txt'))

	try:
		pathfilename = ""
		for filename in filename_list:
			pathfilename = engine_dir + "/" + filename
			shutil.copy( pathfilename, args.out_dir )
	except (OSError, IOError):
		print('ERROR: The file ' + pathfilename + ' could not be copied to ' + args.out_dir + '.\n')
		sys.exit(8)

	################################################################################################################################
	# INSERT THE LINES WITH THE METRIC'S VALUES - FOR EACH METRIC
	################################################################################################################################	
	if len(args.metric) > 0:
		# Metric files
		metrics_dir_out = args.out_dir + "/metrics"
		for m_name in args.metric:
			metric_filename_src = metrics_dir + "/" + m_name + ".csv"
			try:
				shutil.copy( metric_filename_src, metrics_dir_out )	
			except (OSError, IOError):
				print('ERROR: The metric file ' + metric_filename_src + ' could not be found or copied to ' + metrics_dir_out + '.\n')
				sys.exit(8)