"""
Saves dictionary to txt file containing session information (bad channels, noise components, time span of experiment, reject criterion)
"""

from pathlib import Path
import json

session_info = {
    "0115": {
        "reject":{"mag": 3000e-15, "grad": 3000e-13, "eog": 200e-6},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": ["MEG0422"]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },
    },

    "0114": {
        "reject":{"mag": 3000e-15, "grad": 3000e-13, "eog": 300e-6},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 7, 10]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 6, 9]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 6, 9]
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [3, 6, 4]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 7, 8]
        },
    },
    "0113":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13, "eog": 400e-6},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": ["MEG0422"]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },
    },

    "0112":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13, "eog": 400e-6},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": ["MEG0422"]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },
    },

    "0111":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13, "eog": 500e-6},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": ["MEG0422"]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },
        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },
    },
    "0110":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13, "eog": 300e-6},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 9, 30]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 6, 27]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 6, 24]
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 7, 30]
        },
        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 6] # no eye blink component found
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 7] # no eye blink component found
        },
    },

    "0109":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13, "eog": 400e-6},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": ["MEG0422"]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": []
        },
    },

    "0108":{
        "reject": {"mag": 3000e-15, "grad": 3000e-13, "eog": 400e-6},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 12, 21]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 11, 15]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 7, 18]
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 12, 17]
        },
        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 8, 16]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": "LOOKS WEIRD! RUN ICA AGAIN!"
        },
    }

    

}



with open(Path(__file__).parent / "session_info.txt", "w") as f:
    f.write(json.dumps(session_info))
