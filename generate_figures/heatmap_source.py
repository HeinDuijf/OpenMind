import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from generate_figures.plot_vars import PlotVars
from probability_calculator import ProbabilityCalculator


def figure_heatmap_source(
    degree_open_mindedness: int,
    advantage: float = 0,
    filename: str = None,
):
    """Generates heatmap of epistemic benefit of open_mindedness for a range of
    competences and source evaluative capacities.

    Parameters
    ----------
    degree_open_mindedness: int
        Degree of open-mindedness
    advantage: float
        The competence advantage of the associating group
        (disadvantage is represented by negative advantage)

    filename: str
        Location where the plot is to be saved, if you want to save

    Returns
    -------
    Heatmap of epistemic benefit"""
    # 0. Initialize variables

    index = [0.6, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9]
    index.reverse()
    columns = [0.6, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9]
    data = np.zeros((len(index), len(columns)))
    mask = np.zeros_like(data)
    # 1. Generate data about expected accuracy for various parameter settings
    for x, c in enumerate(index):
        for y, p in enumerate(columns):
            prob_calculator = ProbabilityCalculator(
                degree_open_mindedness=degree_open_mindedness,
                competence_opposer=c - advantage,
                competence_associate=c,
                source_evaluative_capacity=p,
            )
            data[x, y] = prob_calculator.compute_probability_right() - c
            if data[x, y] < 0:
                mask[x, y] = True
            data[x, y] = round(data[x, y], 2)

    # 2. Plot data as heatmap
    cbar_ticks = [0, 0.05, 0.1, 0.15]
    df = pd.DataFrame(data, index=index, columns=columns)
    heatmap_style = PlotVars.heatmap_style(
        mask, vmin=0.00, vmax=0.15, cbar_ticks=cbar_ticks
    )

    plt.rc("font", **PlotVars.font_style)
    plt.figure(figsize=PlotVars.figure_size)
    fig = sns.heatmap(df, **heatmap_style)
    bottom, top = fig.get_ylim()
    fig.set_ylim(bottom, top)

    # 3. Styling and labelling plot
    titletext: str = (
        "Epistemic benefits where degree of open-mindedness ($n$) is "
        + str(degree_open_mindedness)
    )
    ylabeltext: str = ""
    if advantage > 0:
        titletext = titletext + "\n and competence advantage is " + str(advantage)
        ylabeltext = "Competence ($p_A$)"
    elif advantage < 0:
        advantage = -1 * advantage
        titletext = titletext + "\n and competence disadvantage is " + str(advantage)
        ylabeltext = "Competence ($p_A$)"
    else:
        titletext = titletext + "\n in a homogeneous community"
        ylabeltext = "Competence ($p_A$ and $p_O$)"
    fig.set_title(titletext, **PlotVars.title_style)
    fig.set_xlabel("Source evaluative capacity ($p_{ES}$)", **PlotVars.label_style)
    fig.set_ylabel(ylabeltext, **PlotVars.label_style)

    # 4. Showing or saving plot
    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


if __name__ == "__main__":
    folder_name = "new_figures"
    os.makedirs(folder_name, exist_ok=True)

    figure_heatmap_source(
        degree_open_mindedness=2,
        advantage=0,
        filename=f"{folder_name}/Figure_heatmap_source_evaluation_n2",
    )
    figure_heatmap_source(
        degree_open_mindedness=4,
        advantage=0,
        filename=f"{folder_name}/Figure_heatmap_source_evaluation_n4",
    )
