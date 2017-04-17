# -*- coding: utf-8 -*-
"""                                                                                       
Parse data extracted from Neuralynx data files
  
Usage
-----
nlx_parse()  
  
"""           

import os, glob, re
import numpy as np
import pylab

# Import custom function
os.chdir('/home/lab/Cloud2/movies/human/LazerMorph/py_analyze/neural')
from nlx_read import nlx_read

def scr_file_sz(fnames):
    """ Screen list of files for non-empty members """
    fsizes = np.array([os.stat(x).st_size for x in fnames]) # Get sizes
    return fnames[np.where(fsizes>fsizes.min())] # Keep >min size files
    
def sort_nice( list_input ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return np.asarray(sorted(list_input, key = alphanum_key))
 
def main():
    
    tank_dir = '/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/'
    
    # Get list of all LFP files
    LFP_fnames = sort_nice(glob.glob(tank_dir+'LFP*.ncs'))
    
    # Get lists of all non-empty analog files (sorted by channel number)
    Inpt_fnames = scr_file_sz(sort_nice(glob.glob(tank_dir+'Inpt*.ncs')))
    PDes_fnames = scr_file_sz(sort_nice(glob.glob(tank_dir+'PDes*.ncs')))
    
    # Get list of each file type for given recording tank, then read each into a list
    LFP_list = [nlx_read(x) for x in LFP_fnames] 
    PDes_list = [nlx_read(x) for x in PDes_fnames] 
    Inpt_list = [nlx_read(x) for x in Inpt_fnames] 
#    CSC_list = [nlx_read(x) for x in glob.glob(tank_dir+'CSC*.ncs')] 

    # Get event codes
    nlx_read(tank_dir+'Events.nev')
    dig_list = [item[0] for item in LFP_list] # Select only continuously-sampled channels
    dig_time = LFP_list[0][1] # Select only timestamps vectors
    dig_fs = LFP_list[0][2][0] # Select only fs value
    
    analog_list = [item[0] for item in Inpt_list] # Select only analog channels
    analog_time = Inpt_list[0][1] # Select only timestamps vectors
    analog_fs = Inpt_list[0][2][0] # Select only fs value
    
    csc_mat = np.vstack(dig_list) # Convert list into 2-D matrix
    
    pylab.plot(csc_mat[0,0:10000],'-')
    

    # plt.savefig('py.png')


main()
    
    
