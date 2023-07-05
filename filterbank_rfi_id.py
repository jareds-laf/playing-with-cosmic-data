import matplotlib
import matplotlib.pyplot as plt
import pylab as plt
import blimpy
from blimpy import Waterfall
from blimpy import calcload
import os
import glob
import numpy as np
import time
from scipy.stats import norm, kurtosis, kurtosistest
import scipy
import numpy.ma as ma
import seaborn as sns

import sys
file_path = '/lustre/aoc/students/jsofair/playing-with-cosmic-data/filterbank/'
sys.path.insert(1, file_path[:54])
from analysis_functions import plot_tavg_power


file_list = glob.glob(os.path.join(file_path,'*.fil'))

ml_list = []
for i, file in enumerate(file_list):
    ml = blimpy.calcload.calc_max_load(os.path.join(file))
    ml_list.append(ml)
    print(f'{ml} -- {file[65:]}')


water0 = Waterfall(os.path.normpath(file_list[0]), max_load = ml_list[0])
water1 = Waterfall(os.path.normpath(file_list[1]), max_load = ml_list[1])
water2 = Waterfall(os.path.normpath(file_list[2]), max_load = ml_list[2])
water3 = Waterfall(os.path.normpath(file_list[3]), max_load = ml_list[3])
water4 = Waterfall(os.path.normpath(file_list[4]), max_load = ml_list[4])
water5 = Waterfall(os.path.normpath(file_list[5]), max_load = ml_list[5])
water6 = Waterfall(os.path.normpath(file_list[6]), max_load = ml_list[6])

water_list = [water0, water1, water2, water3, water4, water5, water6]

for wf in water_list:
	plot_tavg_power(wf)
