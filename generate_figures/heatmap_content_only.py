import os

import pandas as pd
from accuracy_calculator import Agent

from generate_figures.plot_functions import plot_heatmap


def figure_heatmap_content_only(
    degree_open_mindedness: int = 4, advantage: float = 0, filename: str = None,
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
    competences = [0.6, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9]
    competences.reverse()
    content_evaluative_capacities = [0.5, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8]
    df = pd.DataFrame(
        index=competences, columns=content_evaluative_capacities, dtype=float
    )
    mask = pd.DataFrame(
        False, index=competences, columns=content_evaluative_capacities, dtype=bool
    )

    # 1. Generate data about expected accuracy for various parameter settings
    for competence in competences:
        for content_evaluative_capacity in content_evaluative_capacities:
            benefit_open_mind = Agent(
                degree_open_mindedness=degree_open_mindedness,
                competence_reliable_group=competence,
                competence_unreliable_group=competence - advantage,
                source_evaluative_capacity=0.5,
                content_evaluative_capacity=content_evaluative_capacity,
            ).benefit_open_mind()
            df.at[competence, content_evaluative_capacity] = round(benefit_open_mind, 2)

            if df.at[competence, content_evaluative_capacity] <= 0:
                mask.at[competence, content_evaluative_capacity] = True

    # 2. Configure plot parameters
    cbar_ticks = [0, 0.1, 0.20, 0.30]
    vmin = 0.00
    vmax = 0.30
    title = (
        f"Epistemic benefits of only content evaluation where degree of "
        f"\nopen-mindedness ($n$) is {degree_open_mindedness}"
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
        title = f"{title} in a homogeneous community"
        ylabel = "Competence ($p_R$ and $p_U$)"
    xlabel = "Content evaluative capacity ($p_{EC}$)"

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

    figure_heatmap_content_only(
        degree_open_mindedness=4,
        filename=f"{folder_name}/Figure_heatmap_content_only_n4",
    )
