# MEG_portfolio
Portfolio assignment for advanced cognitive neuroscience (F2023)



## Overview
```
├── data ............................... Not included in repo
│   ├── 0108
│   ├── 0109
│   └── ...
├── ICA ................................ Not included in repo 
│   ├── 0108
│   ├── 0109
│   └── ...
├── preprocessing
│   ├── check_ica.ipynb ................ Notebook for checking ICA components
│   ├── prep_for_classification.py ..... Preprocessing data for classification
│   ├── run_ica.py ..................... Run ICA on data
├── env_to_ipykernel.sh ................ Let env be used as kernel in jupyter notebook
├── generate_session_info.py ........... Bad channels, tmin, tmax, etc.
├── README.md                               
├── requirements.txt
├── session_info.txt ................... Session info for all runs
├── setup_env.sh ....................... Setup environment
```


## Notes
### Triggers
|       Description        |   Trigger   |
|------------------|-----------|
|     IMG_PS       |    11     |
|     IMG_PO       |    21     |
|     IMG_NS       |    12     |
|     IMG_NO       |    22     |
|     IMG_BI       |    23     |
|  button_press    |   202     |
