"""
    Date:   12/11/2024
    Author: Martin E. Liza
    File:   chapter1.py
    Def:    Plots chapter 1

"""

import os
import numpy as np
import matplotlib.pyplot as plt
from haot import optics
from ambiance import Atmosphere


def plot_index(blue_sky, altitude, output_png_path, fig_config):
    """
    Calculates and plot the index of refraction as a function of
    altitude for a blue-sky case, using the optics module in the HAOT package
    """

    # Using Atmosphere to get the layers
    atm = Atmosphere(altitude)
    layers = atm.layer_name
    layer_index = np.unique(layers, return_index=True)
    color_layers = "mediumorchid"
    color_atm = "black"

    # Plots altitude vs. Index of refraction
    plt.plot(
        (blue_sky - 1) * 1e3,
        altitude * 1e-3,
        linewidth=fig_config["line_width"],
        label="blue-sky",
        color=color_atm,
    )

    # Plot atmospheric layers
    for k, layer in enumerate(layer_index[0]):
        plt.axhline(
            y=altitude[layer_index[1][k]] * 1e-3, linestyle="--", color=color_layers
        )

        x_min, x_max = plt.xlim()
        x_pos_left = x_min + 0.05 * (
            x_max - x_min
        )  # Set text position as 5% from the right
        x_pos_right = x_max - 0.05 * (
            x_max - x_min
        )  # Set text position as 5% from the left
        if layer == layer_index[0][-1]:
            plt.text(
                x=x_pos_left,
                y=altitude[layer_index[1][k]] * 1e-3,  # Altitude for the text
                s=layer,
                color=color_layers,
                fontsize=10,
                ha="left",  # [right,left]
                va="bottom",  # Align text below the line
            )
        else:
            plt.text(
                x=x_pos_right,
                y=altitude[layer_index[1][k]] * 1e-3,  # Altitude for the text
                s=layer,
                color=color_layers,
                fontsize=10,
                ha="right",  # [right,left]
                va="bottom",  # Align text below the line
            )

    # X and Y axis
    plt.xlabel("$(n - 1)$ $\\times 10^{3}[\;]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("Altitude $[km]$", fontsize=fig_config["axis_label_size"])
    # plt.legend(fontsize=fig_config['legend_size'])

    # Save figure
    plt.savefig(
        os.path.join(output_png_path, "atmosphericOptics.pdf"),
        format="pdf",
        bbox_inches="tight",
        dpi=fig_config["dpi_size"],
    )
    plt.close()


if __name__ == "__main__":
    fig_config = {}
    fig_config["line_width"] = 3
    fig_config["fig_width"] = 6
    fig_config["fig_height"] = 5
    fig_config["dpi_size"] = 600
    fig_config["ticks_size"] = 14
    fig_config["legend_size"] = 14
    fig_config["axis_label_size"] = 16
    fig_config["title_size"] = 18
    output_png = "../figures/chapter1"

    altitude = np.linspace(0, 81e3, 1000)
    blue_sky = optics.atmospheric_index_of_refraction(altitude)
    plot_index(blue_sky, altitude, output_png, fig_config)
