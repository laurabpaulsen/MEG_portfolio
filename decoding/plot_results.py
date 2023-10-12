from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def ax_seconds(ax):
    """
    Convert the x-axis to seconds.
    """
    ticks = ax.get_xticks()
    ticks = ticks / 250
    ax.set_xticklabels(ticks)

def plot_decoding_accuracy(acc, title, savepath = None):
    fig, ax = plt.subplots(1, 1, figsize = (12, 8), dpi = 300)

    for subject in range(acc.shape[0]):
        ax.plot(acc[subject], linewidth = 1, alpha = 0.5, label = f"Subject {subject + 1}")

    # plot the average
    average = np.average(acc, axis = 0)
    ax.plot(average, linewidth = 3, color = "k")

    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Accuracy")

    ax_seconds(ax)

    # vertical line at 0
    ax.axvline(x = 0, color = "k", linestyle = "--", linewidth = 1)

    # horizontal line at 0.5
    ax.axhline(y = 0.5, color = "k", linestyle = "--", linewidth = 1)

    # legend
    legend_title = "Test subject"
    ax.legend(title = legend_title, loc = "upper right")

    if savepath:
        plt.savefig(savepath)

    


if __name__ in "__main__":
    path = Path(__file__).parent
    results_path = path / "results" / "across_subjects_11_12.npy"
    outpath = path / "fig"

    # create output directory if it doesn't exist
    if not outpath.exists():
        outpath.mkdir()

    acc = np.load(results_path)

    plot_decoding_accuracy(
        acc, 
        title = "Decoding accuracy for self chosen positive and negative valence", 
        savepath = outpath / "across_subjects_11_12.png"
        )



    

