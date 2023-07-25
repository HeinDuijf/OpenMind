import os

import numpy as np
import pandas as pd
from accuracy_calculator import Agent

from generate_figures.plot_functions import plot_heatmap


def figure_heatmap_added_accuracy_content(filename: str = None):
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
    companion_accuracies = [round(0.55 + 0.05 * y, 2) for y in range(6)]
    companion_accuracies.reverse()
    content_evaluative_capacities = [round(0.55 + 0.05 * x, 2) for x in range(6)]
    df = pd.DataFrame(
        index=companion_accuracies, columns=content_evaluative_capacities, dtype=float
    )
    mask = np.zeros_like(df)

    # 1. Generate data about expected accuracy for various parameter settings
    for companion_accuracy in companion_accuracies:
        for content_evaluative_capacity in content_evaluative_capacities:
            information_accuracy = Agent(
                trustee_accuracy=companion_accuracy,
                content_evaluative_capacity=content_evaluative_capacity,
            ).accuracy_information()
            df.at[companion_accuracy, content_evaluative_capacity] = round(
                information_accuracy - companion_accuracy, 2
            )

    # 2. Configure plot parameters
    cbar_ticks = [0, 0.1, 0.2, 0.3]
    vmin = 0.00
    vmax = 0.30
    title = "Added epistemic value of content evaluation ($p_I$ minus $p_T$)"
    xlabel = "Content evaluative capacity ($p_{EC}$)"
    ylabel = "Trustee's accuracy ($p_T$)\n (without content evaluation)"

    # 3. Plot heatmap
    plot_heatmap(
        dataframe=df,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        vmin=vmin,
        vmax=vmax,
        mask=mask,
        cbar_ticks=cbar_ticks,
        filename=filename,
    )


if __name__ == "__main__":
    folder_name = "new_figures"
    os.makedirs(folder_name, exist_ok=True)

    figure_heatmap_added_accuracy_content(
        filename=f"{folder_name}/Figure_added_accuracy_content"
    )
