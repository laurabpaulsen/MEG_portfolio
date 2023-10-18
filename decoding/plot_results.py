from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def axis_seconds(ax):
    """
    Changes the x axis to seconds
    """
    ax.set_xticks(np.arange(0, 551, step=50), [-0.2, 0. , 0.2, 0.4, 0.6, 0.8, 1. , 1.2, 1.4, 1.6, 1.8, 2.])

def plot_decoding_accuracy(acc, title, legend_title, savepath = None):
    fig, ax = plt.subplots(1, 1, figsize = (12, 8), dpi = 300)

    for subject in range(acc.shape[0]):
        ax.plot(acc[subject], linewidth = 1, alpha = 0.6, label = f"Subject {subject + 1}")

    # plot the average
    average = np.average(acc, axis = 0)
    ax.plot(average, linewidth = 2, color = "k")

    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Accuracy")

    axis_seconds(ax)

    # vertical line at 0
    ax.axvline(x = 0+0.2*250, color = "k", linestyle = "--", linewidth = 1)

    # horizontal line at 0.5
    ax.axhline(y = 0.5, color = "k", linestyle = "--", linewidth = 1)

    # legend
    ax.legend(title = legend_title, loc = "upper right")

    # x limits
    ax.set_xlim(0, 250*2.2)

    if savepath:
        plt.savefig(savepath)



if __name__ in "__main__":
    path = Path(__file__).parent
    results_path = path / "results" 
    outpath = path / "fig"

    x_files = ["across_subjects_pos_neg_area_LIFG.npy", 
               "across_subjects_pos_neg_area_mPFC.npy",
               "across_subjects_assigned_selfchosen_area_LIFG.npy",
               "across_subjects_assigned_selfchosen_area_mPFC.npy"]
    

    # create output directory if it doesn't exist
    if not outpath.exists():
        outpath.mkdir()

    for files in x_files:
        acc = np.load(results_path / files)
        plot_decoding_accuracy(
            acc, 
            title = files, 
            legend_title = "Test subject",
            savepath = outpath / f"{files[:-4]}.png"
            )

    

