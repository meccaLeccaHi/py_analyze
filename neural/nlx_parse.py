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

[cscs, times, fs] = nlx_read('/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/LFPx256.ncs')
 
def main():
    
    tank_dir = '/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/'
    
    LFP_filelist = glob.glob(tank_dir+'LFP*.ncs') # Get list of LFP files for given recording tank
    
    LFP_list = [nlx_read(x) for x in LFP_filelist] # Read each file into list
    
    cscs_list = [item[0] for item in LFP_list] # Select only continuously-sampled channel vectors
    times_list = [item[1] for item in LFP_list] # Select only timestamps vectors
    fs_list = [item[2] for item in LFP_list] # Select only fs value

    cscs_mat = np.vstack(cscs_list) # Convert list into 2-D matrix
    
    pylab.plot(cscs_mat[0,0:1000], '*-')
    plt.imshow(cscs_mat,aspect='auto',interpolation='none',origin='lower')

    # plt.savefig('py.png')


main()
    
    
