
from pathlib import Path
import mne
import numpy as np
import json


def preprocess_data_sensorspace(fif_path:Path, bad_channels:list, reject = None, ica_path:Path = None, noise_components = None):
    """
    
    Parameters
    ----------
    fif_path : Path
        Path to the fif file.
    bad_channels : list
        List of bad channels.
    reject : dict, optional
        Reject dictionary. The default is None.
    ica_path : Path, optional
        Path to the ICA file. The default is None.
    noise_components : list, optional
        List of noise ICA components. The default is None.
    
    Returns
    -------
    epochs : mne.Epochs
        Epochs object.
    """
    raw = mne.io.read_raw_fif(fif_path, preload = True)

    # projecting out the empty room noise
    raw.apply_proj()

    # Low pass filtering to get rid of line noise
    raw.filter(0.1, 40, n_jobs = 4)

    if ica_path:
        ica = mne.preprocessing.read_ica(ica_path)

        # remove noise components
        ica.exclude = noise_components

        # apply ica
        ica.apply(raw)

    # find the events
    events = mne.find_events(raw, min_duration=2/raw.info["sfreq"])

    # remove bad channels
    raw.drop_channels(bad_channels)

    # epoching
    epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=1, baseline=(None, 0), preload = True, reject = reject)

    # downsampling
    epochs.resample(250)
    return epochs




if __name__ in "__main__":
    path = Path(__file__).parents[1]

    MEG_data_path = Path("/work/834761")
    subjects = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    recording_names = ['001.self_block1',  '002.other_block1', '003.self_block2', '004.other_block2', '005.self_block3',  '006.other_block3']
    plot_path = path / "plots"
    ICA_path = path / "ICA"

    with open(path / 'session_info.txt', 'r') as f:
        file = f.read()
        session_info = json.loads(file)

    # make sure that plot path exists
    if not plot_path.exists():
        plot_path.mkdir(parents=True)

    
    for subject in subjects:
        subject_info = session_info[subject]
        reject = subject_info["reject"]

        subject_path = MEG_data_path / subject
        
        # find the folder with MEG data and not the folder with MRI data
        subject_meg_path = list(subject_path.glob("*_000000"))[0]


        for idx, recording_name in enumerate(recording_names):
            subject_session_info = subject_info[recording_name]
            fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]
            plot_filename = plot_path / f"{subject}-{recording_name}.png"

            ICA_path_sub = ICA_path / subject / f"{recording_name}-ica.fif"

            epochs = preprocess_data_sensorspace(fif_file_path, reject, subject_session_info["bad_channels"], ICA_path_sub, subject_session_info["noise_components"])

            # plot hurra



            # Save plot