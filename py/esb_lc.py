#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import numpy as np
import pandas as pd
from utils import get_bbls


# -- read in the file times
print("reading file times...")
tfile = os.path.join("..", "output", "april_file_list.csv")
times = pd.read_csv(tfile, parse_dates=["datetime"])


# -- read in the light curves
print("reading light curves...")
lcs = np.vstack([np.load(os.path.join("..", "output", 
                                      "light_curves_d6G_sort_{0:04}.npy" \
                                          .format(i))) for i in range(6)])

# -- get BBLs
bbls, blist, nbbl = get_bbls()

# -- pull off esb
esb   = 1008350041
eind, = np.where(blist == esb)
lce   = lcs[:, eind]

# -- pull off each day
days = [i % 30 + 1 for i in range(31)]
mons = [4] * 30 + [5]
stb  = "2017-{0:02}-{1:02} 21:00:00"
enb  = "2017-{0:02}-{1:02} 06:00:00"
form = "%Y-%m-%d %H:%M:%S"

dinds    = []
times_dy = []
lce_dy   = []

for ii in range(len(days) - 1):
    st = datetime.datetime.strptime(stb.format(mons[ii], days[ii]), form)
    en = datetime.datetime.strptime(enb.format(mons[ii+1], days[ii+1]), form)

    dind = (times.datetime >= st) & (times.datetime <= en)

    dinds.append(dind)
    times_dy.append(times.datetime[dind].values)
    lce_dy.append(lce[dind, 0])
