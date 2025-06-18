"""
    Date:   03/26/2023
    Author: Martin E. Liza
    File:   chapter5.py
    Def:    Plots chapter 5 
"""

import os
import scipy.stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import IPython
import figure_configurations
from haot import optics


def get_dicts(data_path: str, f_in: str) -> tuple[dict, object, dict]:
    """
    Load csv files and returns a dictionary with all the densities
    """
    # Loads all csv
    df_in = pd.read_csv(os.path.join(data_path, f_in), index_col=False)

    # Keys to ignore
    ignore_keys = ("time", "Tt", "Tv", "e+")

    # Check gas type
    if df_in["N2"][0] != 0 and df_in["O2"][0] == 0:
        gas_type = "N2"
    elif df_in["O2"][0] != 0 and df_in["N2"][0] == 0:
        gas_type = "O2"
    else:
        gas_type = "Air"

    if gas_type in ("O2", "N2"):
        # (false_value, true_value) [condition]
        tmp = (("N", "N2", "NO"), ("O", "O2", "NO"))[gas_type == "N2"]
        ignore_keys += tmp

    neutral_dict = {}
    ion_dict = {}
    neutral_species = ["N", "O", "NO", "N2", "O2"]
    # Create a neutral dictionary
    for density_key in neutral_species:
        if density_key in ignore_keys:
            continue
        neutral_dict[density_key] = df_in[density_key].to_numpy()

    if len(df_in.keys()) >= 10:
        ion_dict["N+"] = df_in["N+"].to_numpy()
        ion_dict["O+"] = df_in["O+"].to_numpy()
        ion_dict["NO+"] = df_in["NO+"].to_numpy()
        ion_dict["N2+"] = df_in["N2+"].to_numpy()
        ion_dict["O2+"] = df_in["O2+"].to_numpy()
        ion_dict["e+"] = df_in["e+"].to_numpy()

    temp_dict = {}
    temp_dict["time"] = df_in["time"].to_numpy()
    temp_dict["Tt"] = df_in["Tt"].to_numpy()
    temp_dict["Tv"] = df_in["Tv"].to_numpy()

    return temp_dict, neutral_dict, ion_dict


