"""
This script loops over all participants and all sessions and prepares the data for classification analysis.

TRIGGER CODES:

showing circles
'IMG_PS': 11
'IMG_PO': 21 
'IMG_NS': 12 
'IMG_NO': 22  
'IMG_BI': 23


responses
'button_press':202 

all other triggers are a mystery!

"""

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
    raw.filter(None, 40, n_jobs = 4)

    if ica_path:
        ica = mne.preprocessing.read_ica(ica_path)

        # remove noise components
        ica.exclude = noise_components

        # apply ica
        ica.apply(raw)

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
    """
    Parameters
    ----------
    epochs : mne.Epochs
        Epochs object.
    fwd : mne.Forward
        Forward solution.
    pick_ori : str, optional
        Orientation of the inverse solution. The default is 'normal'.
    lambda2 : float, optional
        Regularization parameter. The default is 1.0 / 9.0.
    method : str, optional
        Inverse method. The default is 'dSPM'.
    label : mne.Label, optional
        Label to restrict the inverse solution to. The default is None.
    
    Returns
    -------
    stcs : list
        List of source time courses.
    """
    noise_cov = mne.compute_covariance(epochs, tmax=0.000)
    
    inv = mne.minimum_norm.make_inverse_operator(epochs.info, fwd, noise_cov)

    stcs = mne.minimum_norm.apply_inverse_epochs(epochs, inv, lambda2, method, label, pick_ori=pick_ori)
    
    return stcs

def morph_stcs_label(morph_path:Path, stcs:list, fs_subjects_dir:Path, label_regexp:str = 'parsopercularis-lh'):
    """
    Parameters
    ----------
    morph_path : Path
        Path to the morph file.
    stcs : list
        List of source time courses to morph.
    fs_subjects_dir : Path
        Path to the freesurfer subjects directory.
    label_regexp : str, optional
        Regular expression to select the label. The default is 'parsopercularis-lh'.
    
    Returns
    -------
    X : np.array
        Array with source time courses.
    """
    morph = mne.read_source_morph(morph_path)
            
    # morph from subject to fsaverage
    stcs = [morph.apply(stc) for stc in stcs]

    label = mne.read_labels_from_annot("fsaverage", parc="aparc", subjects_dir=fs_subjects_dir, regexp=label_regexp)[0]
    vertices = label.get_vertices_used(stcs[0].vertices[0]) # get sources from the data that are within the label
            
    X = np.array([stc.data[vertices, :] for stc in stcs])

    return X


if __name__ in "__main__":
    path = Path(__file__).parents[1]

    fs_subjects_dir = Path("/work/835482") # path to freesurfer subjects directory
    MEG_data_path = Path("/work/834761")
    subjects = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    recording_names = ['001.self_block1',  '002.other_block1', '003.self_block2', '004.other_block2', '005.self_block3',  '006.other_block3']
    outpath = path / "data"
    fwd_fsaverage_path = fs_subjects_dir / "fsaverage" / "bem" / "fsaverage-oct-6-src.fif"

    ICA_path = path / "ICA"

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

            ICA_path_sub = ICA_path / subject / f"{recording_name}-ica.fif"

            epochs = preprocess_data_sensorspace(fif_file_path, reject, subject_session_info["bad_channels"], ICA_path_sub, subject_session_info["noise_components"])

            # load forward solution
            fwd_fname = recording_name[4:] + '-oct-6-src-' + '5120-fwd.fif'
            fwd = mne.read_forward_solution(fs_subjects_dir / subject / 'bem' / fwd_fname)

            # get source time courses
            stcs = epochs_to_sourcespace(epochs, fwd)

            # morph from subject to fsaverage
            morph_subject_path = fs_subjects_dir / subject / "bem" / f"{subject}-oct-6-src-morph.h5"
            X_tmp = morph_stcs_label(morph_subject_path, stcs, fs_subjects_dir)
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
        
