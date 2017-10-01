#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from scipy.misc import imsave

def read_image(fname, k):

    # -- utilities
    nrow = 3840
    ncol = 5120

    # -- read the image
    raw = np.fromfile(fname, np.uint8).reshape(nrow, ncol)

    return np.rot90(np.dstack((raw[::2, ::2], raw[1::2, ::2],
                               raw[1::2, 1::2])), k)


# -- read in the images
fnamel = os.path.join("..", "data", "durst", "d6_day_300.raw")
fnamer = os.path.join("..", "data", "durst", "d9_day_600.raw")
imgl   = read_image(fnamel, 3)
imgr   = read_image(fnamer, 1)


# -- gray world
scll  = imgl.mean((0, 1))
scll /= scll.min()
imgl  = imgl.astype(float) / scll

sclr  = imgr.mean((0, 1))
sclr /= sclr.min()
imgr  = imgr.astype(float) / sclr


# -- gamma correct
img    = np.hstack((imgl, imgr))
imgg   = (255 * (img / 255.)**0.75).clip(0, 255).astype(np.uint8)


# -- make the image
imsave(os.path.join("..", "output", "example_day_images.png"), imgg)
