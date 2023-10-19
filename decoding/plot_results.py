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

def determine_ax(info):
    """
    Determines the ax to plot on based on the decoding and area
    """
    if info["decoding"] == "pos_neg":
        row = 0
    elif info["decoding"] == "assigned_selfchosen":
        row = 1
    
    if info["area"] == "LIFG":
        col = 0
    elif info["area"] == "mPFC":
        col = 1

    return row, col

def twobytwo_plot(files_dict, results_path, savepath = None):

    fig, axs = plt.subplots(2, 2, figsize = (12, 8), dpi = 300)

    for idx, (filename, info) in enumerate(files_dict.items()):
        try: 
            acc = np.load(results_path / filename)

            # determine the ax to plot on
            row, col = determine_ax(info)

            for subject in range(acc.shape[0]):
                axs[row, col].plot(acc[subject], linewidth = .8, alpha = 0.6, label = f"Subject {subject + 1}")

            # plot the average
            average = np.average(acc, axis = 0)
            axs[row, col].plot(average, linewidth = 1.5, color = "k")

            axs[row, col].set_title(info["decoding"] + " " + info["area"])
            axs[row, col].set_xlabel("Time (s)")
            axs[row, col].set_ylabel("Accuracy")
        except:
            pass

        for ax in axs.flat:
            axis_seconds(ax)

    if savepath:
        plt.savefig(savepath)


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
        
    
    # 2X2 plot with results for pos_neg and assigned_selfchosen in rows and LIFG and mPFC in columns
    files = {"across_subjects_pos_neg_area_mPFC_150.npy": {"decoding": "pos_neg", "area": "mPFC"},
                "across_subjects_pos_neg_area_LIFG_150.npy": {"decoding": "pos_neg", "area": "LIFG"},
                "across_subjects_assigned_selfchosen_area_mPFC_150.npy": {"decoding": "assigned_selfchosen", "area": "mPFC"},
                "across_subjects_assigned_selfchosen_area_LIFG_150.npy": {"decoding": "assigned_selfchosen", "area": "LIFG"}
        }

    twobytwo_plot(
        files, 
        results_path = results_path,
        savepath = outpath / "results.png"
        )


    

