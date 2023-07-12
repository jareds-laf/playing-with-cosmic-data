import matplotlib
import matplotlib.pyplot as plt
import pylab as plt
import blimpy
from blimpy import Waterfall
import glob
import numpy as np
from scipy.stats import norm, kurtosis
import scipy

def get_tavg_kurtosis(wf_in, n_divs=256):
    # This function grabs the kurtosis of channels of a specified size for a blimpy waterfall object
    
    # wf_in: Specified blimpy waterfall object
    # n_divs: Number of divisions to break wf_in into
        # 32 is the correct number of channels to break a waterfall into assuming the frequency range
        # of the waterfall is 32 MHz
        
    np.set_printoptions(threshold=4)

    # Get power and frequency in increasing order
    if wf_in.header['foff'] < 0:
        pows_flipped = np.flip(wf_in.data)
        freqs_flipped = wf_in.get_freqs()[::-1]
    
    # Time-average the power
    pows_mean_flipped = np.mean(pows_flipped, axis=0)[0]    

    # Split frequency and time-averaged power into n_divs channels
    freqs = np.array_split(freqs_flipped, n_divs)
    pows_mean = np.array_split(pows_mean_flipped, n_divs)
    
    # Get kurtosis of all channels
    kurts_list = []
    
    for i, division in enumerate(pows_mean):
        kurts_list.append(kurtosis(division/(10**9))) # Rescaling data so that kurtosis != inf ever

    kurts = np.array(kurts_list, dtype=np.float64)
    
    # Check to see if any of the kurtoses are infinite
    if np.any(np.isfinite(kurts)) == False:
        print(f'Infinite kurtoses located at indices {np.where(np.isfinite(kurts) == False)}')
    
    
    # Binning frequencies such that the labeled frequency is the bottom of the bin
    # i.e., if chnl[0] is 2010 MHz and each channel is 1 MHz, then the bin from 2010 MHz to 2010.99 MHz will have
    # a value of "2010"
    bins = []
    for chnl in freqs:
        bins.append(chnl[0])

    # bins: All frequency bins for the frequency range of the waterfall
    # kurts: Kurtosis of all frequency bins
        
    return bins, kurts



def plot_tavg_kurtosis(wf_in, n_divs=256):
    # This function plots the kurtosis of the time-averaged power spectrum.
    # For info on inputs, see get_tavg_kurtosis() function definition.
    
    # Get bin and kurtosis information
    bins, kurts = get_tavg_kurtosis(wf_in, n_divs)
    
    # Plot kurtosis vs. frequency
    fig, ax = plt.subplots()
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Kurtosis')
    
    ax.plot(bins, kurts, '.')
    

def get_mask_kurtosis(wf_in, n_divs=256, threshold=50):
    # This function flags bins with high kurtosis (i.e., heavy RFI) and returns the necessary information about
    # these bins.
    # wf_in: See get_tavg_kurtosis() function definition
    # n_divs: See get_tavg_kurtosis() function definition
    # threshold: Minimum kurtosis for a channel to be flagged as 'RFI-heavy'
    
    # TODO: Decide whether or not you wanna split this into one function that just returns the flagged and masked
    # bins/kurtoses and another function that returns the mask
    
    # Get bin and kurtosis information
    bins, kurts = get_tavg_kurtosis(wf_in, n_divs)
    
    # masked_kurts is an array that has all channels with |kurtosis| > threshold masked out
    masked_kurts = ma.masked_where(np.abs(kurts) > threshold, kurts)
    bin_mask = ma.getmask(masked_kurts)
    
    # flagged_bins is an array that has the frequencies of the channels with kurtosis > threshold NOT masked out
    # flagged_kurts masks the opposite elements as masked_kurts (i.e., it contains all of the kurtoses of the
    # high RFI channels)
    flagged_bins = ma.masked_array(bins, mask=~bin_mask)
    flagged_kurts = ma.masked_array(kurts, mask=~bin_mask)
    
    # The reason I am no longer using ma.count(masked_array) is because there can be an error where masked elements
    # are converted to NaNs.
    print(f'{len(np.where(bin_mask == True)[0])} out of {n_divs} channels flagged as having substantial RFI')
    
    # TODO: Grab mask that contains the frequencies with high RFI, not the frequency *bins*!
    # Get frequency in increasing order, first
    if wf_in.header['foff'] < 0:
        freqs_flipped = wf_in.get_freqs()[::-1]
        freqs = ma.masked_array(freqs_flipped)
    
    # Bin width...?
    # There are 7 Hz in between each entry of freqs, and 32 MHz total
    # Given a total of 4194304 elements in freqs, if there are 256 bins, then each bin spans 16384 elements
    # If each bin spans 16384 elements, then it spans 125 kHz (125 kHz * 256 = 32 MHz)
    full_freq_range = freqs[-1] - freqs[0]
    bin_width = bin_width = full_freq_range / n_divs # This is the bin width in terms of MHz
    
    bin_width_elements = int(np.floor(len(freqs) / n_divs)) # This is the bin width in terms of the number of elements in freqs
    
#     print(f'bin width: {bin_width}')
    
    masked_freqs = ma.masked_array(freqs)
    
    for rfi_bin in flagged_bins:
        try:
            # Get the frequency indices of the masked frequency bins and put them in a list
            xmin = np.where(freqs == rfi_bin)[0][0]
            xmax = xmin + bin_width_elements
            masking_indices = np.arange(xmin, xmax)
