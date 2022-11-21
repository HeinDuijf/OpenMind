import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import binom

""" Settings for the style of the figures """
font_style = {"family": "Calibri", "size": 11}
title_style = {"fontname": "Calibri", "fontsize": "11"}
label_style = {"fontname": "Calibri", "fontsize": "11"}
cm = 1 / 2.54  # variable used to convert inches to cm
figure_size = (12 * cm, 10.5 * cm)
graph_size = (16 * cm, 13 * cm)
cmap = plt.get_cmap("Greys")


def accuracy_information(
    source_evaluative_capacity: float,
    competence_associate: float,
    competence_opposer: float,
    content_evaluation_right: float = 0.5,
    content_evaluation_wrong: float = 0.5,
):
    """Function returns the information accuracy when the agent evaluates the source
    and the content.

    The idea is to calculate the probability that the agent accepts an argument that
    survived the source evaluation, the probability that an accepted argument is right
    and the probability that an accepted argument is wrong.
    NOTE: The companion's accuracy (without content evaluation) is given by setting
    content evaluation to 0.5.

    Parameters
    ----------
    competence_associate: float
        Competence level of associates, i.e., agents with aligned interests
    competence_opposer: float
        Competence level of opposers, i.e., agents with opposed interests
    source_evaluative_capacity: float
        Level of source evaluative capacity
    content_evaluation_right: float = 0.5
        Level of content evaluative capacity for right content, i.e., content that supports the alternative that is in
        the agent's best interest
    content_evaluation_wrong: float = 0.5
        Level of content evaluative capacity for wrong content, i.e., content that does not support the alternative
        that is in the agent's best interest

    Returns
    -------
    information_accuracy: float
        The probability that an accepted piece of information supports the right alternative, i.e., the alternative is
        in the agent's best interest"""

    # 1. Calculate the probability that a piece of information from an accepted source supports the right alternative
    # and survives both source and content evaluation:
    # (The probability that the source is an associate who produced a right argument plus
    # the probability that the source is an opposer who produced a right argument) times
    # the probability that a right argument is correctly identified (and thus accepted)
    probability_right = (
        source_evaluative_capacity * competence_associate
        + (1 - source_evaluative_capacity) * (1 - competence_opposer)
    ) * content_evaluation_right

    # 2. idem for the wrong alternative
    probability_wrong = (
        source_evaluative_capacity * (1 - competence_associate)
        + (1 - source_evaluative_capacity) * competence_opposer
    ) * (1 - content_evaluation_wrong)

    # 3. Calculate information accuracy
    probability_accept = probability_right + probability_wrong
    information_accuracy = probability_right / probability_accept
    return information_accuracy


def expected_accuracy(
    degree_open_mindedness: int = 10,
    competence_opposer: float = 0.7,
    competence_associate: float = 0.6,
    source_evaluative_capacity: float = 0.5,
    content_evaluative_capacity: float = 0.5,
    probability_companion_right: float = "None",
):
    """Function returns the expected accuracy of an open-minded agent given certain input.

     Input can be either:
        a) a given degree of open-mindedness, the principal agent's competence and the companion's accuracy, or
        b) a given degree of open-mindedness, competences, and source and content evaluative capacity
        In other words, one can either input the companion's accuracy directly or this function calculates it from
        the other input

    Parameters
    ----------
    degree_open_mindedness: int
        The number of pieces of information taken into consideration
    competence_associate: float
        Competence level of associates, i.e., agents with aligned interests
    competence_opposer: float
        Competence level of opposers, i.e., agents with opposed interests
    source_evaluative_capacity: float
        Level of source evaluative capacity
    content_evaluative_capacity: float = 0.5
        Level of content evaluative capacity for right content, i.e., content that supports the alternative that is in
        the agent's best interest
    probability_companion_right: float
        The probability that a companion supports the right alternative, i.e., the alternative that is in the
        agent's best interest

    Returns
    -------
    probability_right: float
        The probability that an open-minded agent selects the right alternative, i.e., the alternative that is in
        her best interest"""

    # 0. Initialize variables
    probability_right: float = 0

    # 1. Special case of close-minded agent
    if degree_open_mindedness == 0:
        probability_right = competence_associate

    # 2. Open-minded agent
    else:
        # Calculate companion's accuracy if it has not been given as input
        if probability_companion_right == "None":
            probability_companion_right = accuracy_information(
                source_evaluative_capacity=source_evaluative_capacity,
                competence_associate=competence_associate,
                competence_opposer=competence_opposer,
                content_evaluation_right=content_evaluative_capacity,
                content_evaluation_wrong=content_evaluative_capacity,
            )
        # 2.a. Case where degree_open_mindedness is even and there can be no ties.
        if (degree_open_mindedness % 2) == 0:
            # the group that determines the individual vote is odd, so I win in two events:
            # (a) exactly half of the neighbors are correct and I am correct or
            # (b) more than half of the neighbors are correct
            probability_right = binom.pmf(
                degree_open_mindedness / 2,
                degree_open_mindedness,
                probability_companion_right,
            ) * competence_associate + binom.sf(
                degree_open_mindedness / 2,
                degree_open_mindedness,
                probability_companion_right,
            )
        # 2.b. Case where degree_open_mindedness is odd and there can be ties.
        else:
            # the group that determines the individual vote is even, so a tie occurs in two events:
            # (a) exactly half of the neighbors minus 1 are correct and I am correct
            # (b) exactly half of the neighbors plus 1 are correct and I am incorrect
            probability_tie = binom.pmf(
                (degree_open_mindedness - 1) / 2,
                degree_open_mindedness,
                probability_companion_right,
            ) * competence_associate + binom.pmf(
                (degree_open_mindedness + 1) / 2,
                degree_open_mindedness,
                probability_companion_right,
            ) * (
                1 - competence_associate
            )
            # the group that determines the individual vote is even, so I win in three events:
            # (a) exactly half of the neighbors plus 1 are correct and I am correct
            # (b) more than half of the neighbors plus 1 are correct
            # (c) there's a tie and the random choice is correct
            probability_right = (
                binom.pmf(
                    (degree_open_mindedness + 1) / 2,
                    degree_open_mindedness,
                    probability_companion_right,
                )
                * competence_associate
                + binom.sf(
                    (degree_open_mindedness + 1) / 2,
                    degree_open_mindedness,
                    probability_companion_right,
                )
                + probability_tie / 2
            )
    return probability_right


