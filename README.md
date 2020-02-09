# Quantum Data Manager
### A data managing system for simulations with quantum mechanical models

Computer simulations are an essential part of a quantum physicist's toolkit. Today physicists spend as much time, if not more,
in front of a computer as they do running experiments in a lab or writing equations on a chalk board. Programming and running simulations of complex physical systems can be a slow time consuming process, and newcomers often waste a 
substantial amount of time trying to organize their output data. Therefore, it is key that they manage their data effectively and seamlessly, freeing up time and mental space to analyze the physical implications of their results.   

The quantum data manager system provides a simple program to organize large simulation data into files, and retrieve the data into a [pandas](https://pandas.pydata.org/pandas-docs/stable/) dataframe for easy management. This system allows the user to modify or create python functions that set up a physical system of interest (through a Hamiltonian operator) and compute outputs (such as physical properties or observables). There is no restriction on the class of Hamiltonian models, or the simulation outputs, as long as they can be reasonably computed and the user has enough storage space for the output data. 

The default setup of the quantum data manager also provides an example quantum model, with some basic sets of parameters and outputs, to showcase the system's workflow. These examples use the [quspin package](http://weinbe58.github.io/QuSpin/) to quickly and effectively construct physical operators common in quantum mechanics. 

This repository includes a jupyter notebook ([Data_Manager.ipynb](https://github.com/Tamiro2019/Quantum-Data-Manager/blob/master/Data_Manager.ipynb)) which walks through the workflow of the data manager system, and in addition, gives a mini-tutorial on how to use the resulting dataframe for basic plotting and exploratory analysis.

## Key Files

* data_manager.py : main data managing file containing the methods to make and retrieve data into a dataframe.
* user_func.py : user defined functions that are used by data_manager.py to construct simulation data.
* Data_Manager.ipynb : jupyter notebook of the data_manager workflow and a mini-tutorial on using the dataframe.
* requirements.txt : contains a list of all package and version requirements to run the data manager.

## Launch

* Download this repository.
* Make sure to have [Anaconda](https://docs.anaconda.com/anaconda/install/) installed.
* Open a terminal.
* In the terminal, type the following to create a conda environment: $ conda create -n qdm_env python=3.6 
* Acticate the conda environment: $ conda activate qdm_env

Install the requirements using pip:
* Install pip in the qdm_env environment: $ conda install pip
* Tell pip to install all the requirements: $ pip install -r requirements.txt

Alternatively, install the requirements manually in the qdm_env environment:
* Install numpy: $ conda install numpy
* Install scipy: $ conda install scipy
* Install pandas: $ conda install pandas
* Install quspin: $ conda install -c weinbe58 quspin

To run the jupyter notebook:
* Install jupyter in qdm_env : $ conda install jupyter
* Run: $ jupyter notebook
* Open Data_Manager.ipynb
