from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def plot_decoding_accuracy(a, savepath = None):

    fig, ax = plt.subplots(1, 1, figsize = (12, 8), dpi = 300)

    for subject in range(a.shape[0]):
        ax.plot(a[subject], linewidth = 1)

    # plot the average
    average = np.average(a, axis = 0)
    ax.plot(average, linewidth = 3, color = "k")

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
    print(acc.shape)

    plot_decoding_accuracy(acc, savepath=outpath / "hellihallo_test.png")



    

