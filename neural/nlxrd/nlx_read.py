# -*- coding: utf-8 -*-

import numpy as np
 
def nlx_read(nlx_filename):
    """    
    Loads data stored in the formats used by the Neuralynx recording systems
                                                                                   
    Converts binary Neuralynx data files to decimal form,
    then applies analog-to-digital conversion factor

    The format for a continuously-sampled channel file (.ncs) file:
        uint64 - timestamp in microseconds
        uint32 - channel number
        uint32 - sample freq
        uint32 - number of valid samples
        int16 x 512 - actual csc samples
        
    The format for an event record (.nev) file:
        int16 - nstx - reserved
        int16 - npkt_id - id of the originating system
        int16 - npkt_data_size - this value should always be 2
        uint64 - timestamp, microseconds
        int16 - nevent_id - ID value for event
        int16 - nttl - decimal TTL value read from the TTL input port
        int16 - ncrc - record crc check, not used in consumer applications
        int16 - ndummy1 - reserved
        int16 - ndummy2 - reserved
        int32x8 - dnExtra - extra bit values for this event
        string(128) - event string
        
    For more info on Neuralynx file formats:
    http://neuralynx.com/techtips/TechTip_mar_2015.html   
    http://neuralynx.com/research_software/development_software/
                                            
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
    nlx_filename = "/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/Events.nev"
    [t_stamps, event_id, ttl, event_str] = nlx_read(nlx_filename)  
    """
    
    def load_ncs(nlx_filename):
        """Loads a neuralynx .ncs file.
        Returns
        -------
        - cscs (float64)
        - t_stamps (float64)
        - fs (int32)
        Usage
        -----
        [cscs, t_stamps, fs] = loadNev('Events.nev')
        """
        # Open file
        f = open(nlx_filename, 'rb')
    
        # Neuralynx files have a 16kbyte header
        header = str(f.read(2 ** 14)).strip('\x00')
        
        dt = np.dtype([('time', '<Q'), ('channel', '<i'), ('freq', '<i'),
                       ('valid', '<i'), ('csc', '<h', (512,))])
        data = np.fromfile(f, dt)
        
        # Close file
        f.close()
        
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
        
        return cscs, t_stamps, fs
    
    def load_nev(nlx_filename):
        """Loads a neuralynx .nev file.
        Returns four numpy arrays:
        - t_stamps (uint64)
        - event_id (int16)
        - ttl (int16)
        - event_str (string)
        [t_stamps, event_id, ttl, event_str] = loadNev('Events.nev')
        """
        # Open file
        f = open(nlx_filename, 'rb')
        
        # There's nothing useful in the header for .nev files, so skip past it
        f.seek(2 ** 14)
        
        dt = np.dtype([('filler1', '<h', 3), ('time', '<Q'), ('id', '<h'),
                       ('nttl', '<h'), ('filler2', '<h', 3), ('extra', '<i', 8),
                       ('estr', np.dtype('a128'))])
        data = np.fromfile(f, dt)
        
        # Close file
        f.close()
        
        return data['time'], data['id'], data['nttl'], data['estr']
    
    print(nlx_filename)

    # Process each file type differently
    if(nlx_filename.find('.ncs')>0): 
        return load_ncs(nlx_filename)
    elif(nlx_filename.find('.nev')>0):
        return load_nev(nlx_filename)
    else:
        print('Incorrect file type. Needs either .ncs or .nev file(s)')

    
