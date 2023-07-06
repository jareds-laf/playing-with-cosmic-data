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

def plot_tavg_power(wf_in,
                    f_start=0, f_stop=6000,
                    p_start=0, p_stop=5*10**10, find_inf=False, n_divs=0):

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
    wf_pwr_mean_integration = wf_pwr_mean[0]
    
    if find_inf == True:
        # Get power and frequency in increasing order
        if wf_in.header['foff'] < 0:
            pows_flipped = np.flip(wf_in.data)
            freqs_flipped = wf_in.get_freqs()[::-1]

        # Time-average the power
        pows_mean_flipped = np.mean(pows_flipped, axis=0)[0]    

        # Split frequency and time-averaged power into n_divs channels
        freqs = np.array_split(freqs_flipped, n_divs)
        pows_mean = np.array_split(pows_mean_flipped, n_divs)

        # Find kurtosis of each channel
        kurts_list = []
        for i, division in enumerate(pows_mean):
            kurts_list.append(kurtosis(division))

        kurts = np.array(kurts_list, dtype=np.float64)

        # Bin frequencies
        bins = []
        for chnl in freqs:
            bins.append(np.floor(chnl[0]))
        

        # Plot time-averaged power with frequencies of infinite kurtosis flagged
        fig, ax = plt.subplots()
        ax.set_xlim(f_start, f_stop)
        ax.set_ylim(p_start, p_stop)
        ax.set_xlabel('Frequency (MHz)')
        ax.set_ylabel('Time-Averaged Power (Counts)')

        ax.plot(wf_in.get_freqs(), wf_pwr_mean_integration)
        
        # Find where kurtosis is inf and plot these channels
        inf_kurt = np.where(np.isfinite(kurts) == False)

        inf_kurts = []
        for i in inf_kurt[0]:
            inf_kurts.append(bins[i])
            plt.axvline(x=bins[i], ymin=0, ymax=10, c='r', ls='--')

        plt.show()
    else:
        # Plot time-averaged power only
        fig, ax = plt.subplots()
        ax.set_xlim(f_start, f_stop)
        ax.set_ylim(p_start, p_stop)
        ax.set_xlabel('Frequency (MHz)')
        ax.set_ylabel('Time-Averaged Power (Counts)')

        ax.plot(wf_in.get_freqs(), wf_pwr_mean_integration)
        plt.show()

    

    # Based off of this code:
    # wf0_pwr = water0.data
    # print(wf0_pwr.shape)

    # wf0_pwr_mean = np.mean(data_test, axis=0)
    # print(wf0_pwr_mean, len(wf0_pwr_mean[0]))

    # wf0_pwr_mean0 = test_mean[0]
    # print(test_mean0.shape)
    # print(test_mean0)