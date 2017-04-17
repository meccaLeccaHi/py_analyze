# -*- coding: utf-8 -*-
"""                                                                                       
Parse data extracted from Neuralynx data files
  
Usage
-----
nlx_parse()  
  
"""           

import os, glob, re, pylab
import numpy as np

# Import custom function
os.chdir('/home/lab/Cloud2/movies/human/LazerMorph/py_analyze/neural')
from nlx_process import nlx_process
    
def get_crossings(analog_signal):
    """ Read photodiode analog signal, extract timing of onset/offset """
    # analog_signal = analog_list[0]
    analog_z = stats.zscore(analog_list[0])
    minCross = np.where(analog_z>1)[0] # Crossings of minimum threshold
    trialDur = analog_fs*.5 # Approximate number of samples for each trial (~500 msec)
    isoCross = np.where(np.diff(minCross)>int(trialDur))[0]
    minCross[isoCross]
    
tank_dir = '/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/'
digital,analog = nlx_process(tank_dir)




    
    
