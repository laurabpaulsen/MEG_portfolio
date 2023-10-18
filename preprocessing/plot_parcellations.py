"""
Plots the two different areas data was used from

Area1 = labels = ["parsopercularis-lh", "parsorbitalis-lh", "parstriangularis-lh"]
Area2 =  "superiorfrontal-rh"
"""

import mne
import matplotlib.pyplot as plt

from pathlib import Path

def plot_parc(subject, parc, hemi, surf_name, subjects_dir, axes):
    brain = mne.viz.Brain(
        subject=subject,
        hemi=hemi,
        surf=surf_name,
        subjects_dir=subjects_dir,
        background="white",
        foreground="black",
        cortex="bone",
        size=(800, 600),
        show=False,
        axes=axes)
    
    brain.add_annotation(
        parc=parc
    )



if __name__ == "__main__":
    path = Path(__file__).parents[1]

    freesurfer_path = Path("/work/835482")

    # Load the data
    area1 = mne.read_labels_from_annot(
        subject="fsaverage",
        parc="aparc",
        hemi="lh",
        surf_name="white",
        subjects_dir=freesurfer_path
    )

    area2 = mne.read_labels_from_annot(
        subject="fsaverage",
        parc="aparc",
        hemi="rh",
        surf_name="white",
        subjects_dir=freesurfer_path
    )

    # Plot the data
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    plot_parc("fsaverage", "aparc", "lh", "white", freesurfer_path, axes[0])
    plot_parc("fsaverage", "aparc", "rh", "white", freesurfer_path, axes[1])

    plt.savefig(path / "fig" / "parcellations.png")
