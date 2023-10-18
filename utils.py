
import mne
import numpy as np
from pathlib import Path

def preprocess_data_sensorspace(fif_path:Path, bad_channels:list = [], reject = None, ica_path:Path = None, noise_components = None, event_ids = None, tmin = -0.2, tmax = 1, n_jobs = 4):
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
    raw.filter(0.1, 40, n_jobs = n_jobs)

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
    epochs = mne.Epochs(raw, events, event_id = event_ids, tmin=tmin, tmax=tmax, baseline=(None, 0), preload = True, reject = reject, proj = True)

    # downsampling
    epochs.resample(250, n_jobs = n_jobs)
    
    return epochs


def epochs_to_sourcespace(epochs, fwd,  pick_ori='normal', lambda2=1.0 / 9.0, method='dSPM', label=None, n_jobs = 4):
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
    noise_cov = mne.compute_covariance(epochs, tmax=0.000, n_jobs=n_jobs)
    
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

    labels = mne.read_labels_from_annot("fsaverage", parc="aparc", subjects_dir=fs_subjects_dir, regexp=label_regexp)
    vertices = np.concatenate([label.get_vertices_used(stcs[0].vertices[0]) for label in labels])
            
    X = np.array([stc.data[vertices, :] for stc in stcs])

    return X

def flip_sign(X1, X2):
    """
    This function is used to flip the sign of the data in X2 if the correlation between the data in X1 and X2 is negative.

    Parameters
    ----------
    X1 (array): 
        Data from the session to compare to with shape (n_trials, n_channels, n_times)
        
    X2 (array): 
        Data from the session to flip the sign of with shape (n_trials, n_channels, n_times)

    Returns
    -------
    X2 (ndarray): 
        X2 with the sign flipped if the correlation between X1 and X2 is negative in the given parcel with shape (n_channels, n_trials, n_times)
    """

    # checking that the T and P dimensions are the same
    if X1.shape[2] != X2.shape[2]:
        raise ValueError('The number of time points in the two sessions are not the same')
    
    if X1.shape[1] != X2.shape[1]:
        raise ValueError('The number of parcels in the two sessions are not the same')

    # loop over parcels
    for i in range(X1.shape[1]):
        # take means over trials
        mean1 = np.mean(X1[:, i, :], axis = 0)
        mean2 = np.mean(X2[:, i, :], axis = 0)

        # calculate correlation
        corr = np.corrcoef(mean1, mean2)[0, 1]

        if corr < 0: # if correlation is negative, flip sign
            X2[:, i, :] = X2[:, i, :] * -1

    return X2

def n_trials(X, y, n: int, axis: int=0):
    """
    Removes trials from X and y, such that the number of trials is equal to n. It is assumed that classes are already balanced. Therefore an equal number of trials is removed from each class.

    Parameters:
    ----------
    X : np.array
        data
    y : np.array
        labels (0 or 1)
    n : int
        number of trials to keep
    axis : int, optional
        axis along which to remove trials from X array, by default 0
    
    Returns:
    -------
    X : np.array
        data with n trials
    y : np.array
        labels with n trials
    """

    # total number of trials
    n_trials = len(y)

    # number of trials to remove per condition
    n_remove = (n_trials - n)//2

    # getting indices of trials to remove
    idx_0 = np.random.choice(np.where(y==0)[0], n_remove, replace=False)
    idx_1 = np.random.choice(np.where(y==1)[0], n_remove, replace=False)

    # combining indices
    idx = np.concatenate((idx_0, idx_1))

    # removing trials
    X = np.delete(X, idx, axis=axis)
    y = np.delete(y, idx)

    return X, y

def equalise_trials(Xs:list, ys:list):
    """
    This function is used to equalise the number of trials across a list of X and y arrays.

    Parameters
    ----------
    Xs : list
        list of X arrays
    ys : list
        list of y arrays
    
    Returns
    -------
    Xs : list
        list of X arrays with equal number of trials
    ys : list
        list of y arrays with equal number of trials
    """
    # min number of trials
    min_trials = min([len(y) for y in ys])

    # make sure all sessions have the same number of trials
    for i,(X, y) in enumerate(zip(Xs, ys)):
        Xs[i], ys[i] = n_trials(X, y, min_trials)

    return Xs, ys