#!/usr/bin/env python3

##########################################################################################
# Developers: 	Icaro Alzuru and Aditi Malladi
# Project: 		HuMaIN (http://humain.acis.ufl.edu)
# Description: 	Constants to use through the entire simulator: Directories and datatypes.
#				The BASE_DIR must be customized after cloning the repository.
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

BASE_DIR = "/home/ialzuru/Summer2019/HuMaIN_Simulator"
DATASETS_DIR = BASE_DIR + "/datasets"

INPUT_TYPES = ['INT', 'FLOAT', 'STRING', 'LIST', 'JPG', 'TXT', 'TSV', 'D_JPG', 'D_TXT']
OUTPUT_TYPES = ['O_JPG', 'O_TXT', 'O_TSV', 'O_D_AR', 'O_D_JPG', 'O_D_TXT']
DATATYPES = INPUT_TYPES + OUTPUT_TYPES
# The Datatypes JPG, TXT, D_JPG, D_TXT will be checked before the Task starts
# The Datatypes O_JPG, O_TXT, O_D_JPG, O_D_TXT will be checked after the Task has been executed, and they will not be sent as input parameters to execute the Task.
