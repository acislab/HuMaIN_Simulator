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
	
