import numpy as np
from scipy.signal import butter, filtfilt, hilbert, decimate
import pandas as pd
import glob
import os

def common_average_referencing(eeg):
    return eeg - np.mean(eeg, axis=1, keepdims=True)

def butter_filter(data, low_freq, high_freq, fs, btype):
    nyquist = 0.5 * fs
    
    if low_freq:
        low = low_freq / nyquist
    else:
        low = None
        
    if high_freq:
        high = high_freq / nyquist
    else:
        high = None
    
    # Adjust the filter parameters based on the filter type
    if btype == 'low':
        wn = high
    elif btype == 'high':
        wn = low
    elif btype == 'band':
        wn = [low, high]
    else:
        raise ValueError(f"Invalid filter parameters for {btype} filter.")
    
    b, a = butter(4, wn, btype=btype)
    return filtfilt(b, a, data, axis=0)




def compute_hga(eeg, fs, ds_factor=5):
    # Band-pass filter the data
    eeg_bp = butter_filter(eeg, 70, 150, fs, 'band')
    # Compute analytic amplitude
    hga = np.abs(hilbert(eeg_bp, axis=0))
    # Downsample
    hga_ds = decimate(hga, ds_factor, axis=0) # from 1kHz to 200Hz
    return hga_ds

def compute_lfs(eeg, fs,ds_factor=5):
    # Low-pass filter
    eeg_lp = butter_filter(eeg, None, 100, fs, 'low')
    # Downsample
    lfs_ds = decimate(eeg_lp, ds_factor, axis=0) # from 1kHz to 200Hz
    return lfs_ds

def normalize_channel_data(data):
    return (data - np.mean(data, axis=0)) / np.std(data, axis=0)

def process_eeg(eeg):
    # Apply common average referencing
    eeg_car = common_average_referencing(eeg)
    
    # Compute HGA and LFS
    hga = compute_hga(eeg_car, 1000,5)
    lfs = compute_lfs(eeg_car, 1000,5)
    
    # Data normalization
    hga_norm = normalize_channel_data(hga)
    lfs_norm = normalize_channel_data(lfs)
    #print(hga_norm.shape,lfs_norm.shape)
    
    # Compute BBS
    combined_data = np.concatenate((hga_norm, lfs_norm), axis=1)

    if not os.path.exists(path_output):
        os.makedirs(path_output)
        
    # Save BBS Feature
    np.save(os.path.join(path_output,f'{fname}_seeg.npy'), combined_data)

    # Save HGA Feature
    #np.save(os.path.join(path_output,f'{fname}_seeg.npy'), hga_norm)

    # Save LFS Feature
    #np.save(os.path.join(path_output,f'{fname}_seeg.npy'), lfs_norm)


if __name__=="__main__":


    path_output = '/path/to/output'
    
    extension = 'csv'
    directory = '/path/to/input'
    all_filenames = sorted(glob.glob('{}/*.{}'.format(directory, extension)))
    

    for filename in all_filenames:
        
        filename_split = filename.split('\\')
        fname = filename_split[-1]
        fname = fname.split('.')[0]
        eeg = pd.read_csv(filename).values
        eeg = eeg[:,1:]
        eeg = eeg.T

        process_eeg(eeg)