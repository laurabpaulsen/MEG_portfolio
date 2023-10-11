
from pathlib import Path
import mne
import numpy as np
import json

# local imports
sys.path.append(str(Path(__file__).parents[1]))
from utils import preprocess_data_sensorspace # NOTE TO PERN MOVED FUNCTION TO UTILS AS IT IS BEING USED IN MULTIPLE SCRIPTS




if __name__ in "__main__":
    path = Path(__file__).parents[1]

    MEG_data_path = Path("/work/834761")
    subjects = ["0108", "0109", "0110", "0111", "0112", "0113", "0114", "0115"]
    recording_names = ['001.self_block1',  '002.other_block1', '003.self_block2', '004.other_block2', '005.self_block3',  '006.other_block3']
    plot_path = path / "plots"
    ICA_path = path / "ICA"

    with open(path / 'session_info.txt', 'r') as f:
        file = f.read()
        session_info = json.loads(file)

    # make sure that plot path exists
    if not plot_path.exists():
        plot_path.mkdir(parents=True)

    
    for subject in subjects:
        subject_info = session_info[subject]
        reject = subject_info["reject"]

        subject_path = MEG_data_path / subject
        
        # find the folder with MEG data and not the folder with MRI data
        subject_meg_path = list(subject_path.glob("*_000000"))[0]


        for idx, recording_name in enumerate(recording_names):
            subject_session_info = subject_info[recording_name]
            fif_file_path = list((subject_meg_path / "MEG" / recording_name / "files").glob("*.fif"))[0]
            plot_filename = plot_path / f"{subject}-{recording_name}.png"

            ICA_path_sub = ICA_path / subject / f"{recording_name}-ica.fif"

            epochs = preprocess_data_sensorspace(fif_file_path, reject, subject_session_info["bad_channels"], ICA_path_sub, subject_session_info["noise_components"])

            # plot hurra



            # Save plot