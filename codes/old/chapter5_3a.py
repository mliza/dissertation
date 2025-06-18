import pickle
import haot
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import scipy.constants as s_const
import figure_configurations
import IPython
import os


def plot_stagnation_fields(data_in, fig_config, out_pdf_fig, cut_dict=None):
    case_names = ["1R", "2R", "3R"]
    # case_names = ['1R']

    # Fluid species
    ions = ["N+", "O+", "NO+", "N2+", "O2+"]
    neutral = ["N", "O", "NO", "N2", "O2"]

    colors = [
        mcolors.TABLEAU_COLORS["tab:blue"],
        mcolors.TABLEAU_COLORS["tab:orange"],
        mcolors.TABLEAU_COLORS["tab:green"],
        mcolors.TABLEAU_COLORS["tab:red"],
        mcolors.TABLEAU_COLORS["tab:purple"],
    ]

    for n in case_names:
        frozen = data_in[f"{n}_frozen_stagnation"]
        noneq = data_in[f"{n}_nonequilibrium_stagnation"]

        ## Plot Temperatures ##
        plt.plot(
            noneq["x"] * 1e3,
            noneq["Temperature_tr"],
            color=colors[0],
            linewidth=fig_config["line_width"],
            label="$T_{tr}$",
        )
        plt.plot(
            noneq["x"] * 1e3,
            noneq["Temperature_ve"],
            color=colors[1],
            linewidth=fig_config["line_width"],
            label="$T_{vib}$",
        )

        plt.plot(
            frozen["x"] * 1e3,
            frozen["Temperature_tr"],
            "-.",
            color=colors[0],
            linewidth=fig_config["line_width"],
        )
        plt.plot(
            frozen["x"] * 1e3,
            frozen["Temperature_ve"],
            "-.",
            color=colors[1],
            linewidth=fig_config["line_width"],
        )
        plt.legend(fontsize=fig_config["legend_size"])

        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel("T $[K]$", fontsize=fig_config["axis_label_size"])

        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])

        if cut_dict and "temperature" in cut_dict[n]:
            plt.xlim(cut_dict[n]["temperature"])
        plt.savefig(
            os.path.join(out_pdf_fig, f"{n}_temperatures.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot Temperatures ##

        ## Plot Pressures ##
        plt.plot(
            noneq["x"] * 1e3,
            noneq["Pressure"] * 1e-3,
            color=colors[0],
            linewidth=fig_config["line_width"],
            label="Nonequilibrium",
        )

        plt.plot(
            frozen["x"] * 1e3,
            frozen["Pressure"] * 1e-3,
            color=colors[1],
            linewidth=fig_config["line_width"],
            label="Frozen",
        )

        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel("P $[kPa]$", fontsize=fig_config["axis_label_size"])

        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        plt.legend(fontsize=fig_config["legend_size"])

        if cut_dict and "temperature" in cut_dict[n]:
            plt.xlim(cut_dict[n]["temperature"])
        plt.savefig(
            os.path.join(out_pdf_fig, f"{n}_pressures.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot Pressures ##

        ## Plot Mass Fraction ##
        for i, value in enumerate(neutral):
            plt.plot(
                noneq["x"] * 1e3,
                noneq[f"MassFrac_{i}"],
                color=colors[i],
                linewidth=fig_config["line_width"],
                label=figure_configurations.rename_label(value),
            )

            plt.plot(
                frozen["x"] * 1e3,
                frozen[f"MassFrac_{i}"],
                "-.",
                color=colors[i],
                linewidth=fig_config["line_width"],
            )
        plt.legend(fontsize=fig_config["legend_size"])

        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel("Mass Fraction $[ ]$", fontsize=fig_config["axis_label_size"])

        if cut_dict and "temperature" in cut_dict[n]:
            plt.xlim(cut_dict[n]["temperature"])
        plt.savefig(
            os.path.join(out_pdf_fig, f"{n}_massFraction.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot Mass Fraction ##

        # Create Density Dictionaries
        frozen_mass_density_dict = create_mass_density_dict(frozen, neutral)
        noneq_mass_density_dict = create_mass_density_dict(noneq, neutral)

        # Calculate AO properties
        frozen_index, frozen_GD, frozen_dielectric = calculate_aero_props(
            frozen_mass_density_dict
        )
        noneq_index, noneq_GD, noneq_dielectric = calculate_aero_props(
            noneq_mass_density_dict
        )

        ## Plot Species GD ##
        for i, value in enumerate(neutral):
            plt.plot(
                noneq["x"] * 1e3,
                noneq_GD[value] * 1e4,
                color=colors[i],
                linewidth=fig_config["line_width"],
                label=figure_configurations.rename_label(value),
            )

            plt.plot(
                frozen["x"] * 1e3,
                frozen_GD[value] * 1e4,
                "-.",
                color=colors[i],
                linewidth=fig_config["line_width"],
            )
        plt.legend(fontsize=fig_config["legend_size"])

        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel(
            "Species G-D $\\times 10^{-4}$ $[m^3/kg]$",
            fontsize=fig_config["axis_label_size"],
        )

        if cut_dict and "temperature" in cut_dict[n]:
            plt.xlim(cut_dict[n]["temperature"])
        plt.savefig(
            os.path.join(out_pdf_fig, f"{n}_speciesGD.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot Species GD ##

        ## Plot total GD ##
        plt.plot(
            noneq["x"] * 1e3,
            noneq_GD["gladstone_dale"] * 1e4,
            color=colors[0],
            linewidth=fig_config["line_width"],
            label="Nonequilibrium",
        )

        plt.plot(
            frozen["x"] * 1e3,
            frozen_GD["gladstone_dale"] * 1e4,
            color=colors[1],
            linewidth=fig_config["line_width"],
            label="Frozen",
        )

        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel(
            "Total GD $\\times 10^{-4}$ $[m^3/kg]$",
            fontsize=fig_config["axis_label_size"],
        )

        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        plt.legend(fontsize=fig_config["legend_size"])

        if cut_dict and "temperature" in cut_dict[n]:
            plt.xlim(cut_dict[n]["temperature"])
        plt.savefig(
            os.path.join(out_pdf_fig, f"{n}_totalGD.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot total GD ##

        ## Plot Index of Refraction ##
        plt.plot(
            noneq["x"] * 1e3,
            (noneq_index["dilute"] - 1) * 1e3,
            color=colors[0],
            linewidth=fig_config["line_width"],
            label="Nonequilibrium",
        )

        plt.plot(
            frozen["x"] * 1e3,
            (frozen_index["dilute"] - 1) * 1e3,
            color=colors[1],
            linewidth=fig_config["line_width"],
            label="Frozen",
        )

        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel(
            "$(n - 1) \\times 10^{3}$ $[ ]$", fontsize=fig_config["axis_label_size"]
        )

        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        plt.legend(fontsize=fig_config["legend_size"])

        if cut_dict and "temperature" in cut_dict[n]:
            plt.xlim(cut_dict[n]["temperature"])
        plt.savefig(
            os.path.join(out_pdf_fig, f"{n}_indexOfRefraction.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot Index of Refraction ##

        ## Plot Dielectric ##
        plt.plot(
            noneq["x"] * 1e3,
            noneq_dielectric / s_const.epsilon_0,
            color=colors[0],
            linewidth=fig_config["line_width"],
            label="Nonequilibrium",
        )

        plt.plot(
            frozen["x"] * 1e3,
            frozen_dielectric / s_const.epsilon_0,
            color=colors[1],
            linewidth=fig_config["line_width"],
            label="Frozen",
        )

        plt.xlabel("X $[mm]$", fontsize=fig_config["axis_label_size"])
        plt.ylabel(
            "$ \\epsilon_m / \\epsilon_0$ $[ ]$", fontsize=fig_config["axis_label_size"]
        )

        plt.xticks(fontsize=fig_config["ticks_size"])
        plt.yticks(fontsize=fig_config["ticks_size"])
        plt.legend(fontsize=fig_config["legend_size"])

        if cut_dict and "temperature" in cut_dict[n]:
            plt.xlim(cut_dict[n]["temperature"])
        plt.savefig(
            os.path.join(out_pdf_fig, f"{n}_dielectricMedium.pdf"),
            format="pdf",
            bbox_inches="tight",
            dpi=fig_config["dpi_size"],
        )
        plt.close()
        ## Plot Dielectric ##


def create_mass_density_dict(data_in, species):
    dict_out = {}
    for s, val in enumerate(species):
        dict_out[val] = data_in[f"Density_{s}"]

    return dict_out


def calculate_aero_props(mass_density_dict):
    index_of_refraction = haot.index_of_refraction(mass_density_dict)
    gladstone_dale_const = haot.gladstone_dale_constant(mass_density_dict)
    dielectric_property = haot.permittivity_material(index_of_refraction["dilute"])

    return index_of_refraction, gladstone_dale_const, dielectric_property


def get_cut_dict():
    cut_dict = {}
    cut_dict["1R"] = {"temperature": [-2.5, 0]}

    cut_dict["2R"] = {"temperature": [-2.5, 0]}

    cut_dict["3R"] = {"temperature": [-2.5, 0]}
    return cut_dict


if __name__ == "__main__":

    out_pdf_fig = "../figures/chapter5/chemistryReaction"
    pickle_path = "../resultsCFD/chemistryReaction/tecOutData/stagnation.pickle"
    fig_config = figure_configurations.figure_settings() 

    cut_dict = get_cut_dict()

    file = open(pickle_path, "rb")
    data_in = pickle.load(file)
    file.close()

    plot_stagnation_fields(data_in, fig_config, out_pdf_fig, cut_dict)
