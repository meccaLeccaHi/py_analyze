# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

temp_name = "/home/lab/Desktop/372-021_LazerMorph/2017-03-07_12-35-46/LFPx256.ncs"

f = open(temp_name, 'rb')

# Neuralynx files have a 16kbyte header
header = f.read(2 ** 14)
header.strip(b'\x00')


# The format for a .ncs files according the the neuralynx docs is
# uint64 - timestamp in microseconds
# uint32 - channel number
# uint32 - sample freq
# uint32 - number of valid samples
# int16 x 512 - actual csc samples
dt = np.dtype([('time', '<Q'), ('channel', '<i'), ('freq', '<i'),
               ('valid', '<i'), ('csc', '<h', (512,))])
data = np.fromfile(f, dt)


# unpack the csc matrix
csc = data['csc'].reshape((data['csc'].size,))

data_times = data['time'] * 1e-6

# find the frequency
frequency = np.unique(data['freq'])
if len(frequency) > 1:
    raise IOError("only one frequency allowed")
frequency = frequency[0]

# .ncs files have a timestamp for every ~512 data points.
# Here, we assign timestamps for each data sample based on the sampling frequency
# for each of the 512 data points. Sometimes a block will have fewer than 512 data entries,
# number is set in data['valid'].
this_idx = 0
n_block = 512.
offsets = np.arange(0, n_block / frequency, 1. / frequency)
times = np.zeros(csc.shape)
for i, (time, n_valid) in enumerate(zip(data_times, data['valid'])):
    times[this_idx:this_idx + n_valid] = time + offsets[:n_valid]
    this_idx += n_valid

# now find analog_to_digital conversion factor in the header
analog_to_digital = None
for line in header.split(b'\n'):
    if line.strip().startswith(b'-ADBitVolts'):
        analog_to_digital = np.array(float(line.split(b' ')[1].decode()))

if analog_to_digital is None:
    raise IOError("ADBitVolts not found in .ncs header for " + temp_name)

cscs = csc * analog_to_digital

f.close()

#return cscs, times


row_r1 = data[1]    # Rank 1 view of the second row of a  
row_r2 = data[1:2, :]  # Rank 2 view of the second row of a
print row_r1, row_r1.
print row_r2, row_r2.shape  # Prints "[[5 6 7 8]] (1, 4)"
