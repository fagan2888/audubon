#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
View a video from the Brinno field test.
"""

import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # -- get the file name
    dfile = sys.argv[1]
    
    # -- open the file
    cap = cv2.VideoCapture(dfile)
    
    # -- determine if frames should be skipped
    skip = 0 if len(sys.argv) < 3 else int(sys.argv[2])
    
    # -- get parameters from the video
    try:
        nfrm  = int(np.round(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)))
        dum   = cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, skip)
        nrow  = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        ncol  = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    except:
        nfrm  = int(np.round(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        dum   = cap.set(cv2.CAP_PROP_POS_FRAMES, skip)
        nrow  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ncol  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # -- get the first image
    im0 = 1.0 * cap.read()[1][..., ::-1]

    # -- initialize the visualization
    xs = 8.0
    ys = xs * float(nrow) / float(ncol)
    fig, ax = plt.subplots(figsize=(xs, ys))
    fig.subplots_adjust(0, 0, 1, 1)
    ax.axis("off")
    im  = ax.imshow(np.zeros((nrow, ncol, 3), dtype=np.uint8))
    frt = ax.text(ncol - 0.09 * ncol, nrow - 0.05 * nrow, "frame:", 
                  color="white", fontsize=14, ha="right")
    txt = ax.text(ncol - 0.025 * ncol, nrow - 0.05 * nrow, "{0}".format(0), 
                  color="white", fontsize=14, ha="right")
    fig.canvas.draw()
    plt.ion()
    plt.show()
    
    # -- run through the frames
    for ii in range(1, nfrm - skip):
        im1  = 1.0 * cap.read()[1][..., ::-1]
        diff = (im1 - im0).clip(0, 255).astype(np.uint8)
        im0  = im1.copy()
        im.set_data(diff)
        txt.set_text("{0}".format(ii + skip))
        fig.canvas.draw()
        plt.pause(1e-5)
