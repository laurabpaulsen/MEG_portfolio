"""
Plots the two different areas data was used from

Area1 = labels = ["parsopercularis-lh", "parsorbitalis-lh", "parstriangularis-lh"]
Area2 =  "superiorfrontal-rh"
"""

import mne
import matplotlib.pyplot as plt

from pathlib import Path



if __name__ == "__main__":
    path = Path(__file__).parents[1]

    freesurfer_path = Path("/work/835482")

    # Load the data
    area1 = mne.read_labels_from_annot(
        subject="fsaverage",
        parc="aparc",
        hemi="lh",
        surf_name="white",
        subjects_dir=path / "data" / "fsaverage"
    )

    area2 = mne.read_labels_from_annot(
        subject="fsaverage",
        parc="aparc",
        hemi="rh",
        surf_name="white",
        subjects_dir=path / "data" / "fsaverage"
    )

    # Plot the data
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    mne.viz.plot_annot(
        subject="fsaverage",
        parc="aparc",
        hemi="lh",
        surf_name="white",
        subjects_dir=path / "data" / "fsaverage",
        axes=axes[0],
        show=False
    )
    mne.viz.plot_annot(
        subject="fsaverage",
        parc="aparc",
        hemi="rh",
        surf_name="white",
        subjects_dir=path / "data" / "fsaverage",
        axes=axes[1],
        show=False
    )
    plt.savefig(path / "fig" / "parcellations.png")
