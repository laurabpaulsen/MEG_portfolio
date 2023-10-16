# MEG_portfolio
This repository holds the code for the MEG portfolio assignment for the Advanced Cognitive Neuroscience course (F2023), which includes preprocessing of MEG data, sanitity checks and decoding of inner speech. We investigate the decoding accuracy of positive and negative inner speech as well as self-chosen and assigned inner speech. Both classification analyses are conducted using data from *brain area 1* and *brain area 2*.


## Project organisation
The GitHub repository is organised as follows:
```
├── data                                    Not included in repo
│   ├── 0108
│   ├── 0109
│   └── ...
├── ICA                                     Not included in repo 
│   ├── 0108
│   ├── 0109
│   └── ...
├── preprocessing
│   ├── check_ica.ipynb                     Notebook for checking ICA components
│   ├── prep_for_classification.py          Preprocessing data for classification
│   └── run_ica.py                          Generate ICA solutions for all subjects and runs
├── sanity_checks                           Code used for sanity checks and results
├── env_to_ipykernel.sh                     Let env be used as kernel in jupyter notebook
├── generate_session_info.py                Bad channels, tmin, tmax, etc.
├── README.md                               
├── requirements.txt
├── session_info.txt                        Session info for all runs
├── setup_env.sh                            Setup environment
└── utils.py                                Functions used in multiple scripts
```

## Collaborators
The project was done by study group 8 consisting of:
- [Pernille](https://github.com/PernilleBrams)
- [Luke](https://github.com/zeyus)
- [Aleksandrs](https://github.com/sashapustota)
- [Christoffer](https://github.com/clandberger)
- [Laura](https://github.com/laurabpaulsen)

## Notes
### Triggers in the MEG data
|       Description        |   Trigger   |
|------------------|-----------|
|     IMG_PS       |    11     |
|     IMG_PO       |    21     |
|     IMG_NS       |    12     |
|     IMG_NO       |    22     |
|     IMG_BI       |    23     |
|  button_press    |   202     |
