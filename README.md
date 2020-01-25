# Quantum Data Manager
### A data managing system for simulations with quantum mechanical models

Computer simulations are an essential part of a quantum physicist's toolkit. Today physicists spend as much time, if not more,
in front of a computer as they do running experiments in a lab or writing equations on a chalk board. Programming and running 
complex simulations of realistic physical systems can be a slow time consuming process, and newcomers often waste a 
substantial amount of time trying to organize their output or continually re-running entire programs everytime a minor change is made. Therefore, it is key that they learn how to manage their output data quickly 
and seamlessly, freeing up time and mental space to analyze the physical implications of their results.   

This quantum data manager system provides a simple program to organize large simulation data into files, and retrieve the data into a [pandas](https://pandas.pydata.org/pandas-docs/stable/) dataframe for easy management. This system allows the user to modify or create python functions which set up a physical system of interest (through a Hamiltonian operator), simulaton parameters, and outputs. There is no restriction on the class of models (provided they can be expressed using a Hamiltonian operator) or the simulation outputs, as long as they can be reasonably computed and the user has enough storage space for the output data. 

The default setup of the quantum data manager also provides an example physical system, with some basic sets of parameters and outputs, to showcase the system's workflow. These examples use [quspin package](http://weinbe58.github.io/QuSpin/) to quickly and effectively construct physical operators common in quantum mechanics; the user is encouraged to explore quspin although it is not essential and can be removed from the system if needed. We have also included a jupyter notebook ([Data_Manager.ipynb](https://github.com/Tamiro2019/Quantum-Data-Manager/blob/master/Data_Manager.ipynb))

## 

## Launch
