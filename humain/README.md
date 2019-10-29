# humain directory
Common scripts required for running various workflows

#### contants&#46;py
Constants to use through the entire simulator: Directories and datatypes. The BASE_DIR must be customized after cloning the repository.

#### create_project.py
Script to create a new project. Creates the structure of directories for a project, empty or copying the files from an existing project.

#### create_sim_set.py
Create a new simulation file by using an existing simulation. Have the option of having multiple parameters in the same sim file.

#### gen_values.py
Generates values for each file in a given directory or generates a value for each filename in a input csv. 
Can generate random values between some range. 
Generate value at random using the Gaussian distribution using user inputted values of mean and sigma.

#### run_sim_set.py
File runs the simulation set (when the given simulation file has been generated from a prevously exisiting simulation)

#### run_simulation.py
Runs a simulation, which has been previously defined in a simulation file.

#### simulation&#46;py
Simulation class. Loads in memory all the simulation structure: Workflow, Tasks, Parameters, and Simulation. It permits to run pure - and HITL - simulations.

#### utils&#46;py
Functions of common utilization in all the simulator's code
