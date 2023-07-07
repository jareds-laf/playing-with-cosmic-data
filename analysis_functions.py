import matplotlib
import matplotlib.pyplot as plt
import pylab as plt
import blimpy
from blimpy import Waterfall
import glob
import numpy as np
import time
from scipy.stats import norm, kurtosis, kurtosistest
import scipy

def plot_tavg_power(wf_in,
                    f_start=0, f_stop=6000,
                    p_start=0, p_stop=5*10**10, n_divs=0):
    # Plot the time-averaged power spectrum for a given blimpy waterfall object
    # wf: The desired input waterfall object
    # t: The integration number
    # f_start: Lower bound for frequency (horizontal) axis
    # f_stop: Upper bound for frequency (horizontal) axis
    # p_start: Lower bound for time-averaged power (veritcal) axis
    # p_start: Lower bound for time-averaged power (veritcal) axis

    wf_pwr_mean = np.mean(wf_in.data, axis=0)
    wf_pwr_mean_integration = wf_pwr_mean[0]
    
   
    # Plot time-averaged power
    fig, ax = plt.subplots()
    ax.set_xlim(f_start, f_stop)
    ax.set_ylim(p_start, p_stop)
    
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Time-Averaged Power (Counts)')

    ax.plot(wf_in.get_freqs(), wf_pwr_mean_integration)