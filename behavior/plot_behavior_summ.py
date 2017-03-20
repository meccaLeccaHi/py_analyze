# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:17:50 2017

@author: root
"""

import numpy as np
#import matplotlib.pyplot as plt
#import plotly.plotly as py
from matplotlib import pyplot
import csv, sys #, glob

main_dir = "/home/lab/Cloud2/movies/human/LazerMorph/"
header_dir = main_dir+"headers/"
fig_dir = main_dir+"py_analyze/behavior/figs/"
exp_dir = main_dir+"py_stimuli/expEyeTrack/"

sys.path.insert(0, exp_dir)
from plot_beh import plot_beh

#header_list = glob.glob(header_dir + '*')
#
#header_list = header_list[0:3]

#header_files = ["hdr03072017_1244","hdr03092017_1025",
#"hdr03092017_1032"] # "hdr03072017_1229",

header_files = ["hdr02162017_1833","hdr02162017_1825","hdr02162017_1821",
"hdr02162017_1818","hdr02162017_1815","hdr02162017_1811"][::-1]

header_list = [header_dir+x+".csv" for x in header_files]

col_steps = 255/(len(header_list)+1)

fig = pyplot.figure(facecolor='black')     
for H_i, H_nm in enumerate(header_list):
    
    f_names = []
    correct = []
    f = open(H_nm, 'rb')
    try:
        reader = csv.reader(f)
        for row in reader:
            f_names.append(row[2])
            correct.append(row[9])
    finally:
        f.close()
    
    # Extract identity numbers from video list
    ident_ind = f_names[0].find("identity")+len("identity")
    #IDENT_LIST = np.unique([x[ident_ind] for x in f_names],return_inverse = True)[1]
    
    # Correct identity # for faces more than 50% along tang. trajectory
    TRAJ_LIST = np.unique([x[ident_ind+1:ident_ind+4] for x in f_names],return_inverse = True)[1]
    STEP_LIST = np.unique([x[ident_ind+5:ident_ind+8] for x in f_names],return_inverse = True)[1]
    # ['025', '050', '075', '100', 'd.a', 'ly.']
    
#    np.asarray(f_names)[np.where(STEP_LIST>3)]
#    np.asarray(correct)[np.where(STEP_LIST>3)]
    
    foo = np.asarray(correct)[np.where(STEP_LIST>3)]
    rad_results = [np.mean(map(int, foo[foo!='']))]
    for i in range(4):
        foo = np.asarray(correct)[np.where((TRAJ_LIST==1)&(STEP_LIST==i))]
        rad_results.append(np.mean(map(int, foo[foo!=''])))
       
#    np.asarray(f_names)[np.where((TRAJ_LIST==2)&(STEP_LIST==i))]
    tan_results = []
    for i in range(3):
        foo = np.asarray(correct)[np.where((TRAJ_LIST==2)&(STEP_LIST==i))]
        tan_results.append(np.mean(map(int, foo[foo!=''])))
    
    foo = np.asarray(correct)[np.where((TRAJ_LIST==1)&(STEP_LIST==3))]
    tan_results.append(np.mean(map(int, foo[foo!=''])))
    
    
    x1 = np.asarray(rad_results)*100
    x2 = np.asarray(tan_results)*100
    
#    pyplot.clf()
    ax1 = pyplot.subplot(1,2,1,axisbg='k')
    x = np.asarray(range(len(x1)))/(len(x1)-1.0)*100
    pyplot.plot(x,np.tile(25.0,(1,len(x)))[0],'--',color='grey',lw=2)
    pyplot.plot(x,x1,color=pyplot.cm.hot((H_i+1)*col_steps),lw=2)
    pyplot.ylim([0,100])
    pyplot.xticks(x)
    pyplot.xlabel('% identity')
    pyplot.ylabel('% correct')
    pyplot.title('Radial traj.')
    
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_linewidth(0.5)
    ax1.spines['left'].set_linewidth(0.5)
    ax1.spines['bottom'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.title.set_color('white')
    ax1.yaxis.label.set_color('white')
    ax1.xaxis.label.set_color('white')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    
    ax2 = pyplot.subplot(1,2,2,axisbg='k')
    x = np.asarray(range(1,len(x2)+1))/float(len(x2))*100
    pyplot.plot(x,np.tile(25.0,(1,len(x)))[0],'--',color='grey',lw=2)
    pyplot.plot(x,x2,color=pyplot.cm.hot((H_i+1)*col_steps),lw=2)
    pyplot.ylim([0,100])
    pyplot.xticks(x)
    pyplot.xlabel('% identity')
    pyplot.title('Tang traj.')

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_linewidth(0.5)
    ax2.spines['left'].set_linewidth(0.5)
    ax2.spines['bottom'].set_color('white')
    ax2.spines['left'].set_color('white')
    ax2.title.set_color('white')
    ax2.yaxis.label.set_color('white')
    ax2.xaxis.label.set_color('white')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')    
    
pyplot.savefig(filename=(fig_dir + "beh_fig_summ.png"),
               facecolor=fig.get_facecolor(),transparent=True)
    
pyplot.close()
