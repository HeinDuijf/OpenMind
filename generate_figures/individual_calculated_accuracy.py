import os

import numpy as np
import pandas as pd
from accuracy_calculator import Agent

from generate_figures.plot_functions import plot_lines


def figure_individual_calculated_accuracy(
    source_evaluative_capacity: float,
    max_degree_open_mindedness: int = 20,
    filename: str = None,
):
    """Generates plot of individual accuracy depending on source_evaluative_capacity.

    Parameters
    ----------
    source_evaluative_capacity: float
        Level of source evaluative capacity
    max_degree_open_mindedness: int
        The range of the degree_open_mindedness, i.e., of the x-axis
    save: bool
        Option to save the plot
    filename: str
        Location where the plot is to be saved

    Returns
    -------
    Plot of individual accuracy"""
    # 0. Initialize variables
    degrees_of_open_mindedness = np.arange(
        2, max_degree_open_mindedness + 1, 2, dtype=int
    )
    competences = np.arange(0.6, 0.9, 0.05)
    competences = np.round(competences, 2)

    # 1. Generate data for plotting
    df = pd.DataFrame(index=degrees_of_open_mindedness, columns=competences)

    for degree_of_open_mindedness in degrees_of_open_mindedness:
        for competence in competences:
            df.at[degree_of_open_mindedness, competence] = Agent(
                degree_open_mindedness=degree_of_open_mindedness,
                competence_reliable_group=competence,
                competence_unreliable_group=competence,
                source_evaluative_capacity=source_evaluative_capacity,
            ).benefit_open_mind()

    # 2. Configure plot parameters
    if max_degree_open_mindedness != 50:
        xticks = np.arange(0, max_degree_open_mindedness + 1, 2)
    else:
        xticks = np.arange(0, 51, 5)
    xlim = [0, max_degree_open_mindedness]
    xlabel = "Degree of open-mindedness ($n$)"
    ylabel = "Epistemic benefits"
    title = (
        f"Epistemic benefits where the source evaluative capacity ($p_{{ES}}$) is"
        f" {source_evaluative_capacity}\n"
    )

    # 3. Line plot
    plot_lines(
        dataframe=df,
        xticks=xticks,
        xlim=xlim,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        filename=filename,
    )


if __name__ == "__main__":
    folder_name = "new_figures"
    os.makedirs(folder_name, exist_ok=True)

    figure_individual_calculated_accuracy(
        source_evaluative_capacity=0.7,
        max_degree_open_mindedness=20,
        filename=f"{folder_name}/Figure_graph_70_zoom",
    )
    figure_individual_calculated_accuracy(
        source_evaluative_capacity=0.3,
        max_degree_open_mindedness=50,
        filename=f"{folder_name}/Figure_graph_30",
    )
    figure_individual_calculated_accuracy(
        source_evaluative_capacity=1.0,
        max_degree_open_mindedness=50,
        filename=f"{folder_name}/Figure_graph_ 100",
    )
