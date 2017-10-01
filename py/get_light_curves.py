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

# if __name__ == "__main__":
#
# t0  = time.time()
# ind = int(sys.argv[1])

# -- parse the list of days
st   = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
en   = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
#st   = datetime.datetime(2017, 4, 1)
#en   = datetime.datetime(2017, 5, 1)
dirs = np.array(sorted([os.path.basename(i) for i in glob.glob( \
                os.path.join(os.environ["AUDUBON_DATA"], "2017*_night"))]))
dirt = np.array([datetime.datetime.strptime(i, "%Y-%m-%d_night") 
                 for i in dirs])
dirs = dirs[(dirt >= st) & (dirt < en)]


# -- get the image file list
fname = os.path.join("..", "data", "2017-04-09_night", 
                     "1850_d6_1491803544.png")
nobs  = 1

# -- read in the bbls
bbls = np.rot90(np.load("../output/bbls_test.npy").astype(int))

# -- read image
print("FIX THE DIMENSIONS!!!")
img = imread(fname)[5::2, 1::2]

# -- get the list of bbls
blist = np.unique(bbls[bbls > 0])

# -- get the building luminosities
lum = ndm.mean(img, bbls, blist)


brimg = np.zeros(bbls.shape)

for ii in range(blist.size):
    brimg[bbls == blist[ii]] = lum[ii]


# -- set the ouput file name and initialize the log
oname = os.path.join("..", "output", "light_curves.npy".format(ind))
lname = os.path.join("..", "output", "light_curves.log".format(ind))
lopen = open(lname, "w")
lopen.write("Extracting lightcurves for {0} observations...\n========\n" \
                .format(nobs))


# -- initialize lightcurve array
lcs  = np.zeros((nobs, nlab), dtype=float) - 9999


# -- utilities
deg2rad = np.pi / 180.
nro2    = nrow // 2
nco2    = ncol // 2


# -- initialize the rows and columns grids (the nrow//2 and ncol//2
#    performs rotation about the center of the image)
cgr, rgr = np.meshgrid(range(ncol), range(nrow))
rlabs    = rgr[srcs] - nro2
clabs    = cgr[srcs] - nco2
llabs    = labs[0][srcs]
rot      = np.zeros_like(labs[0])


# -- read in image
for ii in range(nobs):

    if ii % 10 == 0:
        lopen.write("  obs {0} of {1}\n".format(ii, nobs))
        lopen.flush()

    if reg.iloc[ii].drow == -9999:
        continue

    rot[...] = 0.
    rec      = reg.iloc[ii]
    ct       = np.cos(-rec.dtheta * deg2rad)
    st       = np.sin(-rec.dtheta * deg2rad)
    img      = read_raw(rec.fpath, rec.fname)

    # -- rotate the source labels (the nrow//2 and ncol//2 performs
    #    rotation about the center of the image)
    rsrc = (rlabs * ct - clabs * st - rec.drow + nro2).round().astype(int)
    csrc = (rlabs * st + clabs * ct - rec.dcol + nco2).round().astype(int)
    gind = (rsrc >= 0) & (rsrc < nrow) & (csrc >= 0) & (csrc < ncol)
    rsrc = rsrc[gind]
    csrc = csrc[gind]
    lsrc = llabs[gind]

    rot[rsrc, csrc] = lsrc

    # -- get brightnesses
    lun = np.unique(lsrc)
    lum = np.array([ndm.mean(img[..., i], rot, lun) for i in [0, 1, 2]]).T

    # -- set indices of extracted sources to their values
    lcs[ii, lun - 1] = lum

    # -- periodically write to file
    if (ii + 1) % 100 == 0:
        np.save(oname, lcs[:ii])

# -- write to file
lopen.write("\nWriting to npy...\n========\n")
lopen.flush()
np.save(oname, lcs)
lopen.write("FINISHED in {0}s\n".format(time.time() - t0))
lopen.flush()
lopen.close()

