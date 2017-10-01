#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../output/audubon_num_files.csv", parse_dates=[0])

ax = data.plot("date", ["nd6", "nd9"], style="o", ylim=[-200,4000])
ax.set_ylabel("total number of images")

plt.gcf().savefig("../output/num_files.png", clobber=True)


data["nd9_nd6"] = data["nd9"] - data["nd6"]
ax = data.plot("date", ["nd9_nd6"], style="ro", legend=False)
ax.set_ylabel("# d9 - # d6")

plt.gcf().savefig("../output/num_files_difference.png", clobber=True)
