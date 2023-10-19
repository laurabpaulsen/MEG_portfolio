"""
This script loops over all participants and all sessions and prepares the data for classification analysis.

- [ ] Only include the triggers from README when saving data

"""

import os
import sys
from pathlib import Path
import json
import mne
import numpy as np
import re
import logging
import argparse
import multiprocessing

if not os.path.exists("/tmp/mne-cache"):
    try:
        os.mkdir("/tmp/mne-cache")
        mne.utils.config.set_cache_dir("/tmp/mne-cache")
    except:
        pass

# local imports
sys.path.append(str(Path(__file__).parents[1]))
from utils import preprocess_data_sensorspace, epochs_to_sourcespace, morph_stcs_label

def sanitize_label_for_filename(label: str) -> str:
    """
    Sanitize a label for use in a filename.

    Any characters not in [a-zA-Z0-9_-] are replaced with an underscore.

    Args:
        label: The label to sanitize.

    Returns:
        The sanitized label.
    """

    return re.sub(r"[^a-zA-Z0-9_\-]", "_", label)

def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_cpu", type=int, default=multiprocessing.cpu_count(), help="Number of CPUs to use, default is all available")
    parser.add_argument("--parcel_regex", type=str, nargs="*", default=["superiorfrontal-lh|superiorfrontal-rh"], help="Regular expression for the parcels to include")
    parser.add_argument("--all_parcels", default=False, action="store_true", help="Whether to include all parcels (ignores parcel_regex)")
    args = parser.parse_args()
    
    num_cpu = args.num_cpu
    os.environ["OMP_NUM_THREADS"] = str(num_cpu)
    logging.info(f"Using {num_cpu} CPUs")
    
    path = Path(__file__).parents[1]

    fs_subjects_dir = Path("/work/835482") # path to freesurfer subjects directory
    MEG_data_path = Path("/work/834761")
    subjects = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    recording_names = ['001.self_block1',  '002.other_block1', '003.self_block2', '004.other_block2', '005.self_block3', '006.other_block3']
    outpath = path / "data"
    fwd_fsaverage_path = fs_subjects_dir / "fsaverage" / "bem" / "fsaverage-oct-6-src.fif"
    ICA_path = path / "ICA"

    labels = ["parsopercularis-lh", "parsorbitalis-lh", "parstriangularis-lh", "superiorfrontal-rh"]
    # load session information with reject criterion
    with open(path / 'session_info.txt', 'r') as f:
        file = f.read()
        session_info = json.loads(file)
    
    # load src for fsaverage
    src_fsaverage = mne.read_source_spaces(fwd_fsaverage_path)

    for label in labels:
        logging.info(f"Processing label {label}")
        for subject in subjects:
            logging.info(f"Processing subject {subject}")
            subject_info = session_info[subject]
            subject_path = MEG_data_path / subject
            
            # find the folder with MEG data and not the folder with MRI data
            subject_meg_path = list(subject_path.glob("*_000000"))[0]

            # make a folder for the subject
            subject_outpath = outpath / subject

            if not subject_outpath.exists():
                subject_outpath.mkdir(parents=True)

            for idx, recording_name in enumerate(recording_names):
                logging.info(f"Processing recording {recording_name}")
                subject_session_info = subject_info[recording_name]

                fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]

                ICA_path_sub = ICA_path / subject / f"{recording_name}-ica.fif"

                if 'self' in recording_name:
                    event_id = {
                        "img/self/positive": 11, 
                        "img/self/negative": 12,
                        "button": 202}
                elif 'other' in recording_name: 
                    event_id = {
                        "img/assigned/positive": 21, 
                        "img/assigned/negative": 22,
                        "button": 202}

                epochs = preprocess_data_sensorspace(
                    fif_path = fif_file_path, 
                    bad_channels = subject_session_info["bad_channels"], 
                    reject = subject_info["reject"], 
                    ica_path = ICA_path_sub, 
                    noise_components = subject_session_info["noise_components"], 
                    event_ids=event_id,
                    tmin = -0.2,
                    tmax = 1,
                    n_jobs=num_cpu)

                # load forward solution
                fwd_fname = recording_name[4:] + '-oct-6-src-' + '5120-fwd.fif'
                fwd = mne.read_forward_solution(fs_subjects_dir / subject / 'bem' / fwd_fname)

                # get source time courses
                stcs = epochs_to_sourcespace(epochs, fwd, n_jobs=num_cpu)

                # morph from subject to fsaverage
                morph_subject_path = fs_subjects_dir / subject / "bem" / f"{subject}-oct-6-src-morph.h5"
                
                X_tmp = morph_stcs_label(morph_subject_path, stcs, fs_subjects_dir, label)
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
            sanitized_label = sanitize_label_for_filename(label)
            logging.info(f"Saving data for label {sanitized_label}")
            X_path = subject_outpath / f"X_{sanitized_label}.npy"
            logging.info(f"Saving X data to {X_path}")
            y_path = subject_outpath / f"y_{sanitized_label}.npy"
            logging.info(f"Saving y data to {y_path}")
            np.save(X_path, X)
            np.save(y_path, y)


if __name__ in "__main__":
    main()
