"""
Saves dictionary to txt file containing session information (bad channels, noise components, time span of experiment, reject criterion)
"""

from pathlib import Path
import json

session_info = {
    "0115": {
        "reject":{"mag": 3000e-15, "grad": 3000e-13},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 15, 33]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 13, 44]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [6, 21, 42]
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [6, 10, 27]
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 17, 65]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [6, 14, 59]
        },
    },

    "0114": {
        "reject":{"mag": 3000e-15, "grad": 3000e-13,
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 8, 11]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components":[4, 7, 9]
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
            "noise_components": [4, 8, 9]
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 6, 7]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 7, 9]
        },
    },
    "0113":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 6, 8]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 6, 7]
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
            "noise_components": [4, 6, 10]
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 6, 10]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [3, 4, 5]
        },
    },

    "0112":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 21, 22]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 26]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 24]
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [9, 28]
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [9, 32]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [6, 35]
        },
    },

    "0111":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 7, 13]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 6, 13]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 6, 13]
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 7, 14]
        },
        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 6, 13]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 7, 12]
        },
    },
    "0110":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 7, 9, 36]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 6, 30]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 6]
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 8]
        },
        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 9]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 7]
        },
    },

    "0109":{
        "reject":{"mag": 3000e-15, "grad": 3000e-13},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [6, 9, 15]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 7, 12]
        },

        "003.self_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 10, 17]
        },

        "004.other_block2": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [3, 6, 11]
        },

        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [3, 7, 14]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [5, 6, 10]
        },
    },

    "0108":{
        "reject": {"mag": 3000e-15, "grad": 3000e-13},
        "001.self_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 7, 18]
        },

        "002.other_block1": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 8, 16]
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
            "noise_components": [5, 13, 20]
        },
        "005.self_block3": {
            "bad_channels": ["MEG0422"], 
            "tmin": 15, 
            "tmax": None, 
            "noise_components": [4, 8, 16]
        },

        "006.other_block3": {
            "bad_channels": ["MEG0422", "MEG1312"], 
            "tmin": 24, 
            "tmax": 360, 
            "noise_components": [20, 4, 5]
        }
    }

}
}



with open(Path(__file__).parent / "session_info.txt", "w") as f:
    f.write(json.dumps(session_info))
