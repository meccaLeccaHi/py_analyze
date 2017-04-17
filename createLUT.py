# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:03:56 2017

@author: lab
"""

"""
Create LazerMorph LUT
"""

import pandas as pd
import numpy as np
import csv, os

# Read header file
header_dir = '/home/lab/Cloud2/movies/human/LazerMorph/headers/'
header_fname = header_dir+'hdr03072017_1244.csv'
# hdr03072017_1229

df = pd.read_csv(header_fname,header=None)

sort_indices = np.argsort(df[1])

stimid = np.asarray(df[1])[sort_indices]-1
stim_fname = np.asarray(df[2])[sort_indices]

f = open(header_dir+'lazermorphLUT.csv', 'wt')
try:
    writer = csv.writer(f, quoting=csv.QUOTE_NONE)
    writer.writerow( ('StimID','filename','identity','level','traj','stim_modality') )
    for i in range(len(stimid)):
        # Extract stim params from each stim name
        fname = os.path.basename(stim_fname[i])
        
        ident_ind = fname.find('identity')
        if(ident_ind==-1):
            ident_num = 0
            ident_lev = 0
            ident_traj = None
        else:
            ident_num = int(fname[ident_ind+len('identity')])
            ident_lev = int(fname[fname.find('_')+1:fname.find('_')+4])
            ident_traj = fname[ident_ind+9:ident_ind+12]
        
        stim_mode = fname[max(map(fname.find, ['audOnly', 'visOnly', 'audVid'])):-4]

        writer.writerow((stimid[i],fname,ident_num,ident_lev,ident_traj,stim_mode))
finally:
    f.close()