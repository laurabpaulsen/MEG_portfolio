import mne
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json

def plot_noise_components(ica, raw, ica_noise_components):
    """
    Plots the noise components of an ICA object.
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # plot the topomap of the components
    ica.plot_components(inst=raw, picks=ica_noise_components, axes=axes[0], show=False)

    # plot the time series of the components
    # extract the time series of the components
    ica_sources = ica.get_sources(raw)
    print(ica_sources.shape)

    # plot the time series of the components
    axes[1].plot(ica_sources.get_data()[ica_noise_components].T)

    plt.savefig(outpath / "ica_components.png")
    


if __name__ in "__main__":
    path = Path(__file__)
    outpath =  path.parent / "fig"
    ICA_path = path.parents[1] / "ICA"

    MEG_data_path = Path("/work/834761")
    subject = "0114"
    recording_name = '001.self_block1'

    # load session information with bad channels and cropping times
    with open(path.parents[1] / 'session_info.txt', 'r') as f:
        file = f.read()
        session_info = json.loads(file)


    subject_info = session_info[subject]

    subject_path = MEG_data_path / subject
        
    # find the folder with MEG data and not the folder with MRI data
    subject_meg_path = list(subject_path.glob("*_000000"))[0]


    if not outpath.exists():
        outpath.mkdir(parents=True)

    subject_session_info = subject_info[recording_name]

    # read ICA solution
    ica = mne.preprocessing.read_ica(ICA_path / subject / f"{recording_name}-ica.fif")

    # load raw data
    raw = mne.io.read_raw_fif(list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0], preload=True)
    
    raw.filter(1, 40, fir_design='firwin')
    raw.resample(250)
    raw.apply_proj()

    ica_noise_components = subject_session_info["noise_components"]

    # plot the noise ica components
    plot_noise_components(ica, raw, ica_noise_components)
    
