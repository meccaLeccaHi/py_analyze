# -*- coding: utf-8 -*-

import numpy as np
 
def nlx_read(nlx_filename):
    
    """                                                                                       
    Converts binary Neuralynx data files to decimal form,
    then applies analog-to-digital conversion factor

    The format for a .ncs file:
        uint64 - timestamp in microseconds
        uint32 - channel number
        uint32 - sample freq
        uint32 - number of valid samples
        int16 x 512 - actual csc samples    
        
    For more info on csc files: http://neuralynx.com/techtips/TechTip_mar_2015.html      
                                            
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
        
    fs : int value
        Sampling rate of acquisition hardware (samples/second)

    Usage
    -----
    nlx_filename = "/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/LFPx19.ncs"
    [cscs, times, fs] = nlx_read(nlx_filename)  
                                                                                                                                                          
    """

    # Open file
    f = open(nlx_filename, 'rb')

    # Neuralynx files have a 16kbyte header
    header = str(f.read(2 ** 14)).strip('\x00')
    
    dt = np.dtype([('time', '<Q'), ('channel', '<i'), ('freq', '<i'),
                   ('valid', '<i'), ('csc', '<h', (512,))])
    data = np.fromfile(f, dt)
    
    # Vectorize the csc matrix
    csc = data['csc'].reshape((data['csc'].size,))
    
    # Get times
    t_stamps = data['time'] * 1e-6
    
    # Find the sampling frequency (fs)
    fs = data['freq']
    
    # .ncs files have a timestamp for every ~512 data points.
    # Here, we assign timestamps for each data sample based on the sampling frequency
    # for each of the 512 data points. Sometimes a block will have fewer than 512 data entries,
    # number is set in data['valid']
    this_idx = 0
    n_block = 512.
    
    offsets = np.arange(0, n_block / fs[0], 1. / fs[0])
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
    
    # Scalar multiplication of digital values
    cscs = csc*analog_to_digital
    
    # Close file
    f.close()
    
    return cscs, t_stamps, fs
