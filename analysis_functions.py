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

def plot_tavg_power(wf_in, t=0,
                    f_start=0, f_stop=6000,
                    p_start=0, p_stop=5*10**10):

# def plot_tavg_power(wf_in, t=0,
#                     f_start=np.amin(wf_in.get_freqs()), f_stop=np.amax(wf_in.get_freqs()),
#                     p_start=0, p_stop=np.amax(wf_in.data)):
    # Plot the time-averaged power spectrum for a given blimpy waterfall object
    # wf: The desired input waterfall object
    # t: The integration number
    # f_start: Lower bound for frequency (horizontal) axis
    # f_stop: Upper bound for frequency (horizontal) axis
    # p_start: Lower bound for time-averaged power (veritcal) axis
    # p_start: Lower bound for time-averaged power (veritcal) axis

    wf_pwr_mean = np.mean(wf_in.data, axis=0)
    wf_pwr_mean_integration = wf_pwr_mean[t]
    
    print(f'Extracting integration {t}...')
    
    fig, ax = plt.subplots()
    ax.set_xlim(f_start, f_stop)
    ax.set_ylim(p_start, p_stop)
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Time-Averaged Power (???)')

    ax.plot(wf_in.get_freqs(), wf_pwr_mean_integration)
    plt.show()
    plt.close()


    

    # Based off of this code:
    # wf0_pwr = water0.data
    # print(wf0_pwr.shape)

    # wf0_pwr_mean = np.mean(data_test, axis=0)
    # print(wf0_pwr_mean, len(wf0_pwr_mean[0]))

    # wf0_pwr_mean0 = test_mean[0]
    # print(test_mean0.shape)
    # print(test_mean0)
