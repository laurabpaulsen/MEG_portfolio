"""
GFP Processing Script

This script provides functionality to process and plot Global Field Power (GFP) for MEG data along with topomaps at GFP peaks.

Modules:
    - mne: Required for MEG data processing.
    - numpy and matplotlib: Required for data manipulation and plotting.
    - scipy.signal: Required for peak detection in GFP.
    - json: Required for reading session info from JSON files.
    - sys and pathlib: Required for file and path operations.
    - utils: Custom module that contains the preprocess_data_sensorspace function.

Functions:
    - calculate_and_plot_erf_gfp_with_topomaps(epochs, ch_type='mag', event_id=None, title=None, filename=None): 
      Calculates and plots the ERF and GFP for the provided epochs and displays topomaps at GFP peaks.
    - main(): The main function that drives the script, defining paths, loading session info, and iterating 
      over subjects and recordings to process the data.

Usage:
    To run the script from the terminal, navigate to the directory containing the script and execute:
        $ python <script_name>.py

Note: 
    Ensure that the 'utils' module with 'preprocess_data_sensorspace' function and other dependencies 
    are available in the appropriate path or directory.
    Ensure the paths and folders are correctly set up in the script.

Example Terminal Usage:
    $ python gfp_processing.py

Dependencies:
    - Ensure you have the 'mne', 'numpy', 'matplotlib', and 'scipy' libraries installed.
    - The 'utils' module with 'preprocess_data_sensorspace' function must be available.
    - Relevant data directories and files as mentioned in the script should be in place.
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import mne
from pathlib import Path
import json
import sys
from utils import preprocess_data_sensorspace


def calculate_and_plot_erf_gfp_with_topomaps(epochs, ch_type='mag', event_id=None, title=None, filename=None):
    """
    Calculate and plot Event-Related Field (ERF), Global Field Power (GFP), 
    and topomaps for specified epochs at GFP peaks.
    
    Parameters
    ----------
    epochs : mne.Epochs
        The epoched data.
    ch_type : str, optional
        Channel type to be picked ('mag' or 'grad'). Default is 'mag'.
    event_id : int or str, optional
        The id of the event for which to compute the ERF.
        If None (default), all epochs will be used.
    title : str, optional
        Title for the plot.
        If None (default), no title will be added.
    filename : str or Path, optional
        Path where the plot should be saved.
        If None (default), the plot is only displayed and not saved.
    """
    # Specify the channel type and average the epochs
    erf = (epochs[event_id].copy().pick_types(meg=ch_type).average() 
           if event_id 
           else epochs.copy().pick_types(meg=ch_type).average())

    # Compute GFP
    gfp = np.sqrt((erf.data ** 2).mean(axis=0))

    # Find peaks in the GFP
    peaks, _ = find_peaks(gfp, distance=20)
    peak_times = erf.times[peaks]

    # Plot ERF and GFP
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    erf.plot(axes=axes[0], spatial_colors=True, show=False)
    axes[1].plot(erf.times, gfp, label='GFP')
    axes[1].plot(peak_times, gfp[peaks], 'ro')  # Mark peaks with red dots
    axes[1].set(xlabel='Time (s)', ylabel='GFP', title='Global Field Power with Peaks')
    axes[1].set_xticks(np.arange(np.min(erf.times), np.max(erf.times), 0.1))
    axes[1].set_xticklabels([f"{tick*1000:.0f}" for tick in erf.times[::10]])

    # Adjust layout
    plt.tight_layout()
    if title:
        fig.suptitle(title, fontsize=16, y=1.02)
        plt.tight_layout(rect=[0, 0, 1, 0.97])

    # Plot topomaps at peaks
    for idx, peak_time in enumerate(peak_times):
        _, ax_topo = plt.subplots(1, 1, figsize=(3, 3))
        erf.plot_topomap(times=peak_time, size=3, show=False, axes=ax_topo, colorbar=False)
        ax_topo.set_title(f"Topomap @ {peak_time*1000:.1f} ms")

        plt.show()


def main():
    """
    Main function that drives the script, defining paths, loading session info, and processing the data.
    """
    # Define paths and settings
    NOTEBOOK_PATH = Path("/work/PernilleHøjlundBrams#8577/notebooks_PHB/MEG_portfolio/sanity_checks")
    sys.path.append(str(NOTEBOOK_PATH.parents[0]))

    MEG_DATA_PATH = Path("/work/834761")
    ICA_PATH = Path("/work/study_group_8/ICA")
    PLOT_PATH = NOTEBOOK_PATH / "plots_button_removed_topo"
    PLOT_PATH.mkdir(parents=True, exist_ok=True)

    with open(NOTEBOOK_PATH / 'session_info.txt', 'r') as file:
        SESSION_INFO = json.load(file)

    SUBJECTS = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    RECORDING_NAMES = [
        '001.self_block1',  '002.other_block1', '003.self_block2',
        '004.other_block2', '005.self_block3',  '006.other_block3'
    ]

    for subject in SUBJECTS:
        subject_info = SESSION_INFO[subject]
        reject = subject_info["reject"]
        subject_path = MEG_DATA_PATH / subject
        subject_meg_path = list(subject_path.glob("*_000000"))[0]

        for recording_name in RECORDING_NAMES:
            subject_session_info = subject_info[recording_name]
            fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]
            ICA_path_sub = ICA_PATH / subject / f"{recording_name}-ica.fif"

            if 'self' in recording_name:
                event_id = {"img/self/positive": 11, "img/self/negative": 12}
            elif 'other' in recording_name:
                event_id = {"img/assigned/positive": 21, "img/assigned/negative": 22}

            epochs = preprocess_data_sensorspace(
                fif_file_path,
                subject_session_info["bad_channels"],
                reject,
                ICA_path_sub,
                subject_session_info["noise_components"],
                event_ids=event_id
            )

            print(f"### \n ### EPOCH EVENT_ID after drop are: {epochs.event_id} ### \n ###")

            title = f"GFP for Subject: {subject}, Session: {recording_name}"
            filename = PLOT_PATH / f"{subject}_{recording_name}_ERF_plot.png"
            calculate_and_plot_erf_gfp_with_topomaps(epochs, event_id=None, title=title, filename=filename)


if __name__ == "__main__":
    main()
