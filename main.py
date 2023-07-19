import os

from generate_figures.heatmap_added_accuracy_content import (
    figure_heatmap_added_accuracy_content,
)
from generate_figures.heatmap_content_only import figure_heatmap_content_only
from generate_figures.heatmap_source import figure_heatmap_source
from generate_figures.heatmap_tipping_evaluation_content import (
    figure_heatmap_tipping_evaluation_content,
)
from generate_figures.individual_calculated_accuracy import (
    figure_individual_calculated_accuracy,
)

if __name__ == "__main__":
    """Saves all figures used in the paper titled 'When should one be open-minded?'
    in the folder 'new_figures'.

    Returns
    -------
    All figures in the folder 'new_figures'"""
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
    figure_heatmap_added_accuracy_content(
        filename=f"{folder_name}/Figure_added_accuracy_content"
    )
    figure_heatmap_content_only(
        degree_open_mindedness=2,
        filename=f"{folder_name}/Figure_heatmap_content_only_n2",
    )
    figure_heatmap_content_only(
        degree_open_mindedness=4,
        filename=f"{folder_name}/Figure_heatmap_content_only_n4",
    )
    figure_heatmap_tipping_evaluation_content(
        degree_open_mindedness=2,
        filename=f"{folder_name}/Figure_heatmap_tipping_content_n2",
    )
    figure_heatmap_tipping_evaluation_content(
        degree_open_mindedness=4,
        filename=f"{folder_name}/Figure_heatmap_tipping_content_n4",
    )
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
