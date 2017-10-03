#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import datetime
import numpy as np



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


