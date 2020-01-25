import numpy as np
import scipy as sp
import pandas as pd

import random
import time 
import os
import itertools 
import warnings

from quspin.operators import hamiltonian # Hamiltonians and operators
from quspin.basis import spin_basis_1d # Hilbert space spin basis

from user_func import *

from pathlib import Path

dir_path = os.path.dirname(os.path.realpath("__file__"))

warnings.filterwarnings("ignore", category=RuntimeWarning)

def make_data( vs=0, L=8, g_id_list=[0] , param_labels = ['alpha','beta', 'gamma'], param_values=[[0.0,0.5,1.0],[1.0],[0.1,1.0]],
              Qs = ['E','S0z','A_norm'], exact_diag = True, write = True):
    '''
    The make_data() function takes the following inputs:
    * vs (number) : version
    * L (int) : system size (e.g. length of a spin chain) 
    * g_id_list (ints): list of identifiers, useful when using multiple realizations over random parameters
    * param_labels (strings) : list of parameter labels
    * param_values (numbers of arrays) : list of lists, each of which contains the values for the corresponding parameter label. 
    * Qs (strings) : list of quantities, whose functions will be called
    * exact_diag (boolean) : Default = True. True enables exact diagonalization of Hamiltonian.
    * write (boolean) : Default = True. True enables writing data to files.
    
    make_data() makes a directory /Sim_Data/, if one is not already available.
    
    make_data() loops over all parameter configuration in param_values, and
        calls the user-defined quantity functions for the specified Qs.
        
    make_data() writes data into text files inside /Sim_Data/.
    
    '''
    
    
    if write == True:
        if not os.path.exists( dir_path+'/Sim_Data/'):
            os.makedirs( dir_path+'/Sim_Data/')

        front = dir_path+'/Sim_Data/'
        
        lab_tup = tuple(param_labels)
    
    
    # create iterator over param_list
    
    looper = itertools.product(*param_values)
    
    # make basis object for quspin
    
    basis = spin_basis_1d(L, pauli=False, S= "1/2")
    
    for g_id in g_id_list: # loop over realizations: relevant e.g. for disordered systems:
        
        for x in looper: # loop over all parameter combinations

            H = H_mapper(L, basis, x) # extract Hamiltonian (array or obj) using user-defined function 

            if exact_diag == True: # find exact eigenvalues and eigenvectors if requested

                [E,V] = np.linalg.eigh(H) 

            for q in Qs: # loop over all quantity/observable requests

                qfunc = q + '_func'
                #print(qfunc)

                try: # try to evaluate user defined function

                    if exact_diag == True:

                        try:
                            Qvalue = globals()[qfunc](L,basis,x,H,E,V) # look for local function with name q and call it
                        except ValueError: 
                            print("Oops! looks like you defined "+ qfunc+"to have different inputs than (L,basis,x,H,E,V).\
                            Maybe exact_diag needs to be set properly.")
                        if write == True:
                            tail = '_vs='+str(vs) +'_L='+ str(L)+'_gid='+str(g_id) + '_' + str(lab_tup) + '=' + str(x)+ '.txt'
                            filename = front + q + tail
                            np.savetxt(filename, Qvalue, fmt='%.15e')
                            #print(filename)

                    else:

                        try: 
                            Qvalue = globals()[qfunc](L,basis,x,H) # look for local function with name q and call it
                        except ValueError: 
                            print("Oops! looks like you defined " + qfunc + "to have different inputs than (L,basis,x,H).\
                            Maybe exact_diag needs to be set properly.")

                        if write == True:
                            tail = '_vs='+str(vs) +'_L='+ str(L)+'_gid='+str(g_id) + '_' + str(lab_tup) + '=' + str(x)+ '.txt'
                            filename = front + q + tail
                            np.savetxt(filename, Qvalue, fmt='%.15e')
                            #print(filename)

                except ValueError: 
                    print("Oops! looks like you haven't defined: ", qfunc)
               
def retrieve_data(vs=0, L_list=[8], g_id_list=[0] , param_labels = ['alpha','beta', 'gamma'], param_values=[[0.0,0.5,1.0],[1.0],[0.1,1.0]],
              Qs = ['E','S0z','A_norm']):
    '''
    The retrieve_data() function takes the following inputs:
    * vs (number) : version
    * L_list (ints) : list of system sizes 
    * g_id_list (ints): list of identifiers, useful when using multiple realizations over random parameters
    * param_labels (strings) : list of parameter labels
    * param_values (numbers of arrays) : list of lists, each of which contains the values for the corresponding parameter label. 
    * Qs (strings) : list of quantities, whose functions will be called
    
    retrieve_data() loops over all parameter configuration in param_values, retrieves data from files in /Sim_Data/.
    retrieve_data() assembles this data into a single dataframe.  
    '''
    
    
    front = dir_path+'/Sim_Data/'
    lab_tup = tuple(param_labels)
    
    df_cols = ['L','g_id'].copy()
    df_cols.extend(param_labels)
    df_cols.extend(Qs)
    #print(df_cols)
    df = pd.DataFrame(columns = df_cols ) # make data frame
    
    # extend parameter list for looper
    param_values_ext = param_values.copy()
    
    param_values_ext.append(L_list)
    param_values_ext.append(g_id_list)
    
    looper = itertools.product(*param_values_ext)

    for x0 in looper: # loop over all parameter combinations

        x = x0[:-2]
        L = x0[-2]
        g_id = x0[-1]
        
        #print(x)
        
        tail = '_vs='+str(vs) +'_L='+ str(L)+'_gid='+str(g_id) + '_' + str(lab_tup) + '='+ str(x)+ '.txt'

        row_tuples = [('L',L),('g_id',g_id)]
        row_tuples.extend(zip(param_labels,x))
        row_dict = dict(row_tuples)

        for name in Qs:

            filename = front + name + tail
            Q = np.loadtxt(filename) # quantity vector
            row_dict[name]= Q

        df = df.append(row_dict, ignore_index=True) 

            
    return df


if __name__ == "__main__":
    
    L_list = [7] #[5,6,7,8,9,10]
    for l in L_list :
        make_data(vs = 1, L=l, g_id_list=[-1])

    df = retrieve_data(vs = 1, L_list=L_list, g_id_list=[-1])
    print(df.head())
        