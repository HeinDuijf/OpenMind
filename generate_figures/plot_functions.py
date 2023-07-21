import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import cm
from matplotlib.colors import ListedColormap

# Global style variables
font_style = {"family": "Calibri", "size": 11}
title_style = {"fontname": "Calibri", "fontsize": "11"}
label_style = {"fontname": "Calibri", "fontsize": "11"}
centi = 1 / 2.54  # variable used to convert inches to centimeters
heatmap_size = (12 * centi, 10.5 * centi)
lineplot_size = (16 * centi, 13 * centi)
cmap_heat = cm.get_cmap("Greys")
cmap_line = ListedColormap(cm.get_cmap("Greys_r")(np.linspace(0.2, 0.8)))
cmap_line_r = ListedColormap(cm.get_cmap("Greys")(np.linspace(0.2, 0.8)))


def plot_heatmap(
    dataframe,
    title,
    ylabel,
    xlabel,
    vmin,
    vmax,
    mask,
    cbar_ticks,
    filename: str = None,
):
    heatmap_style: dict = {
        "annot": True,
        "cmap": cmap_heat,
        "mask": mask,
        "vmin": vmin,
        "vmax": vmax,
        "linewidths": 0.1,
        "linecolor": "k",
        "cbar_kws": {"ticks": cbar_ticks, "shrink": 0.66},
        "square": True,
    }

    plt.rc("font", **font_style)
    plt.figure(figsize=heatmap_size)
    fig = sns.heatmap(dataframe, **heatmap_style)
    bottom, top = fig.get_ylim()
    fig.set_ylim(bottom, top)

    # 3. Styling and labelling plot
    fig.set_title(title, title_style)
    fig.set_xlabel(xlabel, label_style)
    fig.set_ylabel(ylabel, label_style)

    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


def plot_lines(
    dataframe, title, xlabel, ylabel, xticks, xlim, filename: str = None,
):
    plt.rc("font", **font_style)
    dataframe.plot(
        kind="line",
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=lineplot_size,
        colormap=cmap_line,
        xticks=xticks,
        xlim=xlim,
    )
    competences = dataframe.columns
    legend = [f"Competence {competence}" for competence in competences]
    plt.legend(legend, title="Competences ($p_R$ and $p_U$)", loc="lower right", ncol=2)
    plt.axhline(0, color="k", linewidth=1)

    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()
