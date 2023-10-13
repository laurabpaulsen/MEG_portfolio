import mne
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

plt.rcParams['font.family'] = 'sans-serif'

def plot_noise_components(ica, raw, ica_noise_components, outpath):
    """
    Plots the noise components of an ICA object.
    """
    fig = plt.figure(figsize=(10, 7))
    spec = GridSpec(5, 2, width_ratios=[0.7, 2])

    # Create subplots using the grid
    topomap_axes = [plt.Subplot(fig, spec[i, 0]) for i in range(5)]
    time_series_axes = [plt.Subplot(fig, spec[i, 1]) for i in range(5)]

    for i in range(5):
        fig.add_subplot(topomap_axes[i])
        fig.add_subplot(time_series_axes[i])

    # Plot the topomap of the components
    ica.plot_components(inst=raw, picks=ica_noise_components[:2], axes=topomap_axes[:2], show=False)
    ica.plot_components(inst=raw, picks=ica_noise_components[-1], axes=topomap_axes[-2], show=False)
    
    for ax in topomap_axes:
        title = ax.get_title()
        ax.set_title("")
        ax.set_ylabel(title[:-6])


    topomap_axes[2].axis("off")
    topomap_axes[-1].axis("off")

    # Plot the time series of the components
    freq = raw.info["sfreq"]
    ica_sources = ica.get_sources(raw).get_data(start=int(20*freq), stop=int(30*freq))[ica_noise_components]
    extra_sensors = raw.get_data(['EOG001', 'ECG003'], start=int(20*freq), stop=int(30*freq))

    # Plot the time series of the components
    for idx, ax in enumerate(time_series_axes[:2]):
        ax.plot(ica_sources[idx].T, linewidth=0.5, color="k")
    
    time_series_axes[-2].plot(ica_sources[-1].T, linewidth=0.5, color="k")

    time_series_axes[2].plot(extra_sensors[1].T, label="ECG", linewidth=0.5, color="#0047AB")
    time_series_axes[-1].plot(extra_sensors[0].T, label="EOG", linewidth=0.5, color="#0047AB")
    time_series_axes[-1].legend(loc = "upper right")
    time_series_axes[2].legend(loc = "lower right")

    for ax in time_series_axes:
        ax.set_xticks(np.arange(0, 2501, step=250), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        ax.set_xlim(0, 2501)

    # set labels
    topomap_axes[0].set_title("Topomaps")
    time_series_axes[0].set_title("Timeseries")

    

    fig.tight_layout()
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
    plot_noise_components(ica, raw, ica_noise_components, outpath)
    
