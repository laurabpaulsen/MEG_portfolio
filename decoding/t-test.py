import numpy as np
from pathlib import Path
from scipy.stats import ttest_rel, ttest_1samp

def seconds_to_sample(sec, freq = 250):
    """
    Converts seconds to sample
    """
    return int(sec * freq)


if __name__ in "__main__":
    path = Path(__file__).parent
    results_path = path / "results" 

    time_windows = [(.520, .670)] # add more time windows here (in seconds)

    # account for the fact that we have data from -0.2 seconds before the onset of the stimulus
    time_windows_new = [(0.2 + tw[0], 0.2 + tw[1]) for tw in time_windows]
    decoding_types = ["pos_neg", "assigned_selfchosen"]
    areas = ["LIFG", "mPFC"]

    # make empty file to write results to
    with open(results_path / f"t-test.txt", "w") as f:
        f.write("")

    for i, tw in enumerate(time_windows_new):
        for area in areas:
            acc_dt1 = np.load(results_path / f"across_subjects_{decoding_types[0]}_area_{area}_150.npy")
            acc_dt2 = np.load(results_path / f"across_subjects_{decoding_types[1]}_area_{area}_150.npy")

            # get the samples for the time window
            start_sample = seconds_to_sample(tw[0])
            end_sample = seconds_to_sample(tw[1])

            # get the accuracy for the time window
            acc_dt1 = acc_dt1[:, start_sample:end_sample]
            acc_dt2 = acc_dt2[:, start_sample:end_sample]

            # take the average across the time window
            acc_dt1 = np.mean(acc_dt1, axis = 1)
            acc_dt2 = np.mean(acc_dt2, axis = 1)

            # conduct a t-test
            t, p = ttest_rel(acc_dt1, acc_dt2)

            # write results to file
            with open(results_path / f"t-test.txt", "a") as f:
                f.write(f"Time window: {time_windows[i]}\n")
                f.write(f"Decoding type 1: {decoding_types[0]}\n")
                f.write(f"Decoding type 2: {decoding_types[1]}\n")
                f.write(f"Mean accuracy decoding type 1: {np.mean(acc_dt1)}, standard deviation: {np.std(acc_dt1)}\n")
                f.write(f"Mean accuracy decoding type 2: {np.mean(acc_dt2)}, standard deviation: {np.std(acc_dt2)}\n")
                f.write(f"Area: {area}\n")
                f.write(f"t = {t}, p = {p}")
                f.write("\n\n")

    # check that selfchosen vs assigned decoding in LIFG are significantly different from 0.5
    acc = np.load(results_path / f"across_subjects_assigned_selfchosen_area_LIFG_150.npy")
    start_sample = seconds_to_sample(0.520)
    end_sample = seconds_to_sample(0.670)
    acc = acc[:, start_sample:end_sample]
    acc = np.mean(acc, axis = 1)
    t, p = ttest_1samp(acc, 0.5)

    with open(results_path / f"t-test.txt", "a") as f:
        f.write("One sample t-test for assigned vs selfchosen decoding in LIFG\n")
        f.write(f"Time window: {time_windows[0]}\n")
        f.write(f"Decoding type 1: assigned_selfchosen\n")
        f.write(f"Mean accuracy decoding type 1: {np.mean(acc)}, standard deviation: {np.std(acc)}\n")
        f.write(f"Area: LIFG\n")
        f.write(f"t = {t}, p = {p}")
        f.write("\n\n")
    

    # check that pos vs neg decoding in mPFC are significantly different from 0.5

    acc = np.load(results_path / f"across_subjects_pos_neg_area_mPFC_150.npy")
    start_sample = seconds_to_sample(0.520)
    end_sample = seconds_to_sample(0.670)
    acc = acc[:, start_sample:end_sample]
    acc = np.mean(acc, axis = 1)
    t, p = ttest_1samp(acc, 0.5)

    with open(results_path / f"t-test.txt", "a") as f:
        f.write("One sample t-test for pos vs neg decoding in mPFC\n")
        f.write(f"Time window: {time_windows[0]}\n")
        f.write(f"Decoding type 1: pos_neg\n")
        f.write(f"Mean accuracy decoding type 1: {np.mean(acc)}, standard deviation: {np.std(acc)}\n")
        f.write(f"Area: mPFC\n")
        f.write(f"t = {t}, p = {p}")
        


            
            


    
