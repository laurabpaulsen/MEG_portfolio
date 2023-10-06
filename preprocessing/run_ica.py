'''
Usage, e.g., python run_ica.py -i '/media/8.1/raw_data/raw_data/memory_01.fif'

This script is used for initial preprocessing. The following steps are included:
    1) Excludes bad-channels based on file 'session_info.txt'. These channels were marked as bad based on visual expection of raw MEG data.
    2) Crops the ends of the MEG recordings according to times specified in 'session_info.txt'
    3) High and low pass filtering
    4) Running independent component analysis (ICA)

The script saves the ICA to a file. Unwanted components are manually detected and removed the file 'check_ica.ipynb'.
'''

import argparse
import mne
import json
from pathlib import Path

def run_ICA_on_session(filepath:Path, outpath:Path, bad_channels:list, tmin:float, tmax:float):
    """
    Runs ICA on a single session and saves the ICA solution to a file.

    Parameters
    ----------
    filepath : Path
        Path to the raw fif file.
    outpath : Path
        Path to save the ICA solution to.
    bad_channels : list
        List of channels to mark as bad.
    tmin : float
        Start time of the recording (in seconds).
    tmax : float
        End time of the recording (in seconds).
    
    Returns
    -------
    None.
    """
    # loading in the raw data
    raw = mne.io.read_raw_fif(filepath, on_split_missing = 'ignore');
    raw.load_data();
    raw.pick_types(meg=True, eeg=False, stim=True)

    # marking the channels as bad
    raw.info['bads'] = bad_channels

    cropped = raw.copy().crop(tmin = tmin, tmax = tmax)
    del raw

    ### BAND PASS FILTER ### 
    filt_raw = cropped.copy().filter(l_freq=1, h_freq=40)
    del cropped

    ### RESAMPLING ###
    resampled_raw = filt_raw.copy().resample(250)
    del filt_raw

    ### ICA ###
    ica = mne.preprocessing.ICA(n_components=None, random_state=97, method='fastica', max_iter=3000, verbose=None)
    ica.fit(resampled_raw)

    # saving the ICA solution
    ica.save(outpath, overwrite=True)


if __name__ == '__main__':
    path = Path(__file__)
    outpath =  path.parents[1] / "ICA"

    MEG_data_path = Path("/work/834761")
    subjects = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    recording_names = ['001.self_block1',  '002.other_block1', '003.self_block2', '004.other_block2', '005.self_block3',  '006.other_block3']


    # load session information with bad channels and cropping times
    with open(path.parents[1] / 'session_info.txt', 'r') as f:
        file = f.read()
        session_info = json.loads(file)


    for subject in subjects: # loop over subjects
        subject_info = session_info[subject]

        subject_path = MEG_data_path / subject
        
        # find the folder with MEG data and not the folder with MRI data
        subject_meg_path = list(subject_path.glob("*_000000"))[0]

        # make a folder for the subject to save the ICA files to
        subject_outpath = outpath / subject

        if not subject_outpath.exists():
            subject_outpath.mkdir(parents=True)

        for idx, recording_name in enumerate(recording_names): # loop over recordings
            subject_session_info = subject_info[recording_name]
            
            # find the MEG recording file
            fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]
            
            run_ICA_on_session(filepath = fif_file_path, 
                               outpath = subject_outpath / recording_name / "'-ica.fif'", 
                               bad_channels = subject_session_info["bad_channels"], 
                               tmin = subject_session_info["tmin"], 
                               tmax = subject_session_info["tmax"]
                               )

            

    

    


