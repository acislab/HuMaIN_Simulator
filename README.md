# HuMaIN Simulator

## Description
The digitization of biocollections is typically performed through crowdsourcing (volunteers) because of the errors that automated information extraction (IE) methods generate.<br/>
More specifically, Optical Character Recognition technology still generates errors. The segmentation process and the AI recognition models for handwritten text are two of the most challenging cases.<br/>
The HuMaIN simulator expects to promote and accelerate the research in semi-automated IE from biocollections.<br/>
The simulated tasks are tasks for which the results have already been computed.<br/>
The general recommendation is to simulate all the tasks, except that one that you are trying to improve. 

## Acknowledgment
HuMaIN is funded by a grant from the National Science Foundation's ACI Division of Advanced Cyberinfrastructure (Award Number: 1535086).
Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and
do not necessarily reflect the views of the National Science Foundation.


## Installation
The HuMaIN Simulator requires Python 3 installed in your computer. Please refer to https://www.python.org/downloads/ for instructions about how to download and install Python 3 in your operating system.<br/>
To verify the version of Python installed in your computer run:<br/>
```bash
python3 --version
```
You should get an answer similar to the following:
```bash
Python 3.7.2
```

The steps to install the simulator are the following:<br/>
### 1) Clone the HuMaIN Simulator repository. 
From https://github.com/acislab/HuMaIN_Simulator, download the repository as a zip file and locally extract its content, or clone it with git:
```bash
git clone https://github.com/acislab/HuMaIN_Simulator
```
### 2) Update the home directory of the simulator.
In the [Installation_Path]/HuMaIN_Simulator/humain/common/constants.py file, update the value of BASE_DIR to the path of the HuMaIN_Simulator in your computer.
### 3) Update the PYTHONPATH value.
Add the HuMaIN_Simulator directory to PYTHONPATH environment variable of your operating system. For example, in Ubuntu Linux, add the following line to the ~/.bashrc file:
```bash
export PYTHONPATH=$PYTHONPATH:.:/home/user/HuMaIN_Simulator
```
