import os

import pandas as pd
from accuracy_calculator import Agent

from generate_figures.plot_functions import plot_heatmap


def figure_heatmap_source(
    degree_open_mindedness: int, advantage: float = 0, filename: str = None,
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
    competences = [0.6, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9]
    competences.reverse()
    source_evaluative_capacities = [0.6, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9]
    df = pd.DataFrame(
        index=competences, columns=source_evaluative_capacities, dtype=float
    )
    mask = pd.DataFrame(
        False, index=competences, columns=source_evaluative_capacities, dtype=bool,
    )

    # 1. Generate data about expected accuracy for various parameter settings
    for competence in competences:
        for source_evaluative_capacity in source_evaluative_capacities:
            benefit_open_mind = Agent(
                degree_open_mindedness=degree_open_mindedness,
                competence_opposer=competence - advantage,
                competence_associate=competence,
                source_evaluative_capacity=source_evaluative_capacity,
            ).benefit_open_mind()
            df.at[competence, source_evaluative_capacity] = round(benefit_open_mind, 2)
            if df.at[competence, source_evaluative_capacity] <= 0:
                mask.at[competence, source_evaluative_capacity] = True
    # df = pd.DataFrame(data, index=competences, columns=source_evaluative_capacities)

    # 2. Configure plot parameters
    cbar_ticks = [0, 0.05, 0.1, 0.15]
    vmin = 0.00
    vmax = 0.15
    title = (
        f"Epistemic benefits where degree of open-mindedness ($n$) is "
        f"{degree_open_mindedness}"
    )
    ylabel: str = ""
    if advantage > 0:
        title = f"{title}\n and competence advantage is {advantage}"
        ylabel = "Competence ($p_R$)"
    elif advantage < 0:
        advantage = -1 * advantage
        title = f"{title}\n and competence disadvantage is {advantage}"
        ylabel = "Competence ($p_R$)"
    else:
        title = f"{title}\n in a homogeneous community"
        ylabel = "Competence ($p_R$ and $p_U$)"
    xlabel = "Source evaluative capacity ($p_{ES}$)"

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
