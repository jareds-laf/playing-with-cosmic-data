import pylab as plt
import blimpy
from blimpy import Waterfall
from blimpy import calcload
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.stats import norm, kurtosis, kurtosistest
import numpy.ma as ma
import seaborn as sns

file_path = '/lustre/aoc/students/jsofair/filterbank/'
filelist = glob.glob(os.path.join(file_path,'*.fil'))

ml_list = []
for i, file in enumerate(filelist):
    ml = blimpy.calcload.calc_max_load(os.path.join(file))
    ml_list.append(ml)
    print(f'{ml} -- {file[40:]}')

t0 = time.time()
water0 = Waterfall(os.path.normpath(filelist[0]), max_load = ml_list[0])
water1 = Waterfall(os.path.normpath(filelist[1]), max_load = ml_list[1])
water2 = Waterfall(os.path.normpath(filelist[2]), max_load = ml_list[2])
water3 = Waterfall(os.path.normpath(filelist[3]), max_load = ml_list[3])
water4 = Waterfall(os.path.normpath(filelist[4]), max_load = ml_list[4])
water5 = Waterfall(os.path.normpath(filelist[5]), max_load = ml_list[5])

water_list = [water0, water1, water2, water3, water4, water5]
t1 = time.time()
print(f'Elapsed time: {t1 - t0}')

all_channels = []

# Specify the number of channels to break each .fil file into
num_chnls = 100000
# print(len(water_list))

for i in range(0, len(water_list)):
#     print('h')
    exec(f'all_channels.append(np.array_split(water{i}.get_freqs(), {num_chnls}))')




print(kurtosis(all_channels[0][0]),
np.amax(all_channels[0][0]),
np.amin(all_channels[0][0]))



kurts = []

for i, chnl in enumerate(all_channels[0]):
    kurts.append(kurtosis(chnl))
