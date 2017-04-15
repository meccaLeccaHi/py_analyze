# -*- coding: utf-8 -*-

import numpy as np
 
def nlx_read(nlx_filename):
    
    """                                                                                       
    Convert binary Neuralynx data files to decimal form

    The format for a .ncs file:
        uint64 - timestamp in microseconds
        uint32 - channel number
        uint32 - sample freq
        uint32 - number of valid samples
        int16 x 512 - actual csc samples                                                  
                                                                                               
    Parameters                                                                                
    ----------                                                                                
    nlx_filename : String                                                                          
        Filename (preceded by directory path, if not already in Python path)                                                            
                                                                                               
    Returns                                                                                   
    -------                                                                                   
    cscs : (1, samples) array                                                                          
        Continuously sampled channels following analog-to-digital conversion                                                         
                                                                                               
    times : (1, samples) array                                                                            
        Timestamps corresponding to samples in 'cscs'  

    Usage
    -----
    nlx_filename = "/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/LFPx256.ncs"
    [cscs, times] = nlx_read(nlx_filename)                                                                                                                                                                  
    """

    # Open file
    f = open(nlx_filename, 'rb')

    # Neuralynx files have a 16kbyte header
    header = f.read(2 ** 14)
    header.strip(b'\x00')
    
    dt = np.dtype([('time', '<Q'), ('channel', '<i'), ('freq', '<i'),
                   ('valid', '<i'), ('csc', '<h', (512,))])
    data = np.fromfile(f, dt)
    
    # Vectorize the csc matrix
    csc = data['csc'].reshape((data['csc'].size,))
    
    # Get times
    times = data['time'] * 1e-6
    
    # Find the sampling frequency (fs)
    fs = np.unique(data['freq'])[0]
    
    # .ncs files have a timestamp for every ~512 data points.
    # Here, we assign timestamps for each data sample based on the sampling frequency
    # for each of the 512 data points. Sometimes a block will have fewer than 512 data entries,
    # number is set in data['valid']
    this_idx = 0
    n_block = 512.
    offsets = np.arange(0, n_block / fs, 1. / fs)
    times = np.zeros(csc.shape)
    for i, (time, n_valid) in enumerate(zip(times, data['valid'])):
        times[this_idx:this_idx + n_valid] = time + offsets[:n_valid]
        this_idx += n_valid
    
    # Find analog-to-digital conversion factor in the header
    analog_to_digital = None
    for line in header.split(b'\n'):
        if line.strip().startswith(b'-ADBitVolts'):
            analog_to_digital = np.array(float(line.split(b' ')[1].decode()))
    
    if analog_to_digital is None:
        raise IOError("ADBitVolts not found in .ncs header for "+nlx_filename)
    
    cscs = csc*analog_to_digital
    
    # Close file
    f.close()
    
    return cscs, times