def plot_chemistry_composition(dict_data, output_png_path, fig_config, cut_dict=None):

    for i in dict_data.keys():
        tmp = dict_data[i]

        #### Temperatures ####
        fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
        plt.semilogx(
            tmp["temperature"]["time"],
            tmp["temperature"]["Tt"],
            linewidth=fig_config["line_width"],
            label="$T_{tr}$",
        )
        plt.semilogx(
            tmp["temperature"]["time"],
            tmp["temperature"]["Tv"],
            linewidth=fig_config["line_width"],
            label="$T_{vr}$",
        )
        plt.xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel("Temperature $[K]$", fontsize=fig_config["axis_label_size"])
        plt.legend(fontsize=fig_config["legend_size"])
        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])

        if cut_dict and i in cut_dict and "temperature" in cut_dict[i]:
            plt.xlim(cut_dict[i]["temperature"])
        plt.savefig(
            os.path.join(output_png_path, f"{i}_temperatures.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        #### Temperatures ####

        ### Mass Fraction ###
        fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
        total_density = sum(tmp["neutral_sp"].values())
        axes1 = fig.add_subplot(111)

        # Create a secondary axis if ion exists
        if tmp["ion_sp"]:
            axes2 = axes1.twinx()

        # Plot Mass Fraction
        for j in tmp["neutral_sp"].keys():
            # Plot Neutral species
            axes1.semilogx(
                tmp["temperature"]["time"],
                tmp["neutral_sp"][j] / total_density,
                linewidth=fig_config["line_width"],
                label=figure_configurations.rename_label(j),
            )
            # Plot Ions
            if tmp["ion_sp"]:
                axes2.semilogx(
                    tmp["temperature"]["time"],
                    tmp["ion_sp"][f"{j}+"] / total_density * 1e3,
                    linestyle="dotted",
                    linewidth=fig_config["line_width"],
                    label=figure_configurations.rename_label(f"{j}+"),
                )

        axes1.legend(fontsize=fig_config["legend_size"])
        axes1.set_ylabel("Mass Fraction $[\;]$", fontsize=fig_config["axis_label_size"])
        axes1.set_xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
        axes1.tick_params(axis="both", labelsize=fig_config["ticks_size"])
        # Modified axis for ions
        if tmp["ion_sp"]:
            axes1.set_ylabel(
                "Neutral Species $[\;]$", fontsize=fig_config["axis_label_size"]
            )
            axes2.set_ylabel(
                "Ion Species $\\times 10^{-3}$ $[\;]$",
                fontsize=fig_config["axis_label_size"],
            )
            axes2.set_xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
            axes2.legend(fontsize=fig_config["legend_size"])
            axes2.tick_params(axis="x", labelsize=fig_config["ticks_size"])

        if cut_dict and i in cut_dict and "massFraction" in cut_dict[i]:
            plt.xlim(cut_dict[i]["massFraction"])
        plt.savefig(
            os.path.join(output_png_path, f"{i}_massFraction.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()

        # Plot Species GladStone-Dale constant
        fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
        axes1 = fig.add_subplot(111)

        # Create a secondary axis if ion exists
        if tmp["ion_sp"]:
            axes2 = axes1.twinx()

        for j in tmp["neutral_sp"].keys():
            axes1.semilogx(
                tmp["temperature"]["time"],
                tmp["gladstone_species"][j] * 1e4,
                linewidth=fig_config["line_width"],
                label=figure_configurations.rename_label(j),
            )
            # Plot Ions
            if tmp["ion_sp"]:
                axes2.semilogx(
                    tmp["temperature"]["time"],
                    tmp["gladstone_species"][f"{j}+"] * 1e7,
                    linestyle="dotted",
                    linewidth=fig_config["line_width"],
                    label=figure_configurations.rename_label(f"{j}+"),
                )
        axes1.legend(fontsize=fig_config["legend_size"])
        axes1.set_xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
        axes1.set_ylabel(
            "Neutral G-D $\\times 10^{4}\,[m^3/kg]$",
            fontsize=fig_config["axis_label_size"],
        )
        axes1.set_ylabel(
            "Species G-D $\\times 10^{-4}\,[m^3/kg]$",
            fontsize=fig_config["axis_label_size"],
        )
        axes1.tick_params(axis="both", labelsize=fig_config["ticks_size"])
        if tmp["ion_sp"]:
            axes2.set_ylabel(
                "Ion G-D $\\times 10^{-7}\,[m^3/kg]$",
                fontsize=fig_config["axis_label_size"],
            )
            axes1.set_ylabel(
                "Neutral GD $\\times 10^{-4}\,[m^3/kg]$",
                fontsize=fig_config["axis_label_size"],
            )
            axes2.set_xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
            axes2.legend(fontsize=fig_config["legend_size"])
            axes2.tick_params(axis="x", labelsize=fig_config["ticks_size"])

        if cut_dict and i in cut_dict and "speciesGladstone" in cut_dict[i]:
            plt.xlim(cut_dict[i]["speciesGladstone"])
        plt.savefig(
            os.path.join(output_png_path, f"{i}_speciesGladstoneDale.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()

        # Plot Total GladStone-Dale
        fig = plt.figure(figsize=(fig_config["fig_width"], fig_config["fig_height"]))
        plt.semilogx(
            tmp["temperature"]["time"],
            tmp["gladstone_total"] * 1e4,
            linewidth=fig_config["line_width"],
            label="Frozen",
        )
        plt.semilogx(
            tmp["temperature"]["time"],
            tmp["gladstone_species"]["gladstone_dale"] * 1e4,
            linewidth=fig_config["line_width"],
            label="Nonequilibrium",
        )
        plt.xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel(
            "Total Gladstone-Dale $\\times 10^{-4}\,[m^3/kg]$",
            fontsize=fig_config["axis_label_size"],
        )
        plt.legend(fontsize=fig_config["legend_size"])
        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        if cut_dict and i in cut_dict and "totalGladstone" in cut_dict[i]:
            plt.xlim(cut_dict[i]["totalGladstone"])
        plt.savefig(
            os.path.join(output_png_path, f"{i}_totalGladstoneDale.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()

        # Plot Refractive Index dense and dilute
        plt.semilogx(
            tmp["temperature"]["time"],
            (tmp["refraction_index"]["dilute"] - 1) * 1e3,
            linewidth=fig_config["line_width"],
            label="dilute",
        )
        plt.semilogx(
            tmp["temperature"]["time"],
            (tmp["refraction_index"]["dense"] - 1) * 1e3,
            "--",
            linewidth=fig_config["line_width"],
            label="dense",
        )
        plt.legend(fontsize=fig_config["legend_size"])
        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        plt.xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel(
            "$(n- 1) \\times 10^3$ $[\;]$", fontsize=fig_config["axis_label_size"]
        )
        if cut_dict and i in cut_dict and "refractiveIndex" in cut_dict[i]:
            plt.xlim(cut_dict[i]["refractiveIndex"])
        plt.savefig(
            os.path.join(output_png_path, f"{i}_refractionIndex.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()

        # Plot Electric Susceptibility 
        plt.semilogx(
            tmp["temperature"]["time"],
            tmp["electric_dilute"] * 1E5,
            linewidth=fig_config["line_width"],
            label="dilute",
        )
        plt.semilogx(
            tmp["temperature"]["time"],
            tmp["electric_dense"] * 1E5,
            "--",
            linewidth=fig_config["line_width"],
            label="dense",
        )
        plt.legend(fontsize=fig_config["legend_size"])
        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        plt.xlabel("Time $[s]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel(
            "$\\chi_e \\times 10^{-5} [\;]$", fontsize=fig_config["axis_label_size"]
        )
        if cut_dict and i in cut_dict and "refractiveIndex" in cut_dict[i]:
            plt.xlim(cut_dict[i]["refractiveIndex"])
        plt.savefig(
            os.path.join(output_png_path, f"{i}_electricSusceptibility.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()

        ##  TESTING ##
        max_gl = np.max(tmp["gladstone_species"]["gladstone_dale"])
        max_Tt = np.max(tmp["temperature"]["Tt"])
        max_Tv = np.max(tmp["temperature"]["Tv"])
        sqrtT = np.sqrt(tmp["temperature"]["Tv"] * tmp["temperature"]["Tt"])
        max_T = np.max(sqrtT)

        plt.figure("Scatter", figsize=(16, 6))

        plt.subplot(131)
        plt.scatter(
            tmp["gladstone_species"]["gladstone_dale"] / max_gl,
            tmp["temperature"]["Tt"] / max_Tt,
        )
        plt.xlabel(
            "Normalized Gladstone-Dale $[\;]$", fontsize=fig_config["axis_label_size"]
        )
        plt.ylabel("Normalized $T_t$ $[\;]$", fontsize=fig_config["axis_label_size"])
        # Calculate correlation coefficients
        correlations = helper_correlations(
            tmp["gladstone_species"]["gladstone_dale"], tmp["temperature"]["Tt"]
        )
        plt.title(correlations, fontsize=fig_config["title_size"])

        plt.subplot(132)
        plt.scatter(
            tmp["gladstone_species"]["gladstone_dale"] / max_gl,
            tmp["temperature"]["Tv"] / max_Tv,
        )
        plt.xlabel(
            "Normalized Gladstone-Dale $[\;]$", fontsize=fig_config["axis_label_size"]
        )
        plt.ylabel("Normalized $T_v$ $[\;]$", fontsize=fig_config["axis_label_size"])
        # Calculate correlation coefficients
        correlations = helper_correlations(
            tmp["gladstone_species"]["gladstone_dale"], tmp["temperature"]["Tv"]
        )
        plt.title(correlations, fontsize=fig_config["title_size"])

        plt.subplot(133)
        plt.scatter(tmp["gladstone_species"]["gladstone_dale"] / max_gl, sqrtT / max_T)
        plt.xlabel(
            "Normalized Gladstone-Dale $[\;]$", fontsize=fig_config["axis_label_size"]
        )
        plt.ylabel(
            "Normalized $\\sqrt{T_{vr}T_{tr}}$ $[\;]$",
            fontsize=fig_config["axis_label_size"],
        )
        # Calculate correlation coefficients
        correlations = helper_correlations(
            tmp["gladstone_species"]["gladstone_dale"], sqrtT
        )
        plt.title(correlations, fontsize=fig_config["title_size"])

        plt.savefig(
            os.path.join(output_png_path, f"{i}_scatterPlots.pdf"),
            format="pdf",
            bbox_inches="tight",
        )
        plt.close()
        ##  TESTING ##


def helper_correlations(x_array, y_array):
    dict_out = {}
    dict_out["pearson"] = scipy.stats.pearsonr(x_array, y_array)[0]
    dict_out["spearman"] = scipy.stats.spearmanr(x_array, y_array)[0]
    dict_out["kendall"] = scipy.stats.kendalltau(x_array, y_array)[0]

    return [f"{k} = {v:.3f}" for k, v in dict_out.items()]


def get_chemistry_cut():
    cut_dict = {}

    # Non species
    cut_dict["1C"] = {
        "temperature": [1e-10, 3e-6],
        "massFraction": [1e-9, 3e-6],
        "speciesGladstone": [1e-9, 3e-6],
        "refractiveIndex": [1e-9, 3e-6],
        "totalGladstone": [1e-9, 3e-6],
    }

    cut_dict["2C"] = {
        "temperature": [1e-10, 3e-6],
        "massFraction": [1e-9, 3e-6],
        "speciesGladstone": [1e-9, 3e-6],
        "refractiveIndex": [1e-9, 3e-6],
        "totalGladstone": [1e-9, 3e-6],
    }

    cut_dict["3C"] = {
        "temperature": [1e-10, 8e-7],
        "massFraction": [1e-10, 2e-6],
        "speciesGladstone": [1e-10, 2e-6],
        "refractiveIndex": [1e-10, 5e-7],
        "totalGladstone": [1e-10, 5e-7],
    }

    # Species
    cut_dict["1S1"] = {
        "temperature": [1e-10, 1e-6],
        "massFraction": [5e-10, 5e-7],
        "speciesGladstone": [5e-10, 5e-7],
        "refractiveIndex": [1e-10, 1e-6],
        "totalGladstone": [1e-10, 1e-6],
    }

    cut_dict["1S2"] = {
        "temperature": [1e-10, 1e-6],
        "massFraction": [5e-10, 5e-7],
        "speciesGladstone": [5e-10, 5e-7],
        "refractiveIndex": [5e-10, 1e-6],
        "totalGladstone": [5e-10, 1e-6],
    }

    cut_dict["2S1"] = {
        "temperature": [1e-9, 1e-4],
        "massFraction": [1e-8, 5e-5],
        "speciesGladstone": [1e-8, 5e-5],
        "refractiveIndex": [2e-9, 8e-5],
        "totalGladstone": [2e-9, 8e-5],
    }

    cut_dict["2S2"] = {
        "temperature": [1e-9, 1e-4],
        "massFraction": [1e-8, 5e-5],
        "speciesGladstone": [1e-8, 5e-5],
        "refractiveIndex": [2e-9, 8e-5],
        "totalGladstone": [2e-9, 8e-5],
    }
    return cut_dict


def optical_properties(
    data_in_path, files_in, output_png_path, fig_config, cut_dict=None
):

    name_in = [x.split(".")[0] for x in files_in]
    dict_data = {}

    gd = optics.gladstone_dale_constant()
    for f_in in name_in:
        dict_data[f_in] = {}
        density_dict = {}
        temp_dict, neutral_dict, ion_dict = get_dicts(data_in_path, f"{f_in}.csv")
        # Use a density dictionary
        density_dict.update(neutral_dict)
        if ion_dict:
            density_dict.update(ion_dict)
            del density_dict["e+"]

        # Calculate Gladstone-Dale Constant and Index of Refraction
        gd_const = optics.gladstone_dale_constant(density_dict)
        refraction_index = optics.index_of_refraction(density_dict)
        electric_dilute = optics.electric_susceptibility(refraction_index['dilute'])
        electric_dense = optics.electric_susceptibility(refraction_index['dense'])

        # Gladstone-Dale constant frozen
        tot_density = sum(density_dict.values())[0]

        # Calculate mass fraction at the initialization
        mass_fraction = dict(
            [(key, value[0] / tot_density) for key, value in density_dict.items()]
        )
        gds = 0.0

        for key in mass_fraction.keys():
            gds += gd[key] * mass_fraction[key]

        dict_data[f_in]["electric_dilute"] = electric_dilute
        dict_data[f_in]["electric_dense"] = electric_dense
        dict_data[f_in]["temperature"] = temp_dict
        dict_data[f_in]["neutral_sp"] = neutral_dict
        dict_data[f_in]["ion_sp"] = ion_dict
        dict_data[f_in]["refraction_index"] = refraction_index
        dict_data[f_in]["gladstone_species"] = gd_const
        dict_data[f_in]["gladstone_total"] = gd_const["gladstone_dale"][0] * np.ones(
            np.shape(temp_dict["time"])
        )

    plot_chemistry_composition(dict_data, output_png_path, fig_config, cut_dict)


def main(cfd_results_abs_path):
    fig_config = figure_configurations.figure_settings()
    species_flag = False

    if not species_flag:
        # Chemistry Composition #
        data_in_path = os.path.join(
            cfd_results_abs_path, "chemistryComposition", "outputs"
        )
        files_in = ["1C.csv", "2C.csv", "3C.csv"]
        output_png_path = "../figures/chapter5/chemistryComposition"
        # Chemistry Composition #
    else:
        # Species #
        data_in_path = os.path.join(cfd_results_abs_path, "species", "outputs")
        files_in = ["1S1.csv", "2S1.csv", "1S2.csv", "2S2.csv"]
        output_png_path = "../figures/chapter5/species"
        # Species #

    cut_dict_chemistry = get_chemistry_cut()
    optical_properties(
        data_in_path, files_in, output_png_path, fig_config, cut_dict_chemistry
    )


if __name__ == "__main__":
    cfd_results_abs_path = "../resultsCFD"
    main(cfd_results_abs_path)
