from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def axis_seconds(ax):
    """
    Changes the x axis to seconds
    """
    ax.set_xticks(np.arange(0, 301, step=50), [-0.2, 0. , 0.2, 0.4, 0.6, 0.8, 1. ])

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
    ax.set_xlim(0, 300)

    if savepath:
        plt.savefig(savepath)



if __name__ in "__main__":
    path = Path(__file__).parent
    results_path = path / "results" 
    outpath = path / "fig"

    label = "whole_brain"

    # create output directory if it doesn't exist
    if not outpath.exists():
        outpath.mkdir()
    """
    acc = np.load(results_path / f"across_subjects_11_202_{label}.npy")

    plot_decoding_accuracy(
        acc, 
        title = "Decoding accuracy for self chosen positive and button press (across subject)", 
        legend_title = "Test subject",
        savepath = outpath / f"across_subjects_11_202_{label}.png"
        )
    """

    within_subject = []
    for i in range(1, 9):
        within_subject.append(np.load(results_path / f"within_subject_{i}_11_202_{label}.npy"))

    within_subject = np.mean(np.array(within_subject), axis = 2)
    
    plot_decoding_accuracy(
        within_subject,
        legend_title = "Subject",
        title = "Decoding accuracy for self chosen positive and button press (within subject)", 
        savepath = outpath / f"within_subjects_11_202_{label}.png"
        )

    

