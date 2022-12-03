import os

import numpy as np
import pandas as pd

from generate_figures.plot_functions import plot_heatmap
from probability_calculator import find_tipping_evaluation_content


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
    competences = [0.05 * x + 0.6 for x in range(7)]  # 0.6 till 0.9
    competences.reverse()
    source_evaluative_capacities = [0.05 * x + 0.6 for x in range(7)]  # 0.6 till 0.9
    df = pd.DataFrame(
        index=competences, columns=source_evaluative_capacities, dtype=float
    )
    mask = pd.DataFrame(
        False, index=competences, columns=source_evaluative_capacities, dtype=bool
    )

    # 1. Generate data about tipping points for various parameter settings
    for competence in competences:
        for source_evaluative_capacity in source_evaluative_capacities:
            df.at[
                competence, source_evaluative_capacity
            ] = find_tipping_evaluation_content(
                competence_associate=competence,
                competence_opposer=competence,
                source_evaluative_capacity=source_evaluative_capacity,
                degree_open_mindedness=degree_open_mindedness,
            )
            df.at[competence, source_evaluative_capacity] = round(
                df.at[competence, source_evaluative_capacity], 2
            )

    # 2. Configure plot parameters
    cbar_ticks = [0.50, 0.55, 0.60, 0.65]
    vmin = 0.50
    vmax = 0.65
    title = (
        f"Content evaluation capacity required for epistemic benefits\nwhere "
        f"degree of open-mindedness ($n$) is {degree_open_mindedness}\nin a "
        f"homogeneous community"
    )
    xlabel = "Source evaluative capacity ($p_{ES}$)"
    ylabel = "Competence ($p_A$ and $p_O$)"

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

    figure_heatmap_tipping_evaluation_content(
        degree_open_mindedness=4,
        filename=f"{folder_name}/Figure_heatmap_tipping_content",
    )
