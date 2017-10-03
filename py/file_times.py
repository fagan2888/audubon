#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
from utils import *

# -- get the file list
st    = datetime.datetime.strptime("2017-04-01", "%Y-%m-%d")
en    = datetime.datetime.strptime("2017-05-01", "%Y-%m-%d")
flist = get_filelist(st, en)


# -- for each file, pull off the time from the filename
ts = np.array([int(i.split("_")[-1].split(".")[0]) for i in flist])


# -- sort by timestamp
sind  = ts.argsort()
flist = flist[sind]
ts    = ts[sind]


# -- convert to datetime
dt = np.array([datetime.datetime.fromtimestamp(i) for i in ts])


# -- write to csv
fopen = open(os.path.join("..", "output", "april_file_list.csv"), "w")
fopen.write("filename,datetime\n")

for ii in range(dt.size):
    fopen.write("{0},{1}-{2:02}-{3:02} {4:02}:{5:02}:{6:02}\n" \
                    .format(flist[ii], dt[ii].year, dt[ii].month, dt[ii].day, 
                            dt[ii].hour, dt[ii].minute, dt[ii].second))

fopen.close()
