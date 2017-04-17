# -*- coding: utf-8 -*-
"""                                                                                       
Parse data extracted from Neuralynx data files
  
Usage
-----
nlx_parse()  
"""   
        
main_dir = '/home/lab/Cloud2/movies/human/LazerMorph/'

import os
from scipy import stats
import numpy as np
import pandas as pd

# Import custom module
os.chdir(main_dir+'py_analyze/neural/nlxrd/')
import nlxrd
    
def get_crossings(analog_signal):
    """ Read photodiode analog signal, extract timing of onset/offset """
    # analog_signal = analog_list[0]
    analog_z = stats.zscore(analog_list[0])
    minCross = np.where(analog_z>1)[0] # Crossings of minimum threshold
    trialDur = analog_fs*.5 # Approximate number of samples for each trial (~500 msec)
    isoCross = np.where(np.diff(minCross)>int(trialDur))[0]
    minCross[isoCross]
    
header_dir = main_dir+'headers/'

tank_dir = '/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/'
digital,analog = nlxrd.nlx_process(tank_dir)

# Read LUT for stimuli
lut = pd.read_csv(main_dir+'py_analyze/lazermorphLUT.csv')

# Get photodiode event timing
analog['signal']
analog['times']
analog['fs']



# Read header file
header_fname = header_dir+'hdr03072017_1229.csv'
df = pd.read_csv(header_fname)






    
    
