"""
This script loops over all participants and all sessions and prepares the data for classification analysis.
"""

from pathlib import Path
import mne
import numpy as np


def preprocess_data(fif_path:Path):
    raw = mne.io.read_raw_fif(fif_path)

    # projecting out the empty room noise
    raw.apply_proj()

    # filtering
    raw.filter(None, 40)

    # downsampling
    raw.resample(250)

    # find the events
    events = mne.find_events(raw, min_duration=0.0002)

    # remove channel MEG0422
    raw.drop_channels(["MEG0422"])

    # reject
    reject = dict(eeg=100e-6)

    # epoching
    epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=1, baseline=(None, 0), reject=reject, preload=True)

    X = epochs.get_data()
    y = epochs.events[:, -1]

    return X, y







if __name__ in "__main__":
    path = Path(__file__).parent

    MEG_data_path = Path("/work/834761")
    subjects = ["0115"]
    subject_folder = "20230928_000000"
    recording_names = ['001.self_block1',  '002.other_block1', '003.self_block2',  '004.other_block2', '005.self_block3',  '006.other_block3']

    outpath = path / "data"

    # make sure that output folder exists
    if not outpath.exists():
        outpath.mkdir()

    for subject in subjects:
        subject_path = MEG_data_path / subject
        # find the folder with MEG data and not the folder with MRI data
        subject_meg_path = list(subject_path.glob("*_000000"))[0]

        # make a folder for the subject
        subject_outpath = outpath / subject

        for recording_name in recording_names:
            fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]
            X, y = preprocess_data(fif_file_path)

            # path for saving the data
            recording_outpath = subject_outpath / recording_name

            # make a folder for the recording
            if not recording_outpath.exists():
                recording_outpath.mkdir()

            # save the data
            np.save(recording_outpath / "X.npy", X)
            np.save(recording_outpath / "y.npy", y)
        
