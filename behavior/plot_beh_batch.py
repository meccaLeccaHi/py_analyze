# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 13:25:15 2017

@author: root
"""

import numpy as np
#import matplotlib.pyplot as plt
#import plotly.plotly as py
from matplotlib import pyplot
import os, csv, glob, sys

main_dir = "/home/lab/Cloud2/movies/human/LazerMorph/"
header_dir = main_dir+"headers/"
fig_dir = main_dir+"py_analyze/behavior/figs/"
exp_dir = main_dir+"py_stimuli/expEyeTrack/"

sys.path.insert(0, exp_dir)
from plot_beh import plot_beh


#header_list = glob.glob(header_dir + '*')
#
#header_list = header_list[0:3]

header_files = ["hdr02162017_1833","hdr02162017_1825","hdr02162017_1821",
"hdr02162017_1818","hdr02162017_1815","hdr02162017_1811"][::-1]
header_list = [header_dir+x+".csv" for x in header_files]

fig = pyplot.figure(facecolor='black')     
for H_i, H_nm in enumerate(header_list):
    
    f_names = []
    correct = []
    f_nm = os.path.split(H_nm)[1]
    f = open(H_nm, 'rb')
    try:
        reader = csv.reader(f)
        for row in reader:
            f_names.append(row[2])
            
            if row[9].isdigit():
                correct.append(int(row[9]))
            else:
                correct.append(None)
    finally:
        f.close()   
    
    # Extract identity numbers from video list
    ident_ind = f_names[0].find("identity") + len("identity")
    #IDENT_LIST = np.unique([x[ident_ind] for x in f_names],return_inverse = True)[1]
    
    # Correct identity # for faces more than 50% along tang. trajectory
    TRAJ_LIST = np.unique([x[ident_ind+1:ident_ind+4] for x in f_names],return_inverse = True)[1]
    STEP_LIST = np.unique([x[ident_ind+5:ident_ind+8] for x in f_names],return_inverse = True)[1]
    # ['025', '050', '075', '100', 'd.a', 'ly.']
    
    plt = plot_beh(STEP_LIST, TRAJ_LIST, correct)
    plt.savefig(filename = (fig_dir + "beh_fig_foo" + f_nm[0:-4] + ".png"), dpi=100,transparent=True)
    
    plt.close()