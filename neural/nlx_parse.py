# -*- coding: utf-8 -*-
"""                                                                                       
Parse data extracted from Neuralynx data files
  
Usage
-----
nlx_parse()  
  
"""           

import os, glob
import numpy as np
import pylab

os.chdir('/home/lab/Cloud2/movies/human/LazerMorph/py_analyze/neural')
from nlx_read import nlx_read

#[cscs, time_stmps, fs] = nlx_read('/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/CSC1.ncs')
 
def main():
    
    tank_dir = '/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/'
    
    # Get list of each file type for given recording tank, then read each into a list
    LFP_list = [nlx_read(x) for x in glob.glob(tank_dir+'LFP*.ncs')] 
    PDes_list = [nlx_read(x) for x in glob.glob(tank_dir+'PDes*.ncs')] 
#    CSC_list = [nlx_read(x) for x in glob.glob(tank_dir+'CSC*.ncs')] 
    Inpt_list = [nlx_read(x) for x in glob.glob(tank_dir+'Inpt*.ncs')] 

    
    cscs_list = [item[0] for item in LFP_list] # Select only continuously-sampled channel vectors
    # times_list = [item[1] for item in LFP_list] # Select only timestamps vectors
    time = LFP_list[0][1]    
    # fs_list = [item[2] for item in LFP_list] # Select only fs value
    fs = LFP_list[0][2][0]
    del LFP_list
    
    cscs_mat = np.vstack(cscs_list) # Convert list into 2-D matrix
    
    pylab.plot(cscs_mat[1,0:100],'-')
    

    # plt.savefig('py.png')


main()
    
    
