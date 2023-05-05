import matplotlib.pyplot as plt
import numpy as np
import copy
from typing import Union
from pacti.iocontract import IoContract
from pacti.terms.polyhedra import PolyhedralContract

def display_sensor_contracts(
    sensor_input: str = "u",
    output: str = "y",
    leak: float = 0.0,
    start: float = 0.0,
    K: float = 0.0,
    ymax_lin: float = 0.0,
    xlim_min: float = 0.0,
    xlim_max: float = 0.0,
    ylim_min: float = 0.0,
    ylim_max: float = 0.0,
    show: bool = True,
    ax: Union[plt.Axes, None] = None,
    **kwargs
) -> plt.Axes:
    """
    Plot three contracts: lag, linear, saturation on a 2-D plane

    Args:
        sensor_input (str, optional): Sensor input. Defaults to "u".
        output (str, optional): Sensor output. Defaults to "y".
        leak (float, optional): Leak value. Defaults to 0.0.
        start (float, optional): Start value at which linear regime starts.
                                 Defaults to 0.0.
        K (float, optional): Activation constant, also used as end of
                             linear regime. Defaults to 0.0.
        ymax_lin (float, optional): Maximum value of output at the end of
                                    linear regime. Defaults to 0.0.
        xlim_min (float, optional): Minimum limit for plot X axis.
                                    Defaults to 0.0.
        xlim_max (float, optional): Maximum limit for plot axes.
                                    Defaults to 0.0.
        ylim_min (float, optional): Minimum limit for plot Y axis.
                                    Defaults to 0.0.
        ylim_max (float, optional): Maximum limit for plot Y axis.
                                    Defaults to 0.0.
        show (bool, optional): Plot is displayed if True, and hidden if False.
                               Defaults to True.
        ax (Union[plt.Axes, None], optional): Matplotlib Axes object
                                              to use for plotting.
                                              Defaults to None.

    Returns:
        plt.Axes: The matplotlib.pyplot.Axes object
                  that consists of the figure data
    """
    if ax is None:
        _, ax = plt.subplots()
    lw = kwargs.get("lw", 2)
    slope = (ymax_lin - leak) / (K - start)
    intercept = leak - slope * start
    ax.hlines(y=leak, xmin=xlim_min, xmax=start, color="r",
              lw=2, ls="--", label="OFF")
    ax.axvline(x=start, ls="dotted", color="k")
    ax.plot(
        np.linspace(start, K, 2),
        slope * np.array(np.linspace(start, K, 2)) + intercept,
        color="#006400", lw=2, label="Linear"
    )
    ax.hlines(y=ymax_lin, xmin=K, xmax=xlim_max,
              color="blue", lw=lw, ls="--", label="Saturation")
    ax.axvline(x=K, ls="dotted", color="k")
    ax.set_xlabel(sensor_input, fontsize=14)
    ax.set_xscale("log")
    ax.set_xlim(xlim_min, xlim_max)
    ax.set_ylabel(output, fontsize=14)
    ax.set_yscale("log")
    ax.set_ylim(ylim_min, ylim_max)
    ax.legend()
    if show:
        plt.show()
    return ax


def remove_quantization_errors(contract: IoContract,
                               tolerance: float = 1e-4) -> IoContract:
    """Removes quantization errors that creep in Pacti computations
       All terms that have coefficients lower than the specified `tolerance`
       are removed.
    Args:
        contract (IoContract): A contract (`pacti.iocontract.IoContract`)
                               object
        tolerance (float, optional): The tolerance value. Defaults to 1e-4.

    Returns:
        IoContract: Updated contract (`pacti.iocontract.IoContract`)
    """
    from_contract = copy.deepcopy(contract)
    index = 0
    # Remove quantization error from assumptions
    for t_i in list(from_contract.a.terms):
        all_coeff = 0
        for _, coeff in t_i.variables.items():
            all_coeff += np.abs(coeff)
        if all_coeff < tolerance:
            from_contract.a.terms.remove(t_i)
        index += 1
    # Remove quantization error from guarantees
    index = 0
    for t_i in list(from_contract.g.terms):
        all_coeff = 0
        for _, coeff in t_i.variables.items():
            all_coeff += np.abs(coeff)
        if all_coeff < tolerance:
            from_contract.g.terms.remove(t_i)
        index += 1
    return from_contract


# +
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

# +
import numpy as np
import matplotlib.pyplot as plt

