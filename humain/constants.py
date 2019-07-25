#!/usr/bin/env python3

BASE_DIR = "/home/ialzuru/Summer2019/HuMaIN_Simulator"
DATASETS_DIR = BASE_DIR + "/datasets"

INPUT_TYPES = ['INT', 'FLOAT', 'STRING', 'LIST', 'JPG', 'TXT', 'TSV', 'D_JPG', 'D_TXT']
OUTPUT_TYPES = ['O_JPG', 'O_TXT', 'O_TSV', 'O_D_AR', 'O_D_JPG', 'O_D_TXT']
DATATYPES = INPUT_TYPES + OUTPUT_TYPES
# The Datatypes JPG, TXT, D_JPG, D_TXT will be checked before the Action starts
# The Datatypes O_JPG, O_TXT, O_D_JPG, O_D_TXT will be checked after the Action has been executed, and they will not be sent as input parameters to execute the Action.
