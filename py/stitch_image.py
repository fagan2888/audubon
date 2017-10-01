#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

def read_image(fname, k):

    # -- utilities
    nrow = 3840
    ncol = 5120

    # -- read the image
    raw = np.fromfile(fname, np.uint8).reshape(nrow, ncol)

    return np.rot90(np.dstack((raw[::2, ::2], raw[1::2, ::2], 
                               raw[1::2, 1::2])), k)


# -- set the input files
#fname0 = os.path.join("..", "data", "durst", "00000000_000000000014B515.bin")
#fname1 = os.path.join("..", "data", "durst", "00000000_0000000000153562.bin")

fname0 = os.path.join("..", "data", "durst", "d6_n1000000.raw")
fname1 = os.path.join("..", "data", "durst", "d9_n1000000.raw")

# -- read the images
img0 = read_image(fname0, 3)
img1 = read_image(fname1, 1)

# -- stitch images
img = np.hstack((img0[:-13, :1745], img1[13:, 641:]))

# -- make image
xs = 10.
ys = xs * float(img.shape[0]) / float(img.shape[1])
fig, ax = plt.subplots(figsize=(xs, ys))
fig.subplots_adjust(0, 0, 1, 1)
ax.axis("off")
im = ax.imshow((255*np.sqrt(1.0*img/255.)).astype(np.uint8))
fig.canvas.draw()
fig.savefig(os.path.join("..", "output", "first_night_durst.png"), 
            clobber=True)
#fig.savefig(os.path.join("..", "output", "fist_light_durst.png"), 
#            clobber=True)


# 1138, 1745
# 1151, 641