def display_sensor_contracts_range(
    sensor_input: str = "u",
    output: str = "y",
    leak_max: float = 0.0,
    leak_min: float = 0.0,
    start: float = 0.0,
    K: float = 0.0,
    ymax_lin_max: float = 0.0,
    ymax_lin_min: float = 0.0,
    xlim_min: float = 0.0,
    xlim_max: float = 0.0,
    ylim_min: float = 0.0,
    ylim_max: float = 0.0,
    show: bool = True,
    ax: plt.Axes = None,
    **kwargs,  # allow any additional keyword arguments to be passed to the function
) -> plt.Axes:

    if ax is None:
        _, ax = plt.subplots()
    lw = kwargs.get("lw", 2)
    alpha = kwargs.get("alpha", 0.2)
    slope1 = (ymax_lin_max - leak_max) / (K - start)
    slope2 = (ymax_lin_min - leak_min) / (K - start)
    intercept1 = leak_max - slope1 * start
    intercept2 = leak_min - slope2 * start

    ax.hlines(y=leak_min, xmin=xlim_min, xmax=start, color="r",
              lw=lw, ls="--")
    ax.hlines(y=leak_max, xmin=xlim_min, xmax=start, color="r",
              lw=lw, ls="--")
    ax.fill_betweenx([leak_min, leak_max], xlim_min, start, alpha=alpha, color="red", label="OFF Region")
    ax.axvline(x=start, ls="dotted", color="k")
    ax.plot(
        np.linspace(start, K, 2),
        slope1 * np.array(np.linspace(start, K, 2)) + intercept1,
        color="#006400", lw=lw
    )
    ax.plot(
        np.linspace(start, K, 2),
        slope2 * np.array(np.linspace(start, K, 2)) + intercept2,
        color="#006400", lw=lw
    )
    ax.fill_between(np.linspace(start, K, 2),
                    slope1 * np.array(np.linspace(start, K, 2)) + intercept1,
                    slope2 * np.array(np.linspace(start, K, 2)) + intercept2,
                    alpha=alpha, color='#006400', label="Linear Region")

    ax.hlines(y=ymax_lin_max, xmin=K, xmax=xlim_max,
              color="blue", lw=lw, ls="--")
    ax.hlines(y=ymax_lin_min, xmin=K, xmax=xlim_max,
              color="blue", lw=lw, ls="--")
    ax.fill_betweenx([ymax_lin_min, ymax_lin_max], K, xlim_max, alpha=alpha, color="blue", label="Saturation Region")

    ax.axvline(x=K, ls="dotted", color="k")
    ax.set_xlabel(sensor_input, fontsize=14)
    ax.set_xscale("log")
    ax.set_xlim(xlim_min, xlim_max)
    ax.set_ylabel(output, fontsize=14)
    ax.set_yscale("log")
    ax.set_ylim(ylim_min, ylim_max)
    ax.legend()
    if show:
        plt.show()
    return ax

# -

def create_sensor_contracts2(sensor_input="AHL", output="FP", K=0.0, yleak=0.0,
                            start=0.0, ymax_lin=0.0, std=0.0):
    """
    Creates the contracts for a Marionette sensing subsystem
    params:
        * input (str): The inducer input to the sensor
        * output (str): The output of the genetic construct.
                        Inducer activates the production of this output
        * K (float): The value of the Hill activation parameter K
        * yleak (float): The minimum expression of output even
                         in absence of inducer
        * start (float): The value of inducer at which the induction starts
        * ymax_lin (float): The maximum expression of output by the inducer
                            before saturating (the end of linear regime)
        * std (float): The standard deviation for each value to create contracts
    """    
    yleak1 = yleak + std * yleak
    yleak2 = yleak - std * yleak
    ymax_lin1 = ymax_lin - std*ymax_lin
    ymax_lin2 = ymax_lin + std*ymax_lin
    slope1 = (ymax_lin1 - yleak1) / (K - start)
    slope2 = (ymax_lin2 - yleak2) / (K - start)
    intercept1 = yleak1 - slope1 * start
    intercept2 = yleak2 - slope2 * start
    contract_0 = PolyhedralContract.from_string(
        input_vars=[sensor_input],
        output_vars=[output],
        assumptions=[f"{sensor_input} <= {start}"],
        guarantees=[f"{output} <= {yleak1}",
                    f"-{output} <= {-1 * yleak2}"]
    )                
    contract_lin = PolyhedralContract.from_string(
        input_vars=[sensor_input],
        output_vars=[output],
        assumptions=[
            f"{sensor_input} <= {K}",
            f"-{sensor_input} <= {-1 * start}"
        ],
        guarantees=[
            f"-{output} + {slope1}{sensor_input} <= {-1*intercept1}",
            f"{output} - {slope2}{sensor_input} <= {1 * intercept2}"
        ]
    )
    contract_max = PolyhedralContract.from_string(
        input_vars=[sensor_input],
        output_vars=[output],
        assumptions=[
            f"-{sensor_input} <= {-1 * K}"
        ],
        guarantees=[
            f"-{output} <= {-1 * ymax_lin1}",
        ]
    )
    return contract_0, contract_lin, contract_max