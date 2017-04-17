# -*- coding: utf-8 -*-
"""                                                                                       
Extract data from Neuralynx data files
  
Usage
-----
nlx_process(tank_dir)  
  
"""           

import os, glob, re, pylab
import numpy as np
from scipy import stats

# Import custom function
os.chdir('/home/lab/Cloud2/movies/human/LazerMorph/py_analyze/neural')
from nlx_read import nlx_read

def scr_file_sz(fnames):
    """ Screen list of files for non-empty members """
    fsizes = np.array([os.stat(x).st_size for x in fnames]) # Get sizes
    return fnames[np.where(fsizes>fsizes.min())] # Keep >min size files
    
def sort_nice(list_input): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return np.asarray(sorted(list_input, key = alphanum_key))
    
def get_crossings(analog_signal):
    """ Read photodiode analog signal, extract timing of onset/offset """
    # analog_signal = analog_list[0]
    analog_z = stats.zscore(analog_list[0])
    minCross = np.where(analog_z>1)[0] # Crossings of minimum threshold
    trialDur = analog_fs*.5 # Approximate number of samples for each trial (~500 msec)
    isoCross = np.where(np.diff(minCross)>int(trialDur))[0]
    minCross[isoCross]

 
def main():
    
    tank_dir = '/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/'
    tank_name = os.path.basename(os.path.normpath(tank_dir))
    
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
    [t_stamps, event_id, ttl, event_str] = nlx_read(tank_dir+'Events.nev')
        
    # Select continuously-sampled channels
    digital = {
        'signal':np.vstack([item[0] for item in LFP_list]), # Convert list into 2-D matrix 
        'times':LFP_list[0][1], # Select only timestamps vectors
        'fs':LFP_list[0][2][0] # Select only fs value
        }
#    dig_mat = np.vstack(dig_list)   
#    dig_time = LFP_list[0][1] 
#    dig_fs = LFP_list[0][2][0]
    
    analog = {
        'signal':np.vstack([item[0] for item in Inpt_list]), # Convert list into 2-D matrix 
        'times':Inpt_list[0][1], # Select only timestamps vectors
        'fs':Inpt_list[0][2][0] # Select only fs value
        }
#    analog_list = np.vstack([item[0] for item in Inpt_list]) # Select only analog channels
#    analog_time = Inpt_list[0][1] # Select only timestamps vectors
#    analog_fs = Inpt_list[0][2][0] # Select only fs value

    filename = os.path.join(tank_dir,tank_name)
#     np.save(filename,digital, allow_pickle=True)
#     
#     pickle.dump(digital, open("filename.p", "wb"))
#     
#     with open(filename, 'wb') as handle:
#         pickle.dump(digital, handle, protocol=pickle.HIGHEST_PROTOCOL)

main()
    
    
