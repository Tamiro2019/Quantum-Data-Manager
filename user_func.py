import numpy as np
import scipy as sp

import random

from quspin.operators import hamiltonian # Hamiltonians and operators
from quspin.basis import spin_basis_1d # Hilbert space spin basis


def H_mapper(L, basis, x):
    ''' 
    Make Hamiltonian for a system of size L in a specific basis, given a parameter tuple x.
    '''
    
    #print('x = ', x)
    
    # Try to assign parameters into a readable form
    try:
        alpha = x[0]
        beta = x[1]
        gamma = x[2]
        g = gamma*np.linspace(-0.5,0.5,L-1) #
        
    except ValueError: 
        print("Oops! looks like you are trying to call H_mapper with a parameter tuple x which\
        does not match the expected parameters in H_mapper.")


    ## Give specifications for quspin
    
    # one-body operators : list of [coupling-value, i], where i is position of a spin in the chain
    h_z = [[beta, i] for i in range(L)] 
    
    # two-body operators : list of [coupling-value, i,j], where i, j are positions of two spins in the chain.
    J_xx = [[g[i-1],i-1,i] for i in range(1,L)] 
    J_yy = [[g[i-1],i-1,i] for i in range(1,L)] 
    J_zz = [[alpha*(g[i-1]),i-1,i] for i in range(1,L)] 

    ## Create quspin Hamiltonian Object
    static = [["xx",J_xx ],["yy",J_yy],["zz",J_zz],["z",h_z]]
    dynamic = []

    H_obj = hamiltonian(static,dynamic,basis=basis,dtype=np.float64,check_pcon=False,check_symm=False,check_herm=False) 
    
    # Make array from quspin Hamiltonian object
    H_array = np.array(H_obj.todense())
    
    return H_array 


def E_func(L,basis,x,H,E,V):
    '''
    Return the set of all energies of a Hamiltonian
    '''
    
    return E


def S0z_func(L,basis,x,H,E,V):
    '''
    Return the set of all expecation values of the Sz operator (for the 0-th site in the spin chain),
    taken over all eigenstates of a Hamiltnian.
    '''
    
    # make one-body operator 
    J_z = [[1.0,0]] # coupling = 1.0 at site 0
    
    # make quspin operator object
    static = [["z",J_z]] # attach coupling to z spin operator
    dynamic = []
    
    S0_z = hamiltonian(static,dynamic,dtype=np.float64,basis=basis,check_pcon=False,check_symm=False,check_herm=False)
        
    # loop over all eigenstates, and use quspin's matrix_ele function to evaluate expectation values
    Savg = np.zeros((basis.Ns,))
    
    for i in range(basis.Ns): 
        Savg[i] = S0_z.matrix_ele(V[:,i],V[:,i],time=0.)

    return Savg


def A_norm_func(L,basis,x,H,E,V):
    '''
    Computes the norm of the adiabatic gauge potential A for a driving Hamiltonian dH. 
    '''
    
    # Assign useful parameters
    gamma = x[2]
    g = gamma*np.linspace(-0.5,0.5,L-1)
    
    # Make driving Hamiltonian operator, using quspin:
    
    # Let's drive the chain of Sz_i * Sz_{i+1} operators.
    
    h_zz = [[g[i-1],i-1,i] for i in range(1,L)] 

    static = [["zz",h_zz]]
    dynamic = []

    dH_obj = hamiltonian(static,dynamic,basis=basis,dtype=np.float64,check_pcon=False,check_symm=False,check_herm=False) 
    dH = np.array(dH_obj.todense())
    
    # Put dH in energy basis
    dH_E = np.dot( np.transpose(np.conj(V)), np.dot(dH, V) )
    
    # Create the matrix elements of the gauge potential:
    Ematrix = np.transpose(np.array([E,]*(len(E)))) - np.array([E,]*(len(E))) 
    Ematrix[np.abs(Ematrix) < 1e-14 ] = 0 
    
    Amat = np.divide(dH_E, Ematrix) 
    Amat [np.isinf(Amat)== True] = 0.0 # get rid of infs
    Amat [np.isnan(Amat)== True] = 0.0 # get rid of infs

    # Generate the norm of the gauge potential
    A_norm = np.sum(np.sum(np.multiply(Amat,Amat)))

    return [A_norm] # inserted into a list to satisfy np.savetxt() in make_date()