"""
    Date:   11/13/2021
    Author: Martin E. Liza
    File:   chapter1.py
    Def:    Plots chapter 2

"""
import matplotlib.pyplot as plt
from ambiance import Atmosphere
import pandas as pd
import matplotlib.pyplot as plt
import os


def temperature_ratio_plot(data_path, plotting_path):
    perfect_gas = pd.read_csv(os.path.join(data_path, "calorically_perfect.csv"))
    e1 = pd.read_csv(os.path.join(data_path, "1e-1atm.csv"))
    e2 = pd.read_csv(os.path.join(data_path, "1e-2atm.csv"))
    e4 = pd.read_csv(os.path.join(data_path, "1e-4atm.csv"))

    # Config Figure
    fig_config = {}
    fig_config["line_width"] = 3
    fig_config["fig_width"] = 6
    fig_config["fig_height"] = 5
    fig_config["dpi_size"] = 600
    fig_config["ticks_size"] = 12
    fig_config["legend_size"] = 11
    fig_config["axis_label_size"] = 16
    fig_config["title_size"] = 18

    # Plotting
    plt.plot(
        perfect_gas["U"],
        perfect_gas["T_ratio"],
        label="Calorically perfect gas",
        linewidth=fig_config['line_width']
    )

    plt.plot(
        e1["U"], e1["T_ratio"], label="$1e^{-1}\,[atm],\;h=16[km]$",
        linewidth=fig_config['line_width']
    )

    plt.plot(e2["U"], e2["T_ratio"], label="$1e^{-2}\,[atm],\;h=31[km]$", 
        linewidth=fig_config['line_width'])


    plt.plot(
        e4["U"], e4["T_ratio"], label="$1e^{-4}\,[atm],\;h=65[km]$",
        linewidth=fig_config['line_width'])

    plt.legend(fontsize=fig_config['legend_size'])
    plt.xlabel("$U_1\,[km/s]$", fontsize=fig_config["axis_label_size"])
    plt.ylabel("$T_2/T_1\,[\;]$", fontsize=fig_config["axis_label_size"])
    plt.savefig(os.path.join(ploting_path, "temperatureRatio.pdf"),
                format="pdf", bbox_inches="tight", dpi=600)
    plt.close()


if __name__ == "__main__":
    ploting_path = "../figures/chapter2"
    temperature_ratio_plot("calloricallyPerfectGasData", ploting_path)
