#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import numpy as np
from scipy.misc import imread, imsave
from utils import *

# -- get the file list
print("reading file times...")
tfile = os.path.join("..", "output", "april_file_list.csv")
times = pd.read_csv(tfile, parse_dates=["datetime"])

# -- select April 1st
st  = datetime.datetime.strptime("2017-04-01 21:00:00", "%Y-%m-%d %H:%M:%S")
en  = datetime.datetime.strptime("2017-04-02 06:00:00", "%Y-%m-%d %H:%M:%S")
ind = (times.datetime >= st) & (times.datetime <= en)
sub = times[ind]

# -- convert to jpg
ntime = len(sub)
for ii in range(ntime):
    if (ii + 1) % 100 == 0:
        print("{0} of {1}".format(ii + 1, ntime))

    img  = imread(sub.iloc[ii].filename)
    red  = img[::2, ::2]
    grn0 = img[::2, 1::2]
    grn1 = img[1::2, ::2]
    blu  = img[1::2, 1::2]
    rgb  = np.rot90(np.dstack((red, 0.5 * grn0 + 0.5 * grn1, blu)) * 5.0, 3) \
        .clip(0, 255).astype(np.uint8)

    imsave(os.path.join("..", "output", "jpgs", "2017-04-01_night", 
                        "{0:06}_imgRGB.jpg".format(ii)), rgb)


