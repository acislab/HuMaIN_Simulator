# TODO: This is the new one that should be in for XML
import os
import sys
import argparse
import random
import csv
import re
from utils import *
from constants import *
from xml.etree.ElementTree import Element, SubElement, Comment
import xml.etree.ElementTree as ET
import copy


# # read the correct xml section from the exisiting file
# section_name refers to tasks, metircs, post-proc
def replace_result_dir(iter_no, section_name):
    for items in orig_sim_tree.findall(section_name):
        for each_subtask in items:
            for param in each_subtask:
                # find and replace the results directory
                # find and replace results dir
                result_find = "results/" + \
                args.simulation_file.split(".")[0]+"/"
                output_name = (args.output_file).split(".")
                result_replace = "results/" + \
                    output_name[0]+"/"+"SIM_" + \
                    str(iter_no).rjust(2, '0')+"/"
                param.text = re.sub(result_find, result_replace,  param.text)


def find_replace_task(iter_no, args_value):
    for tasks in orig_sim_tree.findall('tasks'):
        for each_task in tasks:
            name_tag = each_task.get('name')
            if name_tag == args.task:
                for param in each_task:
                    param_name = param.get('name')
                    if param_name == args.argument:
                        print("This is the param I want to change")
                        param.text = args.value[0]
                        print(param.text)
                        # here make the change for the task and pass it along
                    else:
                        print("\n")
            else:
                print("\n")
        # tasks_section = copy.deepcopy(tasks)

    # tasks = SubElement(root, 'tasks')
    # root.append(tasks_section)
    # print(ET.tostring(root))

    # add the metrics to it from here
    # change output directory - hello world

    # for metrics in orig_sim_tree.findall('metrics'):
    #     member3 = copy.deepcopy(metrics)

    # root.append(member3)
    # print(ET.tostring(root))
    # tree.write(output_dir)



if __name__ == '__main__':
    """ Create a new simulation set from an exisitng one
    """
    parser = argparse.ArgumentParser(
        "Create a new sim set from an exiting one. Can pass in task parameters to change")
    parser.add_argument('-p', '--project', action="store",
                        required=True, help="Project selected")
    parser.add_argument('-s', '--simulation_file', action="store",
                        required=True, help="Simulation to edit")
    parser.add_argument('-t', '--task', action="store",
                        required=True, help="Task to edit")
    parser.add_argument('-a', '--argument', action="store",
                        required=True, help="Task's parameter or argument to change")
    parser.add_argument('-v', '--value', action="append", required=True,
                        help="Value to put for the parameter selected, can send in more than one.")
    parser.add_argument('-o', '--output_file', action="store", required=True,
                        help="Output csv file for the new simulation filename")
    args = parser.parse_args()

    # usage : python3 create_sim_set2.py -p selfie -s event_date.xml -t ocr_sim -a ocr_input_dir -v datasets/aocr_mix100/ocr/tesseract -v datasets/aocr_mix100/ocr/HELLOWORLD -o new_sim.xml
    #  python3 create_sim_set.py -p selfie -s event_date_001.csv -t ocr_dataset -a dataset -v datasets/aocr_mix100/ocr/tesseract -o new_sim.xml

    project_dir = BASE_DIR + "/" + args.project

    simulation_file = project_dir + "/simulations/" + args.simulation_file
    output_dir = project_dir + "/simulations/" + args.output_file
    # verify the creation of the output file.
    verify_create_file(
        output_dir, 'The output file could not be created.', parser, 4)

    # need to verify that the simulation_file exists
    verify_file(simulation_file, 'The input file does not exist.', parser, 4)

    # read it the xml file
    orig_sim_tree = ET.parse(simulation_file)
    # root for new output XML tree
    root = Element('root')
    tree = ET.ElementTree(root)

    # call function to change the parameters in the tasks
    iter_no = 1
    for param in args.value:
        find_replace_task(iter_no, param)
        replace_result_dir(iter_no, 'tasks')
        replace_result_dir(iter_no, 'metrics')
        replace_result_dir(iter_no, 'post-processing')
        iter_no = iter_no + 1

    for tasks in orig_sim_tree.findall('tasks'):
        tasks_section = copy.deepcopy(tasks)

    for metrics in orig_sim_tree.findall('metrics'):
        metrics_section = copy.deepcopy(metrics)
    
    for post_proc in orig_sim_tree.findall('post-processing'):
        post_proc_section = copy.deepcopy(post_proc) 

    root.append(tasks_section)
    # metrics = SubElement(root, 'metrics')
    root.append(metrics_section)
    # post_proc = SubElement(root, 'post-processing')
    root.append(post_proc_section)
    tree.write(output_dir)


