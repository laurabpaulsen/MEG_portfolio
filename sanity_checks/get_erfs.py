"""
ERF processing script
This script processes and plots Event-Related Fields (ERF) for MEG data (see corresponding partner-script for GFP-plots)

Modules:
    - mne: Required for MEG data processing
    - json: Required for reading session info from JSON files
    - sys and pathlib: Required for file and path operations

Functions:
    - load_session_info(filepath): Reads session info from a given JSON file
    - get_event_id(recording_name): Determines the event ID based on the recording name
    - process_subject_data(subject, recording_name, session_info, MEG_data_path, ICA_path, plot_path): 
      Processes the MEG data for a given subject and recording name and generates ERF plots
    - calculate_and_plot_erf(epochs, event_id=None, title=None, filename=None): 
    - main(): defining paths, loading session info, and iterating over subjects and recordings to process the data

Notes: 
- Ensure that 'utils' module with 'preprocess_data_sensorspace' function and other dependencies are available in the appropriate path

"""

def calculate_and_plot_erf(epochs, event_id=None, title=None, filename=None):
    """
    Calculate and plot the ERF for specified epochs
    
    Parameters
    ----------
    epochs : mne.Epochs
        The epoched data
    event_id : int or str, optional
        The id of the event for which to compute the ERF
        If None (default), all epochs will be used
    title : str, optional
        The title to be added on top of the plots
        If None (default), no title will be added
    filename : str or Path, optional
        The path and filename where the plot should be saved
        If None (default), the plot won't be saved, but only displayed
    """

    if event_id is not None:
        # Compute ERF for specific event type
        erf = epochs[event_id].average()
    else:
        # Compute ERF using all epochs
        erf = epochs.average()

    # Separating data for magnetometers and gradiometers
    erf_mag = erf.copy().pick_types(meg='mag')
    erf_grad = erf.copy().pick_types(meg='grad')
    
    # Plotting ERF for magnetometers
    fig1 = erf_mag.plot(spatial_colors=True, titles='ERF - Magnetometers', show=False)
    
    # Adding a title if provided
    if title is not None:
        fig1.suptitle(title, fontsize=16, y=1.02)
    
    # Adjusting the figure size
    fig1.set_size_inches((10, 6))

    if filename:
        mag_filename = filename.with_name(f"{filename.stem}_mag{filename.suffix}")
        plt.tight_layout()
        plt.savefig(mag_filename, dpi=300, bbox_inches='tight', pad_inches=0.5)
    plt.show()
    
    # Plotting ERF for gradiometers
    fig2 = erf_grad.plot(spatial_colors=True, titles='ERF - Gradiometers', show=False)

    # Adding a title if provided
    if title is not None:
        fig2.suptitle(title, fontsize=16, y=1.02)
    
    # Adjusting the figure size
    fig2.set_size_inches((10, 6))

    if filename:
        grad_filename = filename.with_name(f"{filename.stem}_grad{filename.suffix}")
        plt.tight_layout()
        plt.savefig(grad_filename, dpi=300, bbox_inches='tight', pad_inches=0.5)

    plt.show()
    
    return erf

# funcss
import json
from pathlib import Path
import sys
import mne
from utils import preprocess_data_sensorspace

# Load sess func
def load_session_info(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# get_event_id
def get_event_id(recording_name):
    if 'self' in recording_name:
        return {
            "img/self/positive": 11,
            "img/self/negative": 12
        }
    elif 'other' in recording_name:
        return {
            "img/assigned/positive": 21,
            "img/assigned/negative": 22
        }

# processing_subject_data
def process_subject_data(subject, recording_name, session_info, MEG_data_path, ICA_path, plot_path):
    subject_info = session_info[subject]
    reject = subject_info["reject"]
    subject_path = MEG_data_path / subject
    subject_meg_path = list(subject_path.glob("*_000000"))[0]
    fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]

    ICA_path_sub = ICA_path / subject / f"{recording_name}-ica.fif"
    event_id = get_event_id(recording_name)

    epochs = preprocess_data_sensorspace(
        fif_file_path,
        subject_info[recording_name]["bad_channels"],
        reject,
        ICA_path_sub,
        subject_info[recording_name]["noise_components"],
        event_ids=event_id
    )

    print(f"### \n ### EPOCH EVENT_ID after drop are: {epochs.event_id} ### \n ###")

    title = f"ERF for Subject: {subject}, Session: {recording_name}"
    filename = plot_path / f"{subject}_{recording_name}_ERF_plot.png"

    calculate_and_plot_erf(epochs, event_id=None, title=title, filename=filename)

# driver
def main():
    NOTEBOOK_PATH = Path("/work/PernilleHøjlundBrams#8577/notebooks_PHB/MEG_portfolio/sanity_checks")
    sys.path.append(str(NOTEBOOK_PATH.parents[0]))
    
    from utils import preprocess_data_sensorspace  # Move the import here after updating sys.path

    MEG_DATA_PATH = Path("/work/834761")
    ICA_PATH = Path("/work/study_group_8/ICA")
    PLOT_PATH = NOTEBOOK_PATH / "plots_button_removed_topo"

    PLOT_PATH.mkdir(parents=True, exist_ok=True)

    SESSION_INFO = load_session_info('/work/PernilleHøjlundBrams#8577/notebooks_PHB/MEG_portfolio/session_info.txt')

    SUBJECTS = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    RECORDING_NAMES = [
        '001.self_block1', '002.other_block1', '003.self_block2',
        '004.other_block2', '005.self_block3', '006.other_block3'
    ]

    for subject in SUBJECTS:
        for recording_name in RECORDING_NAMES:
            process_subject_data(subject, recording_name, SESSION_INFO, MEG_DATA_PATH, ICA_PATH, PLOT_PATH)


if __name__ == '__main__':
    main()
