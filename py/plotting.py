#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gp
from scipy.misc import imread
from utils import *

def see_images(flist):
    """ View a list of images. """

    cnt = [0]

    def next_img(event):
        if event.key == "right":
            cnt[0] += 1
        elif event.key == "left":
            cnt[0] -= 1

        cnt[0] %= len(flist)
        im.set_data(np.rot90(imread(flist[cnt[0]]), 3)[1::2, 1::2])
        tt.set_text("{0} : {1}".format(cnt[0], flist[cnt[0]]))
        fig.canvas.draw()

        return

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")
    im = ax.imshow(np.rot90(imread(flist[cnt[0]]), 3)[1::2, 1::2], 
                   clim=[0, 50])
    tt = ax.set_title("{0} : {1}".format(cnt[0], flist[cnt[0]]))
    fig.canvas.draw()
    fig.canvas.mpl_connect("key_press_event", next_img)

    return


def plot_visible():
    """ Plot the visible buildings. """

    # -- get the bbls
    print("reading BBLs...")
    bbls, blist, nbbl = get_bbls()

    # -- get mappluto
    print("reading MapPLUTO...")
    mp = gp.read_file(os.path.join("..", "data", "mappluto", "MN", 
                                   "MNMapPLUTO.shp"))

    # -- get the subset of viewable buildings
    sub = mp[mp.BBL.isin(blist)]

    # -- get the borough boundaries
    boro = gp.read_file(os.path.join("..", "data", "nyc_shp", "nybb.shp"))

    # -- read in the audubon buildings
    volbld = pd.read_csv(os.path.join("..", "data", "Audubon_buildings.csv"))
    asub   = mp[mp.BBL.isin(volbld[" BBL"])]


    close("all")
    fig, ax = plt.subplots()
    ax.axis("off")
    fig.set_facecolor("#111111")
    fig.canvas.draw()
    base = boro.plot(edgecolor="k", color="#222222", lw=0.5, ax=ax)
    mp.plot(color="#222222", edgecolor="w", ax=ax, lw=0.1)
    sub.plot(color="khaki", edgecolor="w", ax=ax, lw=0.1)
    ax.scatter(asub.centroid.x, asub.centroid.y, lw=0, color="crimson")
    subplots_adjust(0, 0, 1, 1)
