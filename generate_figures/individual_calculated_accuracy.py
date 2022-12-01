import os

import matplotlib.pyplot as plt
import numpy as np

from generate_figures.plot_vars import PlotVars
from probability_calculator import ProbabilityCalculator


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
    # Error handling
    if source_evaluative_capacity > 1 or source_evaluative_capacity < 0:
        raise ValueError(
            f"Source evaluation capacity has value {source_evaluative_capacity}"
            ", it should between 0 and 1."
        )

    # 0. Initialize variables
    xx_values = np.arange(2, max_degree_open_mindedness + 1, 2)
    competence_values = np.arange(0.6, 0.90, 0.05)
    competence_max = max(competence_values) + 0.1
    competence_range = competence_max - min(competence_values)
    plt.figure(figsize=PlotVars.graph_size)

    # 1. Plots
    for competence in competence_values:
        color = PlotVars.cmap((competence_max - competence) / competence_range)
        competence = round(competence, 2)
        label = "Competence " + str(competence)
        # y_values give the expected accuracy minus competence
        y_values = [
            ProbabilityCalculator(
                competence_associate=competence,
                competence_opposer=competence,
                source_evaluative_capacity=source_evaluative_capacity,
                degree_open_mindedness=x,
            ).compute_probability_right()
            - competence
            for x in xx_values
        ]
        plt.plot(xx_values, y_values, color=color, label=label)

    # 2. Styling and labelling plot
    plt.rcParams.update(
        {
            "font.family": PlotVars.font_style["family"],
            "font.size": PlotVars.font_style["size"],
        }
    )
    plt.title(
        "Epistemic benefits where the source evaluative capacity ($p_{ES}$) is "
        + str(source_evaluative_capacity)
        + "\n"
    )
    plt.ylabel("Epistemic benefits")
    plt.xlabel("Degree of open-mindedness ($n$)")
    if max_degree_open_mindedness != 50:
        plt.xticks(np.arange(0, max_degree_open_mindedness + 1, 2))
    else:
        plt.xticks(np.arange(0, 51, 5))
    plt.axhline(0, color="k", linewidth=1)
    plt.xlim([0, max_degree_open_mindedness])
    plt.legend(loc="lower right")

    # 3. Showing or saving plot
    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


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
