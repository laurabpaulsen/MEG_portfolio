"""
Saves dictionary to pickle file containing session information (bad channels, noise components, time span of experiment)
"""

from pathlib import Path
import pickle


session_info = {
    "0115": {
        "self_block1.fif": {
            "bad_channels": ["MEG0422"], 
            "tmin": 0, 
            "tmax": 0, 
            "noise_components": []
        },

        "other_block1.fif": {
            "bad_channels": ["MEG0422"], 
            "tmin": 0, 
            "tmax": 0, 
            "noise_components": ["MEG0422"]
        },

        "self_block2.fif": {
            "bad_channels": ["MEG0422"], 
            "tmin": 0, 
            "tmax": 0, 
            "noise_components": []
        },

        "other_block2.fif": {
            "bad_channels": ["MEG0422"], 
            "tmin": 0, 
            "tmax": 0, 
            "noise_components": []
        },

        "self_block3.fif": {
            "bad_channels": ["MEG0422"], 
            "tmin": 0, 
            "tmax": 0, 
            "noise_components": []
        },

        "other_block3.fif": {
            "bad_channels": ["MEG0422"], 
            "tmin": 0, 
            "tmax": 0, 
            "noise_components": []
        },
    },

}


if __name__ == "__main__":
    # Save session_info dictionary to pickle file
    with open(Path(__file__).parent / "session_info.pickle", "wb") as f:
        pickle.dump(session_info, f)