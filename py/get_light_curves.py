#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import glob
import datetime
import numpy as np
import pandas as pd
import scipy.ndimage.measurements as ndm
from scipy.misc import imread

def get_filelist(st, en):
    """ Get the file list between start and end times. """

    # -- get directory list
    dirs = np.array(sorted([os.path.basename(i) for i in glob.glob( \
                    os.path.join(os.environ["AUDUBON_DATA"], "2017*_night"))]))

    # -- pull dates off of directory names
    dirt = np.array([datetime.datetime.strptime(i, "%Y-%m-%d_night") 
                     for i in dirs])

    # -- sub-select directories
    dirs = dirs[(dirt >= st) & (dirt < en)]

    # -- return the image file list
    bpath = os.environ["AUDUBON_DATA"]

    return np.array([i for j in dirs for i in 
                     glob.glob(os.path.join(bpath, j, "*d6*.png"))])


if __name__ == "__main__":

    t0  = time.time()
    
    # -- get the file list
    ind  = int(sys.argv[1])
    st    = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
    en    = datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d")
    #st    = datetime.datetime(2017, 4, 1)
    #en    = datetime.datetime(2017, 5, 1)
    flist = get_filelist(st, en)
    nobs  = flist.size
    
    
    # -- read in the bbls
    bbls  = np.rot90(np.load("../output/bbls_test.npy").astype(int))
    blist = np.sort(np.unique(bbls[bbls > 0]))
    nbbl  = len(blist)
    
    
    # -- set the ouput file name and initialize the log
    oname = os.path.join("..", "output", "light_curves_d6_{0:04}.npy" \
                             .format(ind))
    lname = os.path.join("..", "output", "light_curves_d6_{0:04}.log" \
                             .format(ind))
    lopen = open(lname, "w")
    lopen.write("Extracting lightcurves for {0} observations...\n========\n" \
                    .format(nobs))
    
    
    # -- initialize the lightcurve array
    lcs = np.zeros((nobs, nbbl), dtype=float) - 9999
    
    
    # -- loop over observations
    lopen.write("  FIX THE DIMENSIONS!!!\n")
    
    for ii, fname in enumerate(flist):
        if ii % 10 == 0:
            lopen.write("  obs {0} of {1}\n".format(ii, nobs))
            lopen.flush()
    
        # - get luminosities
        img    = imread(fname)[5::2, 1::2]
        lcs[ii] = ndm.mean(img, bbls, blist)

        # - periodically write to file
        if (ii + 1) % 100 == 0:
            np.save(oname, lcs[:ii])
    
    
    # -- write to file
    lopen.write("\nWriting to npy...\n========\n")
    lopen.flush()
    np.save(oname, lcs)
    lopen.write("FINISHED in {0}s\n".format(time.time() - t0))
    lopen.flush()
    lopen.close()

