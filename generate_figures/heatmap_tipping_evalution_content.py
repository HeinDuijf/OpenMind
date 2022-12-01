import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from generate_figures.plot_vars import PlotVars
from probability_calculator import ProbabilityCalculator


def figure_heatmap_tipping_evaluation_content(
    degree_open_mindedness: int = 4, filename: str = None
):
    """Generates heatmap of tipping points for content evaluative capacity where
    open-mindedness becomes epistemically beneficial for an open-minded agent for a
    range of competences and source evaluative capacities.

    Parameters
    ----------
    degree_open_mindedness: int
        Degree of open-mindedness
    save: bool
        Option to save the plot
    filename: str
        Location where the plot is to be saved

    Returns
    -------
    Heatmap of tipping points"""

    # 0. Initialize variables
    index = [0.05 * x + 0.6 for x in range(7)]  # 0.6 till 0.9
    index.reverse()
    columns = [0.05 * x + 0.6 for x in range(7)]  # 0.6 till 0.9
    data = np.zeros((len(index), len(columns)))
    mask = np.zeros_like(data)

    # 1. Generate data about tipping points for various parameter settings
    for x in range(len(index)):
        for y in range(len(columns)):
            c = index[x]
            p = columns[y]
            prob_calculator = ProbabilityCalculator(
                competence_associate=c,
                competence_opposer=c,
                source_evaluative_capacity=p,
                degree_open_mindedness=degree_open_mindedness,
                content_evaluative_capacity=0.5,
            )
            data[x, y] = prob_calculator.find_tipping_evaluation_content()
            data[x, y] = round(data[x, y], 2)

    # 2. Plot data as heatmap
    cbar_ticks = [0.50, 0.55, 0.60, 0.65]
    df = pd.DataFrame(data, index=index, columns=columns)

    heatmap_style = PlotVars.heatmap_style(
        mask=mask, vmin=0.50, vmax=0.65, cbar_ticks=cbar_ticks
    )
    plt.rc("font", **PlotVars.font_style)
    plt.figure(figsize=PlotVars.figure_size)
    fig = sns.heatmap(df, **heatmap_style)
    bottom, top = fig.get_ylim()
    fig.set_ylim(bottom, top)

    # 3. Styling and labelling plot
    fig.set_title(
        "Content evaluation capacity required for epistemic benefits"
        "\nwhere degree of open-mindedness ($n$) is "
        f"{degree_open_mindedness}\nin a homogeneous community",
        **PlotVars.title_style,
    )
    fig.set_xlabel("Source evaluative capacity ($p_{ES}$)", **PlotVars.label_style)
    fig.set_ylabel("Competence ($p_A$ and $p_O$)", **PlotVars.label_style)

    # 4. Showing or saving plot
    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


if __name__ == "__main__":
    folder_name = "new_figures"
    os.makedirs(folder_name, exist_ok=True)

    figure_heatmap_tipping_evaluation_content(
        degree_open_mindedness=4,
        filename=f"{folder_name}/Figure_heatmap_tipping_content",
    )
