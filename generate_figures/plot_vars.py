import matplotlib.pyplot as plt


class PlotVars:
    """Settings for the style of the figures"""

    font_style = {"family": "Calibri", "size": 11}
    title_style = {"fontname": "Calibri", "fontsize": "11"}
    label_style = {"fontname": "Calibri", "fontsize": "11"}
    cm = 1 / 2.54  # variable used to convert inches to cm
    figure_size = (12 * cm, 10.5 * cm)
    graph_size = (16 * cm, 13 * cm)
    cmap = plt.get_cmap("Greys")

    @staticmethod
    def heatmap_style(mask, vmin, vmax, cbar_ticks):
        return {
            "annot": True,
            "cmap": PlotVars.cmap,
            "mask": mask,
            "vmin": vmin,
            "vmax": vmax,
            "linewidths": 0.1,
            "linecolor": "k",
            "cbar_kws": {"ticks": cbar_ticks, "shrink": 0.66},
            "square": True,
        }
