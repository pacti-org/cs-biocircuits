from typing import List
import numpy as np
from matplotlib.figure import Figure as MplFigure
import matplotlib.pyplot as plt
from typing import List
import matplotlib.pyplot as plt
from matplotlib.figure import Figure as MplFigure
import matplotlib as mpl

def stitch_mpl_plots(plots: List[MplFigure], show: bool = True, ax: mpl.pyplot.Axes = None, **kwargs) -> MplFigure:
    """
    Stitch multiple matplotlib figures to plot them together.
    Keyword arguments are passed to matplotlib.
    Arguments:
        * plots (List[MplFigure]): A list of MplFigure objects to stitch together
        * show (bool): To display the resulting plot, set to `True, otherwise `False`
        * ax (matplotlib.pyplot.Axes): Use this Axes object to plot the stitched figure. 
    Returns:
        * stitched_figure (MplFigure): The stitched plot as a MplFigure.
    Raises:
        ValueError: Arguments failed sanity checks
        TypeError: Unsupported patch type.
    """
    # Initialize variables to hold limits
    xlims = []
    ylims = []

    # Loop through each figure and extract the axis limits
    for fig in plots:
        # Get the axis object from the figure
        fig_ax = fig.axes[0]
        
        # Append the x and y limits to the corresponding list
        xlims.append(fig_ax.get_xlim())
        ylims.append(fig_ax.get_ylim())

    # Find the overall limits
    xmin = min([x[0] for x in xlims])
    xmax = max([x[1] for x in xlims])
    ymin = min([y[0] for y in ylims])
    ymax = max([y[1] for y in ylims])

    # Create the stitched figure with the overall limits
    figsize = kwargs.get("figsize", (4,3))
    if type(figsize) is not tuple:
        raise ValueError("If `figsize` argument is used, \
                         a tuple must be passed in to set the figure size.")
    stitched_figure = plt.figure(figsize=figsize)
    if not ax:
        ax = stitched_figure.add_axes([0, 0, 1, 1])
    for fig in plots:
        # Get the axis object from the figure
        ax_to_add = fig.axes[0]
        
        # Loop through each rectangle in the axis and add it to the stitched figure
        for patch in ax_to_add.patches:
            if isinstance(patch, mpl.patches.Rectangle):
                # For rectangles, use get_x(), get_y(), get_width() and get_height() methods
                new_patch = mpl.patches.Rectangle((patch.get_x(), patch.get_y()), patch.get_width(), patch.get_height(),
                                                  fill=True, edgecolor=patch.get_edgecolor(),
                                                  facecolor=patch.get_facecolor(), linewidth=patch.get_linewidth())
            elif isinstance(patch, mpl.patches.Polygon):
                # For polygons, use get_xy() method to get a list of (x, y) tuples representing vertices
                vertices = patch.get_xy()
                width = max(vertices[:, 0]) - min(vertices[:, 0])
                height = max(vertices[:, 1]) - min(vertices[:, 1])
                new_patch = mpl.patches.Polygon(vertices, fill=True, edgecolor=patch.get_edgecolor(), 
                                                facecolor=patch.get_facecolor(),
                                                linewidth=patch.get_linewidth())
            else:
                raise TypeError("Unsupported patch type")
            ax.add_patch(new_patch)



    # Set the overall limits on the stitched figure
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # Set the labels and title on the stitched figure
    ax.set_xlabel(plots[0].axes[0].get_xlabel())
    ax.set_ylabel(plots[0].axes[0].get_ylabel())
    stitched_figure.suptitle(plots[0].get_axes()[0].get_title())

    # Show the stitched figure if desired
    if show:
        plt.show()

    return stitched_figure, ax
