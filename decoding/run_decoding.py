"""
X shape = (n_epochs, n_times, n_sources)
"""

from pathlib import Path
import numpy as np
from sklearn import svm
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

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

    X = np.load(data_path / subject / x_file)
    y = np.load(data_path / subject / y_file)

    return X, y
    


def within_subject_decoding(data_path, outpath, subjects):
    """Run decoding within subject.

    Parameters
    ----------
    data_path : str
        Path to the data directory.
    outpath : str
        Path to the output directory.
    subjects : list
        List of subjects to run decoding on.
    """
    pass

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
    """
    N, T, S = Xs[0].shape
    results = np.array((Xs.shape[0], T)) # number of subjects, number of time points

    for i in range(Xs):
        X_tmp = Xs.copy()
        X_test = X_tmp.pop(i)

        y_tmp = ys.copy()
        y_test = y_tmp.pop(i)

        X_train = np.concatenate(X_tmp, axis=0)
        y_train = np.concatenate(y_tmp, axis=0)

        for t in range(T):
            decoder.fit(X_train[:, t, :], y_train)
            results[i, t] = decoder.score(X_test[:, t, :], y_test)
    
    return results


if __name__ in "__main__":

    path = Path(__file__).parent

    data_path = path / "data"
    outpath = path / "results"

    # create output directory if it doesn't exist
    if not outpath.exists():
        outpath.mkdir()
    
    subjects = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    label = 'parsopercularis-lh'    

    # read in data for all subjects
    Xs = []
    ys = []

    for subject in subjects:
        X, y = read_data(data_path, subject, x_file="X.npy", y_file="y.npy")
        Xs.append(X)
        ys.append(y)

    # run decoding
    decoder = make_pipeline(StandardScaler(), svm.SVC(C=1, kernel='linear', gamma='auto'))
    results = across_subject(decoder, Xs, ys)

    # save results
    np.save(outpath / "across_subjects.npy", results)


    