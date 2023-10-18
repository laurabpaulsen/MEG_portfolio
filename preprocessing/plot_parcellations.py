"""
Plots the two different areas data was used from

Area1 = labels = ["parsopercularis-lh", "parsorbitalis-lh", "parstriangularis-lh"]
Area2 =  "superiorfrontal-rh"
"""

import mne
import matplotlib.pyplot as plt

from pathlib import Path

# local imports
import sys
sys.path.append(str(Path(__file__).parents[1]))
from utils import preprocess_data_sensorspace, epochs_to_sourcespace, morph_stcs_label

def plot_parc(stc, subject, parc, hemi, surf_name, subjects_dir, fig):
    mne.viz.plot_source_estimates(
        stc,
        subject=subject,
        surface=surf_name,
        hemi=hemi,
        subjects_dir=subjects_dir,
        time_label="",
        colormap="viridis",
        transparent=True,
        colorbar=False,
        figure = fig,
        backend = "matplotlib",
        background='white'
    )


def get_stc(fif_file_path, fwd_fsaverage_path, label, fs_subjects_dir, subject):
    epochs = preprocess_data_sensorspace(
                    fif_path = fif_file_path, 
                    event_ids={"img/self/positive": 11, "img/self/negative": 12},
                    tmin = -0.2,
                    tmax = 2)

    # load forward solution
    fwd_fname = recording_name[4:] + '-oct-6-src-' + '5120-fwd.fif'
    fwd = mne.read_forward_solution(fs_subjects_dir / subject / 'bem' / fwd_fname)

    # get source time courses
    stcs = epochs_to_sourcespace(epochs, fwd)

    # morph from subject to fsaverage
    morph_subject_path = fs_subjects_dir / subject / "bem" / f"{subject}-oct-6-src-morph.h5"
    

    morph = mne.read_source_morph(morph_subject_path)
            
    # morph from subject to fsaverage
    stc = morph.apply(stcs[0])
    return stc



if __name__ == "__main__":
    path = Path(__file__).parent

    freesurfer_path = Path("/work/835482")
    subject = "0108"
    recording_name = '001.self_block1'
    MEG_data_path = Path("/work/834761")
    fwd_fsaverage_path = freesurfer_path / "fsaverage" / "bem" / "fsaverage-oct-6-src.fif"

    subject_path = MEG_data_path / subject
            
    # find the folder with MEG data and not the folder with MRI data
    subject_meg_path = list(subject_path.glob("*_000000"))[0]

    # get the 
    fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]

    stc = get_stc(fif_file_path, fwd_fsaverage_path, "superiorfrontal-rh", freesurfer_path, subject=subject)

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    plot_parc(stc, "fsaverage", "superiorfrontal-rh", "rh", "pial", freesurfer_path, fig)
    plt.savefig(path / "fig" / "parcellations.png")
