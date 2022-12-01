import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from generate_figures.plot_vars import PlotVars
from probability_calculator import ProbabilityCalculator


def figure_heatmap_content_only(
    degree_open_mindedness: int = 4,
    advantage: float = 0,
    filename: str = None,
):
    """Generates heatmap of epistemic benefit of open_mindedness when only practicing
    content evaluation for a range of competences and content evaluative capacities.

    Parameters
    ----------
    degree_open_mindedness: int
        Degree of open-mindedness
    advantage: float
        The competence advantage of the associating group (disadvantage is represented
        by negative advantage)

    save: bool
        Option to save the plot
    filename: str
        Location where the plot is to be saved

    Returns
    -------
    Heatmap of epistemic benefit"""

    # 0. Initialize variables
    index = [0.6, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9]
    index.reverse()
    columns = [0.5, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8]
    data = np.zeros((len(index), len(columns)))
    mask = np.zeros_like(data)

    # 1. Generate data about expected accuracy for various parameter settings
    for x, c in enumerate(index):
        for y, p in enumerate(columns):
            prob_calculator = ProbabilityCalculator(
                degree_open_mindedness=degree_open_mindedness,
                competence_associate=c,
                competence_opposer=c - advantage,
                source_evaluative_capacity=0.5,
                content_evaluative_capacity=p,
            )
            data[x, y] = prob_calculator.compute_probability_right() - c

            if data[x, y] < 0:
                mask[x, y] = True
            data[x, y] = round(data[x, y], 2)
    df = pd.DataFrame(data, index=index, columns=columns)

    # 2. Plot data as heatmap
    cbar_ticks = [0, 0.1, 0.20, 0.30]
    heatmap_style = PlotVars.heatmap_style(
        mask, vmin=0.00, vmax=0.30, cbar_ticks=cbar_ticks
    )
    plt.rc("font", **PlotVars.font_style)
    plt.figure(figsize=PlotVars.figure_size)
    fig = sns.heatmap(df, **heatmap_style)
    bottom, top = fig.get_ylim()
    fig.set_ylim(bottom, top)

    # 3. Styling and labelling plot
    titletext: str = (
        "Epistemic benefits of only content evaluation where "
        + f"degree of \nopen-mindedness($n$) is {degree_open_mindedness}"
    )

    ylabeltext: str = ""
    if advantage > 0:
        titletext = f"{titletext}\n and competence advantage is {advantage}"
        ylabeltext = "Competence ($p_A$)"
    elif advantage < 0:
        advantage = -1 * advantage
        titletext = f"{titletext}\n and competence disadvantage is {advantage}"
        ylabeltext = "Competence ($p_A$)"
    else:
        titletext = f"{titletext} in a homogeneous community"
        ylabeltext = "Competence ($p_A$ and $p_O$)"
    fig.set_title(titletext, **PlotVars.title_style)
    fig.set_xlabel("Content evaluative capacity ($p_{EC}$)", **PlotVars.label_style)
    fig.set_ylabel(ylabeltext, **PlotVars.label_style)

    # 4. Showing or saving plot
    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


if __name__ == "__main__":
    folder_name = "new_figures"
    os.makedirs(folder_name, exist_ok=True)

    figure_heatmap_content_only(
        degree_open_mindedness=4,
        save=True,
        filename="figures/Figure_heatmap_content_only_n4",
    )
