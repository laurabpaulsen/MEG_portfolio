
import mne
import numpy as np
from pathlib import Path

def preprocess_data_sensorspace(fif_path:Path, bad_channels:list, reject = None, ica_path:Path = None, noise_components = None, event_ids = None):
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
    event_ids: dict, optional
        Dictionary with event ids and triggers to include in the epochs. Default is None
    
    Returns
    -------
    epochs : mne.Epochs
        Epochs object.
    """
    raw = mne.io.read_raw_fif(fif_path, preload = True)


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
    epochs = mne.Epochs(raw, events, event_id = event_ids, tmin=-0.2, tmax=1, baseline=(None, 0), preload = True, reject = reject, proj = True)

    # downsampling
    epochs.resample(250)
    
    return epochs


def epochs_to_sourcespace(epochs, fwd,  pick_ori='normal', lambda2=1.0 / 9.0, method='dSPM', label=None, return_inv = False):
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
    if return_inv:
        return stcs, inv
    
    else:
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


 
def flip_sign(X1, X2):
    """
    This function is used to flip the sign of the data in X2 if the correlation between the data in X1 and X2 is negative.

    Parameters
    ----------
    X1 (array): 
        Data from the session to compare to with shape (n_channels, n_trials, n_times)
        
    X2 (array): 
        Data from the session to flip the sign of with shape (n_channels, n_trials, n_times)

    Returns
    -------
    X2 (ndarray): 
        X2 with the sign flipped if the correlation between X1 and X2 is negative in the given parcel with shape (n_channels, n_trials, n_times)
    """

    # checking that the T and P dimensions are the same
    if X1.shape[0] != X2.shape[0]:
        raise ValueError('The number of time points in the two sessions are not the same')
    
    if X1.shape[2] != X2.shape[2]:
        raise ValueError('The number of parcels in the two sessions are not the same')

    # loop over parcels
    for i in range(X1.shape[2]):
        # take means over trials
        mean1 = np.mean(X1[:, :, i], axis = 1)
        mean2 = np.mean(X2[:, :, i], axis = 1)

        # calculate correlation
        corr = np.corrcoef(mean1, mean2)[0, 1]

        if corr < 0: # if correlation is negative, flip sign
            X2[:, :, i] = X2[:, :, i] * -1

    return X2
