"""
This script loops over all participants and all sessions and prepares the data for classification analysis.

DEV NOTES:
- [ ] Do we want to morph to "average" brain so we can compare across subjects?
- [ ] Do we want to parcel the data?
"""

from pathlib import Path
import mne
import numpy as np


def preprocess_data_sensorspace(fif_path:Path):
    raw = mne.io.read_raw_fif(fif_path, preload = True)

    # projecting out the empty room noise
    raw.apply_proj()

    # filtering
    raw.filter(None, 40, n_jobs = 4)

    # downsampling
    raw.resample(250)

    # find the events
    events = mne.find_events(raw, min_duration=0.0002)

    # remove channel MEG0422 (bad in all recordings)
    raw.drop_channels(["MEG0422"])

    # epoching
    epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=1, baseline=(None, 0), preload = True)

    return epochs



def epochs_to_sourcespace(epochs, fwd,  pick_ori='normal', lambda2=1.0 / 9.0, method='dSPM', label=None, ):
    noise_cov = mne.compute_covariance(epochs, tmax=0.000)
    
    inv = mne.minimum_norm.make_inverse_operator(epochs.info, fwd, noise_cov)

    stcs = mne.minimum_norm.apply_inverse_epochs(epochs, inv, lambda2, method, label, pick_ori=pick_ori)
    
    
    return X, y



if __name__ in "__main__":
    path = Path(__file__).parent

    fs_subjects_dir = Path("/work/835482") # path to freesurfer subjects directory
    MEG_data_path = Path("/work/834761")
    subjects = ["0115"] # ["0108","0109","0110","0111","0112","0113","0114","0115"]
    recording_names = ['001.self_block1',  '002.other_block1', '003.self_block2',  '004.other_block2', '005.self_block3',  '006.other_block3']
    morphmap_path = fs_subjects_dir "/morph-maps"
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

        if not subject_outpath.exists():
            subject_outpath.mkdir()

        for idx, recording_name in enumerate(recording_names):
            fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]
            epochs = preprocess_data_sensorspace(fif_file_path)

            # load forward solution
            fwd_fname = recording_name[4:] + '-oct-6-src-' + '5120-fwd.fif'
            fwd = mne.read_forward_solution(fs_subjects_dir / subject / 'bem' / fwd_fname)

            stcs = epochs_to_sourcespace(epochs, fwd)

            # morph subject path
            morph_subject_path = fs_subjects_dir / f"fsaverage-{subject}-morph.fif"

            # read
            morph = mne.read_source_morph(morph_subject_path)

            # morph
            stcs = morph.apply(stcs)
            

            X = np.array([stc.data for stc in stcs])
            y = epochs.events[:, -1]


            if idx == 0:
                X = X_tmp
                y = y_tmp
            else:
                X = np.concatenate((X, X_tmp))
                y = np.concatenate((y, y_tmp))

        print(X.shape)
        print(y.shape)
        
        # save the data
        np.save(subject_outpath / "X.npy", X)
        np.save(subject_outpath / "y.npy", y)
        