#             print(len(masking_indices))
            
            # Create a masked array that masks the indices of the high RFI bins
            masked_freqs[masking_indices] = ma.masked
            freq_mask = ma.getmask(masked_freqs)
        except:
            pass
    
#     print(f'Some bins to be masked: {flagged_bins}')
#     print(masked_freqs)
#     print(ma.count(masked_freqs))
#     print(freq_mask)
#     maskie = freqs == masked_freqs
    
#     print(freqs[maskie])
    
#     freq_mask = []
#     for rfi_freq in masked_freqs:
#         maskie = freqs == rfi_freq

#         masked_freqs_indices = np.concatenate(masked_freqs_indices, np.where(rfi_freq == freqs)[0])
        
    # Summary of returned variables:
    # flagged_bins: Channels with high kurtosis (i.e., high RFI)
    # flagged_kurts: Kurtosis of each channel that was flagged as having high RFI
    # masked_kurts: Kurtosis of all 'clean' (low RFI) channels with high RFI channels masked out
    # bin_mask: The mask used to generate masked_kurts -- Masks the frequency *bins*
    # freq_mask: A mask to be used to block out the *actual* frequencies, rather than the frequency *bins*
    return flagged_bins, flagged_kurts, masked_kurts, bin_mask, freq_mask


def plot_mask_kurtosis(wf_in, n_divs=256, threshold=50, unfiltered=True, clean_chnls=True, rfi=False,
                      f_start=0, f_stop=0, k_start=0, k_stop=0):
    # This function plots the kurtosis of each frequency channel for a specified waterfall object.
    # wf_in: See get_tavg_kurtosis() function definition
    # n_divs: See get_tavg_kurtosis() function definition
    # threshold: See get_mask_kurtosis() function definition
    # unfiltered: If true, plot the data before any RFI filtering has occurred
    # clean_chnls: If true, plot the data after RFI has been filtered out
    # rfi: If true, plot the channels that have been marked as RFI
    
    bins, kurts = get_tavg_kurtosis(wf_in, n_divs)
    flagged_bins, flagged_kurts, masked_kurts, bin_mask, freq_mask = get_mask_kurtosis(wf_in, n_divs, threshold)
    
    fig, ax = plt.subplots()
    
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Kurtosis')
    
    if unfiltered:
        ax.plot(bins, kurts, 'o', c='#4287f5', label='Unfiltered data') # Color is a nice blue
    if clean_chnls:
        ax.plot(bins, masked_kurts, '.', c='#43cc5c', label='Clean channels') # Color is a nice green
    if rfi:
        ax.plot(flagged_bins, flagged_kurts, '.', c='red', label='Heavy RFI') # Color is red
    
    if np.any([f_start, f_stop, k_start, k_stop]) != 0:
        ax.set_xlim(f_start, f_stop)
        ax.set_ylim(k_start, k_stop)
    
        ax.legend(fancybox=True,shadow=True, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncols=3)
    else:
        ax.legend(fancybox=True,shadow=True, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncols=3)


def plot_tavg_power(wf_in,
                    f_start=0, f_stop=6000,
                    p_start=0, p_stop=5*10**10, n_divs=256, threshold=50,
                    show_filtered_bins=True):
    # Plot the time-averaged power spectrum for a given blimpy waterfall object
    # wf: The desired input waterfall object
    # t: The integration number
    # f_start: Lower bound for frequency (horizontal) axis
    # f_stop: Upper bound for frequency (horizontal) axis
    # p_start: Lower bound for time-averaged power (veritcal) axis
    # p_start: Lower bound for time-averaged power (veritcal) axis
    # show_filtered: If true, draw a red box where high RFI channels are

    # Time average the power
    wf_pwr_mean = np.mean(wf_in.data, axis=0)
    wf_pwr_mean_integration = wf_pwr_mean[0]
   
    # Plot time-averaged power
    fig, ax = plt.subplots()
    
    ax.set_xlim(f_start, f_stop)
    ax.set_ylim(p_start, p_stop)
    
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Time-Averaged Power (Counts)')

    ax.plot(wf_in.get_freqs(), wf_pwr_mean_integration, label='Time-averaged power spectrum')

    # Grab info for RFI masking
    bins, kurts = get_tavg_kurtosis(wf_in, n_divs)
    flagged_bins, flagged_kurts, masked_kurts, bin_mask, freq_mask = get_mask_kurtosis(wf_in, n_divs, threshold)

    # Plot frequency bins that were flagged as RFI
    if show_filtered_bins == True:
        full_freq_range = np.amax(wf_in.get_freqs()) - np.amin(wf_in.get_freqs())
        bin_width = full_freq_range / n_divs

        for rfi_bin in flagged_bins:
            xmin = rfi_bin
            xmax = rfi_bin + bin_width
            flagged_line = plt.axvspan(xmin=xmin, xmax=xmax, ymin=0, ymax=1, color='red', alpha=0.4)

        flagged_line.set_label('RFI-flagged channels')
        ax.legend(fancybox=True,shadow=True, loc='lower center', bbox_to_anchor=(1, 1), ncols=1)
    else:
        ax.legend(fancybox=True,shadow=True, loc='lower center', bbox_to_anchor=(1, 1), ncols=1)