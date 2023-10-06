"""
This script loops over all participants and all sessions and prepares the data for classification analysis.

DEV NOTES:
- [ ] different tresholds reject - subject 0109 + 0111 + 0112   so many epochs are dropped
- [ ] read in pickle file with reject criteria



QUESTIONS FOR LAU
- Seems like you did not apply the projections in preparing X? Any reason for this? Maybe it does not matter for ML but does for ERF's and such?
- Q: Does it matter a lot with bad channels. A: Yes but for the purpose of this assignment it is important



TRIGGER CODES:
'IMG_PS': 11
'IMG_PO': 21 
'IMG_NS': 12 
'IMG_NO': 22  
---------------
'IMG_BM': 13
'IMG_BI': 23

"""

from pathlib import Path
import mne
import numpy as np
import json


def preprocess_data_sensorspace(fif_path:Path, bad_channels:list, reject = None):
    raw = mne.io.read_raw_fif(fif_path, preload = True)

    # projecting out the empty room noise
    raw.apply_proj()

    # Low pass filtering to get rid of line noise
    raw.filter(None, 40, n_jobs = 4)

    # downsampling to 250 hz (from 1000 hz)
    raw.resample(250)

    # find the events
    events = mne.find_events(raw, min_duration=2/raw.info["sfreq"])

    # remove bad channels
    raw.drop_channels(bad_channels)

    # epoching
    epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=1, baseline=(None, 0), preload = True, reject = reject)

    return epochs


def epochs_to_sourcespace(epochs, fwd,  pick_ori='normal', lambda2=1.0 / 9.0, method='dSPM', label=None):
    noise_cov = mne.compute_covariance(epochs, tmax=0.000)
    
    inv = mne.minimum_norm.make_inverse_operator(epochs.info, fwd, noise_cov)

    stcs = mne.minimum_norm.apply_inverse_epochs(epochs, inv, lambda2, method, label, pick_ori=pick_ori)
    
    return stcs


if __name__ in "__main__":
    path = Path(__file__).parents[1]

    fs_subjects_dir = Path("/work/835482") # path to freesurfer subjects directory
    MEG_data_path = Path("/work/834761")
    subjects = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    recording_names = ['001.self_block1',  '002.other_block1', '003.self_block2', '004.other_block2', '005.self_block3',  '006.other_block3']
    outpath = path / "data"
    fwd_fsaverage_path = fs_subjects_dir / "fsaverage" / "bem" / "fsaverage-oct-6-src.fif"

    # load session information with reject criterion
    with open(path / 'session_info.txt', 'r') as f:
        file = f.read()
        session_info = json.loads(file)
    
    # load src for fsaverage
    src_fsaverage = mne.read_source_spaces(fwd_fsaverage_path)


    for subject in subjects:
        subject_info = session_info[subject]
        reject = subject_info["reject"]

        subject_path = MEG_data_path / subject
        # find the folder with MEG data and not the folder with MRI data
        subject_meg_path = list(subject_path.glob("*_000000"))[0]

        # make a folder for the subject
        subject_outpath = outpath / subject

        if not subject_outpath.exists():
            subject_outpath.mkdir(parents=True)

        for idx, recording_name in enumerate(recording_names):
            subject_session_info = subject_info[recording_name]

            fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]

            #ADD REMOVING NOISY ICA COMPONENTS

            epochs = preprocess_data_sensorspace(fif_file_path, reject, subject_session_info["bad_channels"])

            # load forward solution
            fwd_fname = recording_name[4:] + '-oct-6-src-' + '5120-fwd.fif'
            fwd = mne.read_forward_solution(fs_subjects_dir / subject / 'bem' / fwd_fname)

            stcs = epochs_to_sourcespace(epochs, fwd)

            # morph subject path
            morph_subject_path = fs_subjects_dir / subject / "bem" / f"{subject}-oct-6-src-morph.h5"
            morph = mne.read_source_morph(morph_subject_path)
            
            # morph from subject to fsaverage
            stcs = [morph.apply(stc) for stc in stcs]

            label = mne.read_labels_from_annot("fsaverage", parc="aparc", subjects_dir=fs_subjects_dir, regexp='parsopercularis-lh')[0] # CHECK THAT THIS LABEL IS ACTUALLY BROCAS
            vertices = label.get_vertices_used(stcs[0].vertices[0]) # get sources from the data that are within the label
            
            X_tmp = np.array([stc.data[vertices, :] for stc in stcs])
            y_tmp = epochs.events[:, -1]


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
        
