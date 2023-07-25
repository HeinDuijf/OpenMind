import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from generate_figures.plot_functions import cmap_line_r, lineplot_size


def calculate_tipping_source(competence_reliable_group, competence_unreliable_group):
    tipping_source_evaluation = (competence_unreliable_group - 1 / 2) / (
        competence_reliable_group + competence_unreliable_group - 1
    )
    return tipping_source_evaluation


def figure_epistemic_potential(filename: str = None):
    """Generates plot of required source evaluative capacities depending on the
    competences of the reliable, for one specific competence of the unreliable group,
    and coloring the areas below the curves.

        Parameters
        ----------
        filename: str
            Location where the plot is to be saved

        Returns
        -------
        Plot of required source evalutative capacities"""
    # 0. Initialize variables
    competences_reliable_group = np.round(np.linspace(0.50001, 0.9, 41), 2)
    competences_unreliable_group = np.round(np.linspace(0.9, 0.55, 8), 2)

    # 1. Generate data for plotting
    data = [
        [
            calculate_tipping_source(
                competence_reliable_group, competence_unreliable_group
            )
            for competence_unreliable_group in competences_unreliable_group
        ]
        for competence_reliable_group in competences_reliable_group
    ]
    df = pd.DataFrame(
        data, index=competences_reliable_group, columns=competences_unreliable_group
    )

    # 2. Plot
    ax = df.plot.area(
        stacked=False,
        title="The epistemic potential of open-mindedness\n",
        xlabel="Competence reliable group ($p_R$)",
        ylabel="Source evaluative capacity ($p_{ES}$)",
        figsize=lineplot_size,
        colormap=cmap_line_r,
        xticks=np.linspace(0.5, 1, 6),
        yticks=np.linspace(0, 1, 11),
        xlim=(0.5, 0.9),
        ylim=(0, 1.0),
    )

    #
    plt.legend(
        title="Competence unreliable group ($p_U$)", loc="upper right", ncol=2,
    )
    plt.hlines(0.5, xmin=0.5, xmax=1.0, colors="k", linestyles="dashed")
    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


if __name__ == "__main__":
    folder_name = "new_figures"
    os.makedirs(folder_name, exist_ok=True)
    filename = f"{folder_name}/Figure_epistemic_potential"
    figure_epistemic_potential(filename=filename)