def figure_individual_calculated_accuracy(
    source_evaluative_capacity: float = "None",
    max_degree_open_mindedness: int = 20,
    save: bool = False,
    filename: str = "",
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
    if source_evaluative_capacity == "None":
        print("Error: chance_of_meeting_peer not specified.")
    elif source_evaluative_capacity > 1 or source_evaluative_capacity < 0:
        print("Error: chance_of_meeting_peer has a value below 0 or above 1.")

    # 0. Initialize variables
    xx_values = np.arange(2, max_degree_open_mindedness + 1, 2)
    competence_values = np.arange(0.6, 0.90, 0.05)
    competence_max = max(competence_values) + 0.1
    competence_range = competence_max - min(competence_values)
    colormap = plt.get_cmap("Greys")
    plt.figure(figsize=graph_size)

    # 1. Plots
    for competence in competence_values:
        color = colormap((competence_max - competence) / competence_range)
        competence = round(competence, 2)
        label = "Competence " + str(competence)
        # y_values give the expected accuracy minus competence
        y_values = [
            expected_accuracy(
                competence_associate=competence,
                competence_opposer=competence,
                source_evaluative_capacity=source_evaluative_capacity,
                degree_open_mindedness=x,
            )
            - competence
            for x in xx_values
        ]
        plt.plot(xx_values, y_values, color=color, label=label)

    # 2. Styling and labelling plot
    plt.rcParams.update(
        {"font.family": font_style["family"], "font.size": font_style["size"]}
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
    if save:
        if filename == "":
            print("Error: filename not specified.")
        else:
            plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


def figure_heatmap_source(
    degree_open_mindedness: int,
    advantage: float = 0,
    save: bool = False,
    filename: str = "",
):
    """Generates heatmap of epistemic benefit of open_mindedness for a range of competences and
    source evaluative capacities.

    Parameters
    ----------
    degree_open_mindedness: int
        Degree of open-mindedness
    advantage: float
        The competence advantage of the associating group (disadvantage is represented by negative advantage)

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
    columns = [0.6, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9]
    data = np.zeros((len(index), len(columns)))
    mask = np.zeros_like(data)

    # 1. Generate data about expected accuracy for various parameter settings
    for x in range(len(index)):
        for y in range(len(columns)):
            c = index[x]
            p = columns[y]
            data[x, y] = (
                expected_accuracy(
                    degree_open_mindedness=degree_open_mindedness,
                    competence_opposer=c - advantage,
                    competence_associate=c,
                    source_evaluative_capacity=p,
                )
                - c
            )
            if data[x, y] < 0:
                mask[x, y] = True
            data[x, y] = round(data[x, y], 2)

    # 2. Plot data as heatmap
    vmin = 0.00
    vmax = 0.15
    cbar_ticks = [0, 0.05, 0.1, 0.15]
    df = pd.DataFrame(data, index=index, columns=columns)

    heatmap_style = {
        "annot": True,
        "cmap": cmap,
        "mask": mask,
        "vmin": vmin,
        "vmax": vmax,
        "linewidths": 0.1,
        "linecolor": "k",
        "cbar_kws": {"ticks": cbar_ticks, "shrink": 0.66},
        "square": True,
    }
    plt.rc("font", **font_style)
    plt.figure(figsize=figure_size)
    fig = sns.heatmap(df, **heatmap_style)
    bottom, top = fig.get_ylim()
    fig.set_ylim(bottom, top)

    # 3. Styling and labelling plot
    titletext: str = (
        "Epistemic benefits where degree of open-mindedness ($n$) is "
        + str(degree_open_mindedness)
    )
    ylabeltext: str = ""
    if advantage > 0:
        titletext = titletext + "\n and competence advantage is " + str(advantage)
        ylabeltext = "Competence ($p_A$)"
    elif advantage < 0:
        advantage = -1 * advantage
        titletext = titletext + "\n and competence disadvantage is " + str(advantage)
        ylabeltext = "Competence ($p_A$)"
    else:
        titletext = titletext + "\n in a homogeneous community"
        ylabeltext = "Competence ($p_A$ and $p_O$)"
    fig.set_title(titletext, **title_style)
    fig.set_xlabel("Source evaluative capacity ($p_{ES}$)", **label_style)
    fig.set_ylabel(ylabeltext, **label_style)

    # 4. Showing or saving plot
    if save:
        if filename == "":
            print("Error: filename not specified.")
        else:
            plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


def find_tipping_evaluation_content(
    competence_associate: float,
    competence_opposer: float,
    source_evaluative_capacity: float,
    degree_open_mindedness: int = 4,
):
    """Function returns the tipping point for content evaluative capacity where open-mindedness becomes epistemically
    beneficial for an open-minded agent with specified degree of open-mindedness, competences and
    source evaluative capacities.

    The idea is to step-wise increase (or decrease) the content evaluative capacity until the point where
    open-mindedness is epistemically beneficial.

    Parameters
    ----------
    degree_open_mindedness: int
        Degree of open-mindedness
    competence_associate: float
        Competence level of associates, i.e., agents with aligned interests
    competence_opposer: float
        Competence level of opposers, i.e., agents with opposed interests
    source_evaluative_capacity: float
        Level of source evaluative capacity

    Returns
    -------
    evaluation_content: float
        Tipping for content evaluative capacity to become epistemically beneficial"""

    # 0. Initialize variables
    evaluation_content: float = 0.5
    step_size = 0.01
    probability_companion_right = accuracy_information(
        source_evaluative_capacity=source_evaluative_capacity,
        competence_associate=competence_associate,
        competence_opposer=competence_opposer,
        content_evaluation_right=evaluation_content,
        content_evaluation_wrong=evaluation_content,
    )
    probability_right = expected_accuracy(
        degree_open_mindedness=degree_open_mindedness,
        probability_companion_right=probability_companion_right,
        competence_associate=competence_associate,
    )
    # 1. If probability_right is lower than competence_associate, the idea is to step-wise increase the content
    # evaluative capacity until the point where open-mindedness is epistemically beneficial
    if probability_right < competence_associate:
        while probability_right < competence_associate:
            evaluation_content = evaluation_content + step_size
            probability_companion_right = accuracy_information(
                source_evaluative_capacity=source_evaluative_capacity,
                competence_associate=competence_associate,
                competence_opposer=competence_opposer,
                content_evaluation_right=evaluation_content,
                content_evaluation_wrong=evaluation_content,
            )
            probability_right = expected_accuracy(
                degree_open_mindedness=degree_open_mindedness,
                probability_companion_right=probability_companion_right,
                competence_associate=competence_associate,
            )
    # 2. If probability_right is higher than competence_associate, the idea is to step-wise decrease the content
    # evaluative capacity until the point where open-mindedness is no longer epistemically beneficial
    else:
        while probability_right > competence_associate:
            evaluation_content = evaluation_content - step_size
            probability_companion_right = accuracy_information(
                source_evaluative_capacity=source_evaluative_capacity,
                competence_associate=competence_associate,
                competence_opposer=competence_opposer,
                content_evaluation_right=evaluation_content,
                content_evaluation_wrong=evaluation_content,
            )
            probability_right = expected_accuracy(
                degree_open_mindedness=degree_open_mindedness,
                probability_companion_right=probability_companion_right,
                competence_associate=competence_associate,
            )
        evaluation_content = evaluation_content + step_size
    return round(evaluation_content, 2)


def figure_heatmap_tipping_evaluation_content(
    degree_open_mindedness: int = 4, save: bool = False, filename: str = ""
):
    """Generates heatmap of tipping points for content evaluative capacity where open-mindedness becomes epistemically
    beneficial for an open-minded agent for a range of competences and source evaluative capacities.

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
    # columns = [0.02 * x + 0.5 for x in range(11)]  # 0.5 till 0.7
    columns = [0.05 * x + 0.6 for x in range(7)]  # 0.6 till 0.9
    data = np.zeros((len(index), len(columns)))
    mask = np.zeros_like(data)

    # 1. Generate data about tipping points for various parameter settings
    for x in range(len(index)):
        for y in range(len(columns)):
            c = index[x]
            p = columns[y]
            data[x, y] = find_tipping_evaluation_content(
                competence_associate=c,
                competence_opposer=c,
                source_evaluative_capacity=p,
                degree_open_mindedness=degree_open_mindedness,
            )
            data[x, y] = round(data[x, y], 2)
    df = pd.DataFrame(data, index=index, columns=columns)

    # 2. Plot data as heatmap
    vmin = 0.50
    vmax = 0.65
    cbar_ticks = [0.50, 0.55, 0.60, 0.65]
    df = pd.DataFrame(data, index=index, columns=columns)

    heatmap_style = {
        "annot": True,
        "cmap": cmap,
        "mask": mask,
        "vmin": vmin,
        "vmax": vmax,
        "linewidths": 0.1,
        "linecolor": "k",
        "cbar_kws": {"ticks": cbar_ticks, "shrink": 0.66},
        "square": True,
    }
    plt.rc("font", **font_style)
    plt.figure(figsize=figure_size)
    fig = sns.heatmap(df, **heatmap_style)
    bottom, top = fig.get_ylim()
    fig.set_ylim(bottom, top)

    # 3. Styling and labelling plot
    fig.set_title(
        "Content evaluation capacity required for epistemic benefits"
        "\nwhere degree of open-mindedness ($n$) is "
        + str(degree_open_mindedness)
        + "\nin a homogeneous community",
        **title_style
    )
    fig.set_xlabel("Source evaluative capacity ($p_{ES}$)", **label_style)
    fig.set_ylabel("Competence ($p_A$ and $p_O$)", **label_style)

    # 4. Showing or saving plot
    if save:
        if filename == "":
            print("Error: filename not specified.")
        else:
            plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


def figure_heatmap_content_only(
    degree_open_mindedness: int = 4,
    advantage: float = 0,
    save: bool = False,
    filename: str = "",
):
    """Generates heatmap of epistemic benefit of open_mindedness when only practicing content evaluation
    for a range of competences and content evaluative capacities.

    Parameters
    ----------
    degree_open_mindedness: int
        Degree of open-mindedness
    advantage: float
        The competence advantage of the associating group (disadvantage is represented by negative advantage)

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
    # columns = [0.6, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9]
    columns = [0.5, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8]
    data = np.zeros((len(index), len(columns)))
    mask = np.zeros_like(data)

    # 1. Generate data about expected accuracy for various parameter settings
    for x in range(len(index)):
        for y in range(len(columns)):
            c = index[x]
            p = columns[y]
            data[x, y] = (
                expected_accuracy(
                    degree_open_mindedness=degree_open_mindedness,
                    competence_associate=c,
                    competence_opposer=c - advantage,
                    source_evaluative_capacity=0.5,
                    content_evaluative_capacity=p,
                )
                - c
            )
            if data[x, y] < 0:
                mask[x, y] = True
            data[x, y] = round(data[x, y], 2)
    df = pd.DataFrame(data, index=index, columns=columns)

    # 2. Plot data as heatmap
    vmin = 0.00
    vmax = 0.30
    cbar_ticks = [0, 0.1, 0.20, 0.30]
    heatmap_style = {
        "annot": True,
        "cmap": cmap,
        "mask": mask,
        "vmin": vmin,
        "vmax": vmax,
        "linewidths": 0.1,
        "linecolor": "k",
        "cbar_kws": {"ticks": cbar_ticks, "shrink": 0.66},
        "square": True,
    }
    plt.rc("font", **font_style)
    plt.figure(figsize=figure_size)
    fig = sns.heatmap(df, **heatmap_style)
    bottom, top = fig.get_ylim()
    fig.set_ylim(bottom, top)

    # 3. Styling and labelling plot
    titletext: str = (
        "Epistemic benefits of only content evaluation where degree of \nopen-mindedness ($n$) is "
        + str(degree_open_mindedness)
    )
    ylabeltext: str = ""
    if advantage > 0:
        titletext = titletext + "\n and competence advantage is " + str(advantage)
        ylabeltext = "Competence ($p_A$)"
    elif advantage < 0:
        advantage = -1 * advantage
        titletext = titletext + "\n and competence disadvantage is " + str(advantage)
        ylabeltext = "Competence ($p_A$)"
    else:
        titletext = titletext + " in a homogeneous community"
        ylabeltext = "Competence ($p_A$ and $p_O$)"
    fig.set_title(titletext, **title_style)
    fig.set_xlabel("Content evaluative capacity ($p_{EC}$)", **label_style)
    fig.set_ylabel(ylabeltext, **label_style)

    # 4. Showing or saving plot
    if save:
        if filename == "":
            print("Error: filename not specified.")
        else:
            plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


def figure_added_accuracy_content(save: bool = False, filename: str = ""):
    """Generates heatmap of the added accuracy when practicing not only source evaluation but also content evaluation
    for a range of competences and source evaluative capacities.

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
    # columns = [0.6, 0.65, 0.70, 0.75, 0.8, 0.85, 0.9]
    columns = [
        round(0.55 + 0.05 * x, 2) for x in range(6)
    ]  # values for content evaluation
    data = np.zeros((len(index), len(columns)))
    mask = np.zeros_like(data)

    # 1. Generate data about expected accuracy for various parameter settings
    for x in range(len(index)):
        for y in range(len(columns)):
            companion_accuracy = index[x]
            content_evaluation = columns[y]
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
    vmin = 0.00
    vmax = 0.30
    cbar_ticks = [0, 0.1, 0.2, 0.3]
    heatmap_style = {
        "annot": True,
        "cmap": cmap,
        "mask": mask,
        "vmin": vmin,
        "vmax": vmax,
        "linewidths": 0.1,
        "linecolor": "k",
        "cbar_kws": {"ticks": cbar_ticks, "shrink": 0.66},
        "square": True,
    }
    plt.rc("font", **font_style)
    plt.figure(figsize=figure_size)
    fig = sns.heatmap(df, **heatmap_style)
    bottom, top = fig.get_ylim()
    fig.set_ylim(bottom, top)

    # 3. Styling and labelling plot
    fig.set_title(
        "Added epistemic value of content evaluation ($p_I$ minus $p_C$)", **title_style
    )
    fig.set_xlabel("Content evaluative capacity ($p_{EC}$)", **label_style)
    fig.set_ylabel(
        "Companion's accuracy ($p_C$)\n (without content evaluation)", **label_style
    )

    # 4. Showing or saving plot
    if save:
        if filename == "":
            print("Error: filename not specified.")
        else:
            plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


def save_all_figures():
    """Saves all figures used in the paper titled 'When should one be open-minded?' in the folder 'figures'.

    Returns
    -------
    All figures in the folder 'figures'"""
    os.makedirs("figures", exist_ok=True)

    figure_heatmap_source(
        degree_open_mindedness=2,
        advantage=0,
        save=True,
        filename="figures/Figure_heatmap_source_evaluation_n2",
    )
    figure_heatmap_source(
        degree_open_mindedness=4,
        advantage=0,
        save=True,
        filename="figures/Figure_heatmap_source_evaluation_n4",
    )
    figure_added_accuracy_content(
        save=True, filename="figures/Figure_added_accuracy_content"
    )
    figure_heatmap_content_only(
        degree_open_mindedness=4,
        save=True,
        filename="figures/Figure_heatmap_content_only_n4",
    )
    figure_heatmap_tipping_evaluation_content(
        degree_open_mindedness=4,
        save=True,
        filename="figures/Figure_heatmap_tipping_content",
    )
    figure_individual_calculated_accuracy(
        source_evaluative_capacity=0.7,
        max_degree_open_mindedness=20,
        save=True,
        filename="figures/Figure_graph_70_zoom",
    )
    figure_individual_calculated_accuracy(
        source_evaluative_capacity=0.3,
        max_degree_open_mindedness=50,
        save=True,
        filename="figures/Figure_graph_30",
    )
    figure_individual_calculated_accuracy(
        source_evaluative_capacity=1.0,
        max_degree_open_mindedness=50,
        save=True,
        filename="figures/Figure_graph_ 100",
    )


if __name__ == "__main__":
    """Save all figures :)"""
    save_all_figures()
