"""
X shape = (n_epochs, n_times, n_sources)
"""

from pathlib import Path
import numpy as np
from sklearn import svm
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
import multiprocessing
from tqdm import tqdm

# local imports
import sys
sys.path.append(str(Path(__file__).parents[1]))
from utils import flip_sign, equalise_trials

def read_data(data_path, subject, x_file="X.npy", y_file="y.npy"):
    """Read in data for a given subject.

    Parameters
    ----------
    data_path : str
        Path to the data directory.
    subject : str
        Subject ID.

    Returns
    -------
    X : array
        Data array.
    y : array
        Label array.
    """
    if len(x_file) == 1:
        X = np.load(data_path / subject / x_file[0])
        y = np.load(data_path / subject / y_file[0])
    
    else: # loop over files and concatenate
        Xs = []
        ys = []

        for file_x in x_file:
            print(np.load(data_path / subject / file_x).shape)
            Xs.append(np.load(data_path / subject / file_x))
        
        y = np.load(data_path / subject / y_file[0])
        X = np.concatenate(Xs, axis=1)

    return X, y
    
def balance_class_weights(X, y):
    """
    Balances the class weight by removing trials so each class has the same number of trials as the class with the least trials.

    Parameters
    ----------
    X : array
        Data array with shape (n_trials, x, x)
    y : array
        Array with shape (n_trials, ) containing several classes

    Returns
    -------
    X_equal : array
        Data array with shape (n_trials, x, x) with equal number of trials for each class
    y_equal : array
        Array with shape (n_trials, ) containing classes with equal number of trials for each class

    """
    keys, counts = np.unique(y, return_counts = True)

    keep_inds = []

    for key in keys:
        index = np.where(np.array(y) == key)
        random_choices = np.random.choice(index[0], size = counts.min(), replace=False)
        keep_inds.extend(random_choices)
    
    X_equal = X[keep_inds, :, :]
    y_equal = y[keep_inds]

    return X_equal, y_equal


def across_subject(decoder, Xs, ys):
    """
    Run decoding across subjects.

    Parameters
    ----------
    decoder : sklearn estimator
        Decoder to use.
    Xs : array
        Data array.
    ys : array
        Label array.

    Returns
    -------
    results : array
        Array with shape (n_subjects, n_timepoints) containing decoding results for each subject and timepoint.
    """
    N, S, T = Xs[0].shape # ntrials, nsources, ntimepoints
    results = np.zeros((len(Xs), T)) # number of subjects, number of time points

    for i in tqdm(range(len(Xs)), desc = "Leaving out data from subject for testing"):
        X_tmp = Xs.copy()
        X_test = X_tmp.pop(i)

        y_tmp = ys.copy()
        y_test = y_tmp.pop(i)

        X_train = np.concatenate(X_tmp, axis=0)
        y_train = np.concatenate(y_tmp, axis=0)

        for t in tqdm(range(T), desc = "timepoint"):
            decoder.fit(X_train[:, :, t], y_train)
            results[i, t] = decoder.score(X_test[:, :, t], y_test)
    
    return results


def keep_triggers(X, y, zero = [], one = []):
    """
    Only keeps specified triggers and converts them to 0 and 1.

    Parameters
    ----------
    zero : list
        List of triggers to convert to 0.
    one : list
        List of triggers to convert to 1.
    
    Returns
    -------
    X : array
        Array with shape (n_trials, , )
    y : array
        Array with shape (n_trials, ) containing 0 and 1.
    """
    # only keep certain triggers
    trigger_idx = np.where(np.isin(y, zero + one))

    X = X[trigger_idx[0], :, :]
    y = y[trigger_idx[0]]


    y_new = np.zeros(len(y))

    for i in range(len(y)):
        if y[i] in zero:
            y_new[i] = 0
        elif y[i] in one:
            y_new[i] = 1
    
    return X, y_new



if __name__ in "__main__":

    path = Path(__file__).parent

    data_path = path.parent / "data"
    outpath = path / "results"
    trig_pairs_labels = ["innerspeech_buttonpress"]
    trig_pairs = [([11, 21, 12, 22], [202])]

    area_labels = ["LIFG", "mPFC"]
    labels_area_1 = ['parsopercularis-lh','parsorbitalis-lh','parstriangularis-lh']
    labels_area_2 = ['superiorfrontal-rh']

    k_features = 150

    # create output directory if it doesn't exist
    if not outpath.exists():
        outpath.mkdir()
                
    subjects = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"] 

    for idx_trig, trig_pair in enumerate(trig_pairs):
        print(f"Running decoding for {trig_pairs_labels[idx_trig]}")
        print(f"Triggers are {trig_pair[0]} and {trig_pair[1]}")
        
        for idx_area, area in enumerate([labels_area_1, labels_area_2]):
            print(f"Running decoding for {area}, which is in area {idx_area + 1}")
            Xs = []
            ys = []
            # read in data for all subjects
            for i, subject in enumerate(subjects):
                files_x = [f"X_{label}.npy" for label in area]
                files_y = [f"y_{label}.npy" for label in area]

                
                print(f"reading data for subject {subject}")
                print(f"reading files {files_x} and {files_y}")

                X, y = read_data(data_path, subject, x_file=files_x, y_file=files_y)


                # only keep data from certain triggers and convert y to zero and ones
                X, y = keep_triggers(X, y, zero = trig_pair[0], one = trig_pair[1])

                X, y = balance_class_weights(X, y)
                

                if i != 0:
                    X = flip_sign(Xs[0], X)

                Xs.append(X)
                ys.append(y)


            # make sure we keep an equal number of trials per participant
            Xs, ys = equalise_trials(Xs, ys)
            # run decoding
            decoder = make_pipeline(StandardScaler(), SelectKBest(k=k_features), svm.SVC(kernel = "rbf"))

            # run across subject decoding
            results = across_subject(decoder, Xs, ys)
            # save results
            np.save(outpath / f"across_subjects_{trig_pairs_labels[idx_trig]}_area_{area_labels[idx_area]}_{k_features}.npy", results)
