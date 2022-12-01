import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from generate_figures.plot_vars import PlotVars


def figure_added_accuracy_content(filename: str = None):
    """Generates heatmap of the added accuracy when practicing not only source
    evaluation but also content evaluation for a range of competences and
    source evaluative capacities.

    Parameters
    ----------
    save: bool
        Option to save the plot
    filename: str
        Location where the plot is to be saved

    Returns
    -------
    Heatmap of added accuracy"""

    # 0. Initialize variables
    index = [
        round(0.55 + 0.05 * y, 2) for y in range(6)
    ]  # values for old companion's accuracy
    index.reverse()

    columns = [
        round(0.55 + 0.05 * x, 2) for x in range(6)
    ]  # values for content evaluation
    data = np.zeros((len(index), len(columns)))
    mask = np.zeros_like(data)

    # 1. Generate data about expected accuracy for various parameter settings
    for x, companion_accuracy in enumerate(index):
        for y, content_evaluation in enumerate(columns):
            data[x, y] = (
                companion_accuracy
                * content_evaluation
                / (
                    companion_accuracy * content_evaluation
                    + (1 - companion_accuracy) * (1 - content_evaluation)
                )
                - companion_accuracy
            )
            data[x, y] = round(data[x, y], 2)
    df = pd.DataFrame(data, index=index, columns=columns)

    # 2. Plot data as heatmap
    cbar_ticks = [0, 0.1, 0.2, 0.3]
    heatmap_style = PlotVars.heatmap_style(
        mask, vmin=0.00, vmax=0.30, cbar_ticks=cbar_ticks
    )

    plt.rc("font", **PlotVars.font_style)
    plt.figure(figsize=PlotVars.figure_size)
    fig = sns.heatmap(df, **heatmap_style)
    bottom, top = fig.get_ylim()
    fig.set_ylim(bottom, top)

    # 3. Styling and labelling plot
    fig.set_title(
        "Added epistemic value of content evaluation ($p_I$ minus $p_C$)",
        **PlotVars.title_style,
    )
    fig.set_xlabel("Content evaluative capacity ($p_{EC}$)", **PlotVars.label_style)
    fig.set_ylabel(
        "Companion's accuracy ($p_C$)\n (without content evaluation)",
        **PlotVars.label_style,
    )

    # 4. Showing or saving plot
    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


if __name__ == "__main__":
    folder_name = "new_figures"
    os.makedirs(folder_name, exist_ok=True)

    figure_added_accuracy_content(
        filename="{folder_name}/Figure_added_accuracy_content"
    )
