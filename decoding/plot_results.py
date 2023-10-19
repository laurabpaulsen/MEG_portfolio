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
        ax.plot(acc[subject], linewidth = .8, alpha = 0.6, label = f"Subject {subject + 1}")

    # plot the average
    average = np.average(acc, axis = 0)
    ax.plot(average, linewidth = 1.5, color = "k")

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
    ax.set_ylim(.40, .60)

    if savepath:
        plt.savefig(savepath)

    plt.close()



if __name__ in "__main__":
    path = Path(__file__).parent
    results_path = path / "results" 
    outpath = path / "fig"

    # get all npy files in results_path
    files = list(results_path.glob("*.npy"))

    # create output directory if it doesn't exist
    if not outpath.exists():
        outpath.mkdir()

    for f in files:
        acc = np.load(f)
        print(acc.shape)
        plot_decoding_accuracy(
            acc[:, :-1], 
            title = f.stem, 
            legend_title = "Test subject",
            savepath = outpath / f"{f.name[:-4]}.png"
            )

    

